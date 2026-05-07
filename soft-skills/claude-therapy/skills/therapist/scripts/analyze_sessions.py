#!/usr/bin/env python3
"""
Session Log Analyzer for Claude Code Therapy Sessions

Parses JSONL transcript files from Claude Code sessions and extracts
interaction patterns, friction signals, and collaboration metrics.

Usage:
    python3 analyze_sessions.py [--days 7] [--verbose] [--output FILE]
"""

import json
import os
import re
import sys
import glob
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict


# ─── Friction signal keywords ───────────────────────────────────────────────
# Each entry is (display_name, regex_pattern). Patterns use word
# boundaries (\b) so short tokens like "stop", "wrong", or "no," do not
# match benign substrings (e.g. "stopping", "wrongly", "kimono"). All
# matching is done against text that has already been lowercased, so
# patterns themselves are lowercase and re.IGNORECASE is unnecessary.
FRUSTRATION_SIGNALS: list[tuple[str, str]] = [
    ("no, ", r"\bno,\s"),
    ("that's not", r"\bthat'?s not\b"),
    ("i said", r"\bi said\b"),
    ("i already", r"\bi already\b"),
    ("wrong", r"\bwrong\b"),
    ("try again", r"\btry again\b"),
    ("not what i", r"\bnot what i\b"),
    ("i meant", r"\bi meant\b"),
    ("i don't want", r"\bi don'?t want\b"),
    ("just do", r"\bjust do\b"),
    ("stop", r"\bstop\b"),
    ("ugh", r"\bugh\b"),
    ("sigh", r"\bsigh\b"),
    ("seriously", r"\bseriously\b"),
    ("come on", r"\bcome on\b"),
    ("forget it", r"\bforget it\b"),
    ("never mind", r"\bnever ?mind\b"),
    ("why did you", r"\bwhy did you\b"),
    ("why didn't you", r"\bwhy didn'?t you\b"),
    ("i told you", r"\bi told you\b"),
]

SUCCESS_SIGNALS: list[tuple[str, str]] = [
    ("perfect", r"\bperfect\b"),
    ("great", r"\bgreat\b"),
    ("exactly", r"\bexactly\b"),
    ("nice", r"\bnice\b"),
    ("awesome", r"\bawesome\b"),
    ("thanks", r"\bthanks\b"),
    ("that works", r"\bthat works\b"),
    ("looks good", r"\blooks good\b"),
    ("love it", r"\blove it\b"),
    ("well done", r"\bwell done\b"),
    ("nailed it", r"\bnailed it\b"),
    ("ship it", r"\bship it\b"),
    ("lgtm", r"\blgtm\b"),
    ("merge it", r"\bmerge it\b"),
]

FRUSTRATION_PATTERNS: list[tuple[str, re.Pattern]] = [
    (name, re.compile(pat)) for name, pat in FRUSTRATION_SIGNALS
]
SUCCESS_PATTERNS: list[tuple[str, re.Pattern]] = [
    (name, re.compile(pat)) for name, pat in SUCCESS_SIGNALS
]

OVER_SPECIFICATION_THRESHOLD = 500  # chars — user prompt is very long
RAPID_CORRECTION_WINDOW = 3        # corrections within N exchanges = friction


def find_transcripts(days=7):
    """Find all session transcript JSONL files modified within the given timeframe.

    Claude Code stores each session as `~/.claude/projects/<encoded-cwd>/<session-uuid>.jsonl`,
    where `<encoded-cwd>` is the absolute project path with `/` replaced by `-`.

    Subagent transcripts at `<session-id>/subagents/agent-<uuid>.jsonl` are
    excluded by design. This script analyzes user-Claude collaboration; in a
    subagent transcript, `role:"user"` messages are the parent Claude's
    prompts to the subagent, not real user input. Treating them as user input
    would corrupt friction-signal counts. The parent session's own transcript
    already records every Task invocation, so no signal is lost at the
    user-facing level.
    """
    transcripts = []
    cutoff = datetime.now() - timedelta(days=days)

    base = os.path.expanduser("~/.claude/projects/")
    pattern = os.path.join(base, "**", "*.jsonl")
    # Build the subagent-path token using os.sep so the exclusion works on
    # Windows (where paths use backslash separators) as well as POSIX.
    subagents_token = os.sep + "subagents" + os.sep
    for path in glob.glob(pattern, recursive=True):
        if subagents_token in path:
            continue
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            if mtime >= cutoff:
                transcripts.append((path, mtime))
        except OSError:
            continue

    transcripts.sort(key=lambda x: x[1], reverse=True)
    return transcripts


def parse_transcript(filepath):
    """Parse a JSONL transcript file into structured messages."""
    messages = []
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                msg["_line"] = line_num
                messages.append(msg)
            except json.JSONDecodeError:
                continue
    return messages


def classify_message(msg):
    """Classify a message by role and type.

    Claude Code transcript lines are shaped:
        {"type": "user"|"assistant", "message": {"role": ..., "content": ...}, ...}
    The role and content are nested under `message`. We unwrap it here so
    callers can treat top-level and nested-message lines uniformly.
    """
    inner = msg.get("message") if isinstance(msg.get("message"), dict) else msg
    # Prefer the inner role; fall back to the top-level `type` (which
    # carries the same role label for user/assistant lines).
    role = inner.get("role") or msg.get("type") or "unknown"

    # Detect tool use / tool result
    is_tool_use = False
    is_tool_result = False
    content = inner.get("content")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "tool_use":
                    is_tool_use = True
                elif block.get("type") == "tool_result":
                    is_tool_result = True

    return {
        "role": role,
        "is_tool_use": is_tool_use,
        "is_tool_result": is_tool_result,
    }


def extract_text(msg):
    """Extract human-readable text from a message.

    Unwraps `msg["message"]` (the standard Claude Code transcript schema)
    before reading content. For string content (typical user prompts),
    returns the string directly. For block-list content (typical assistant
    responses), concatenates `text`-type blocks only. tool_result and
    tool_use blocks are intentionally skipped — including their text
    would produce false frustration/success matches against arbitrary
    tool output (e.g. a log line containing the word "stop").
    """
    inner = msg.get("message") if isinstance(msg.get("message"), dict) else msg
    content = inner.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return " ".join(parts)
    return ""


def analyze_session(messages):
    """Analyze a single session's messages for patterns."""
    stats = {
        "total_messages": len(messages),
        "user_messages": 0,
        "assistant_messages": 0,
        "tool_uses": 0,
        "frustration_signals": [],
        "success_signals": [],
        "long_prompts": 0,
        "rapid_corrections": 0,
        "exchange_lengths": [],  # messages per "task"
        "user_prompt_lengths": [],
    }

    current_exchange = 0
    last_role = None
    consecutive_corrections = 0

    for msg in messages:
        classification = classify_message(msg)
        role = classification["role"]
        text = extract_text(msg).lower()

        # User-role messages whose content is a tool_result block are
        # synthesized by Claude Code (the harness packaging tool output for
        # the assistant), not real user input. Exclude them from friction
        # analysis — but keep counting tool_use so we still see tool activity.
        is_real_user_prompt = (
            role in ("human", "user") and not classification["is_tool_result"]
        )

        if is_real_user_prompt:
            stats["user_messages"] += 1
            prompt_len = len(extract_text(msg))
            stats["user_prompt_lengths"].append(prompt_len)

            if prompt_len > OVER_SPECIFICATION_THRESHOLD:
                stats["long_prompts"] += 1

            # Check frustration signals (word-boundary anchored — see
            # FRUSTRATION_PATTERNS for why short tokens like "stop" or
            # "wrong" are matched as whole words rather than substrings).
            matched_frustration = False
            for signal, pattern in FRUSTRATION_PATTERNS:
                if pattern.search(text):
                    stats["frustration_signals"].append({
                        "signal": signal,
                        "excerpt": text[:120],
                        "line": msg.get("_line", 0),
                    })
                    matched_frustration = True
                    break

            if matched_frustration:
                consecutive_corrections += 1
                # Count once per cluster: only when crossing the threshold.
                # If frustration continues past the window, we don't keep
                # incrementing — that would report 1 cluster of 5 messages
                # as 3 clusters.
                if consecutive_corrections == RAPID_CORRECTION_WINDOW:
                    stats["rapid_corrections"] += 1
            else:
                consecutive_corrections = 0

            # Check success signals (also word-boundary anchored)
            for signal, pattern in SUCCESS_PATTERNS:
                if pattern.search(text):
                    stats["success_signals"].append({
                        "signal": signal,
                        "excerpt": text[:120],
                        "line": msg.get("_line", 0),
                    })
                    break

        elif role in ("assistant",):
            stats["assistant_messages"] += 1

        if classification["is_tool_use"]:
            stats["tool_uses"] += 1

        # Track exchange boundaries (user -> assistant = 1 exchange).
        # Only real user prompts mark a new exchange; tool_result user
        # messages continue the assistant's in-flight turn.
        if is_real_user_prompt and last_role in ("assistant", None):
            if current_exchange > 0:
                stats["exchange_lengths"].append(current_exchange)
            current_exchange = 1
        else:
            current_exchange += 1

        # last_role tracks the *effective* conversational role: tool_result
        # user messages don't reset the assistant's turn for exchange
        # accounting.
        last_role = "user" if is_real_user_prompt else (role if role == "assistant" else last_role)

    if current_exchange > 0:
        stats["exchange_lengths"].append(current_exchange)

    return stats


def compute_metrics(all_stats: list[dict]) -> dict[str, int | float]:
    """Compute aggregate metrics across all sessions."""
    metrics: dict[str, int | float] = {
        "sessions_analyzed": len(all_stats),
        "total_exchanges": sum(s["user_messages"] for s in all_stats),
        "total_frustration_events": sum(len(s["frustration_signals"]) for s in all_stats),
        "total_success_events": sum(len(s["success_signals"]) for s in all_stats),
        "total_rapid_corrections": sum(s["rapid_corrections"] for s in all_stats),
        "total_long_prompts": sum(s["long_prompts"] for s in all_stats),
        "avg_prompt_length": 0,
        "frustration_rate": 0.0,
        "success_rate": 0.0,
    }

    all_prompt_lengths = []
    for s in all_stats:
        all_prompt_lengths.extend(s["user_prompt_lengths"])

    if all_prompt_lengths:
        metrics["avg_prompt_length"] = sum(all_prompt_lengths) // len(all_prompt_lengths)

    total_user_msgs = sum(s["user_messages"] for s in all_stats)
    if total_user_msgs > 0:
        metrics["frustration_rate"] = round(
            metrics["total_frustration_events"] / total_user_msgs * 100, 1
        )
        metrics["success_rate"] = round(
            metrics["total_success_events"] / total_user_msgs * 100, 1
        )

    return metrics


def generate_report(transcripts_info, all_stats, metrics):
    """Generate a markdown report."""
    lines = []
    lines.append("# Session Analysis Report")
    lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Sessions analyzed:** {metrics['sessions_analyzed']}")
    lines.append(f"**Total user messages:** {metrics['total_exchanges']}")

    lines.append("\n## Sessions Reviewed")
    for path, mtime in transcripts_info:
        lines.append(f"- `{path}` (modified {mtime.strftime('%Y-%m-%d %H:%M')})")

    lines.append("\n## Aggregate Metrics")
    lines.append(f"- Average user prompt length: **{metrics['avg_prompt_length']} chars**")
    lines.append(f"- Frustration signal rate: **{metrics['frustration_rate']}%** of user messages")
    lines.append(f"- Success signal rate: **{metrics['success_rate']}%** of user messages")
    lines.append(f"- Rapid correction clusters: **{metrics['total_rapid_corrections']}**")
    lines.append(f"- Over-long prompts (>{OVER_SPECIFICATION_THRESHOLD} chars): **{metrics['total_long_prompts']}**")

    # Top frustration signals
    all_frustrations = []
    for s in all_stats:
        all_frustrations.extend(s["frustration_signals"])

    if all_frustrations:
        lines.append("\n## Frustration Signals Detected")
        signal_counts = Counter(f["signal"] for f in all_frustrations)
        for signal, count in signal_counts.most_common(10):
            lines.append(f"- `{signal}` — appeared {count} time(s)")

        lines.append("\n### Sample Excerpts")
        for f in all_frustrations[:5]:
            lines.append(f"- Line {f['line']}: _{f['excerpt']}_")

    # Success signals
    all_successes = []
    for s in all_stats:
        all_successes.extend(s["success_signals"])

    if all_successes:
        lines.append("\n## Success Signals Detected")
        signal_counts = Counter(f["signal"] for f in all_successes)
        for signal, count in signal_counts.most_common(10):
            lines.append(f"- `{signal}` — appeared {count} time(s)")

    # Session-by-session summary
    lines.append("\n## Per-Session Breakdown")
    for i, (info, stats) in enumerate(zip(transcripts_info, all_stats)):
        path, mtime = info
        lines.append(f"\n### Session {i+1} ({mtime.strftime('%Y-%m-%d')})")
        lines.append(f"- Messages: {stats['total_messages']} ({stats['user_messages']} user, {stats['assistant_messages']} assistant)")
        lines.append(f"- Tool uses: {stats['tool_uses']}")
        lines.append(f"- Frustration events: {len(stats['frustration_signals'])}")
        lines.append(f"- Success events: {len(stats['success_signals'])}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze Claude Code session logs")
    parser.add_argument("--days", type=int, default=7, help="Look back N days (default: 7)")
    parser.add_argument("--verbose", action="store_true", help="Print detailed output")
    parser.add_argument("--output", help="Write report to file instead of stdout")
    args = parser.parse_args()

    transcripts = find_transcripts(args.days)

    if not transcripts:
        print(f"No session transcripts found in the last {args.days} days.", file=sys.stderr)
        print("Checked: ~/.claude/projects/**/*.jsonl", file=sys.stderr)
        print("\nThe therapist can still run a prospective session without logs.", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Found {len(transcripts)} transcript(s):", file=sys.stderr)
        for path, mtime in transcripts:
            print(f"  {path} ({mtime})", file=sys.stderr)

    all_stats = []
    for path, mtime in transcripts:
        messages = parse_transcript(path)
        if messages:
            stats = analyze_session(messages)
            all_stats.append(stats)

    if not all_stats:
        print("Transcripts found but contained no parseable messages.", file=sys.stderr)
        sys.exit(1)

    metrics = compute_metrics(all_stats)
    report = generate_report(transcripts, all_stats, metrics)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
