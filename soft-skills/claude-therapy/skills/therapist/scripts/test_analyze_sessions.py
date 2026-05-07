#!/usr/bin/env python3
"""Smoke tests for analyze_sessions.py.

Locks the Claude Code transcript schema (lines have a top-level `type`
field and a nested `message.content` payload) and a few core behaviors:

- classify_message and extract_text unwrap the inner message correctly
- frustration / success matching uses word boundaries (no substring
  false positives like "stopping" → "stop")
- rapid_corrections counts once per cluster, not once per message past
  the threshold
- tool_result user messages do NOT pollute friction analysis

Run directly from this directory:
    python3 test_analyze_sessions.py

Exits non-zero on any failure. No pytest dependency.
"""

import unittest

import analyze_sessions as az


# ─── Sample transcript lines (real Claude Code schema) ─────────────────────

# Real user prompt with string content.
USER_TEXT_LINE: dict = {
    "type": "user",
    "message": {"role": "user", "content": "no, that's not what I asked"},
    "_line": 1,
}

# Real user prompt that should NOT match frustration despite containing
# "wrong" as a substring of another word.
USER_BENIGN_LINE: dict = {
    "type": "user",
    "message": {"role": "user", "content": "the algorithm runs wrongly fast"},
    "_line": 2,
}

# User message whose content is a tool_result block (synthesized by the
# harness from a tool call). Should be classified as a tool_result and
# excluded from friction analysis.
USER_TOOL_RESULT_LINE: dict = {
    "type": "user",
    "message": {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "abc",
                "content": "stop printing this is wrong",
            }
        ],
    },
    "_line": 3,
}

# Assistant turn with a list of text blocks.
ASSISTANT_LIST_LINE: dict = {
    "type": "assistant",
    "message": {
        "role": "assistant",
        "content": [{"type": "text", "text": "Sure, I'll do that."}],
    },
    "_line": 4,
}


class TestSchemaUnwrapping(unittest.TestCase):
    def test_classify_user_text(self) -> None:
        c = az.classify_message(USER_TEXT_LINE)
        self.assertEqual(c["role"], "user")
        self.assertFalse(c["is_tool_use"])
        self.assertFalse(c["is_tool_result"])

    def test_classify_user_tool_result(self) -> None:
        c = az.classify_message(USER_TOOL_RESULT_LINE)
        self.assertEqual(c["role"], "user")
        self.assertTrue(c["is_tool_result"])

    def test_classify_assistant(self) -> None:
        c = az.classify_message(ASSISTANT_LIST_LINE)
        self.assertEqual(c["role"], "assistant")

    def test_extract_text_string(self) -> None:
        self.assertEqual(
            az.extract_text(USER_TEXT_LINE),
            "no, that's not what I asked",
        )

    def test_extract_text_list_blocks(self) -> None:
        self.assertEqual(
            az.extract_text(ASSISTANT_LIST_LINE),
            "Sure, I'll do that.",
        )

    def test_extract_text_skips_tool_result(self) -> None:
        # tool_result content must NOT be flattened — otherwise its text
        # would generate false frustration matches.
        self.assertEqual(az.extract_text(USER_TOOL_RESULT_LINE), "")


class TestWordBoundaryMatching(unittest.TestCase):
    def test_wrong_matches_as_word(self) -> None:
        text = "this is wrong, redo it"
        matched = [name for name, p in az.FRUSTRATION_PATTERNS if p.search(text)]
        self.assertIn("wrong", matched)

    def test_wrong_does_not_match_inside_other_words(self) -> None:
        text = "the algorithm runs wrongly fast"
        matched = [name for name, p in az.FRUSTRATION_PATTERNS if p.search(text)]
        self.assertNotIn("wrong", matched)

    def test_stop_does_not_match_stopping(self) -> None:
        text = "we keep stopping the loop early"
        matched = [name for name, p in az.FRUSTRATION_PATTERNS if p.search(text)]
        self.assertNotIn("stop", matched)

    def test_great_does_not_match_greater(self) -> None:
        text = "the value is greater than zero"
        matched = [name for name, p in az.SUCCESS_PATTERNS if p.search(text)]
        self.assertNotIn("great", matched)


class TestRapidCorrectionClusterCounting(unittest.TestCase):
    """rapid_corrections must count once per cluster, not once per message."""

    def _build_user_msgs(self, texts: list[str]) -> list[dict]:
        msgs: list[dict] = []
        for i, t in enumerate(texts, start=1):
            msgs.append({
                "type": "user",
                "message": {"role": "user", "content": t},
                "_line": i,
            })
        return msgs

    def test_single_cluster_of_five_counts_as_one(self) -> None:
        # 5 frustration messages in a row should be 1 cluster, not 3.
        msgs = self._build_user_msgs([
            "wrong, redo",
            "no, that's not it",
            "i said make it bigger",
            "ugh, just do what i asked",
            "i told you already",
        ])
        stats = az.analyze_session(msgs)
        self.assertEqual(stats["rapid_corrections"], 1)
        self.assertEqual(len(stats["frustration_signals"]), 5)

    def test_two_separated_clusters_count_as_two(self) -> None:
        msgs = self._build_user_msgs([
            "wrong",
            "i said x",
            "ugh",
            "thanks, that works perfectly",   # success — resets
            "looks good",
            "no, that's not it",
            "i meant the other one",
            "wrong again",
        ])
        stats = az.analyze_session(msgs)
        self.assertEqual(stats["rapid_corrections"], 2)

    def test_below_threshold_does_not_count(self) -> None:
        msgs = self._build_user_msgs([
            "wrong",
            "i said x",
            "thanks, that works",
        ])
        stats = az.analyze_session(msgs)
        self.assertEqual(stats["rapid_corrections"], 0)


class TestToolResultFiltering(unittest.TestCase):
    def test_tool_result_user_message_skipped_for_friction(self) -> None:
        # A single tool_result user message followed by a real user prompt:
        # only the real prompt should be counted; tool_result text must not
        # contribute frustration matches even though it contains "stop"
        # and "wrong".
        msgs = [
            USER_TOOL_RESULT_LINE,
            {
                "type": "user",
                "message": {"role": "user", "content": "thanks, that works"},
                "_line": 99,
            },
        ]
        stats = az.analyze_session(msgs)
        self.assertEqual(stats["user_messages"], 1)
        self.assertEqual(len(stats["frustration_signals"]), 0)
        self.assertEqual(len(stats["success_signals"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
