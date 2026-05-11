#!/usr/bin/env python3
"""Validate the calibration of the context-awareness predictor.

Parses past Claude Code session transcripts (~/.claude/projects/<slug>/<uuid>.jsonl)
and computes residuals between consecutive `~K tool calls remaining` predictions
versus the actual tool-call deltas observed in the session.

If burn rate were perfectly stationary, then between two prediction events:
    predicted_K_i  -  predicted_K_{i+1}  ==  tools_between_them
A negative residual means the predictor was optimistic (session burned faster
than its session-average baseline). A positive residual means pessimistic.

Predictions reported as `>1000` (the cap) are skipped — they aren't a real number.

The script reads transcripts only; it does not modify the plugin or the logs.
Standard library only.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from statistics import mean, median


# Match the predictor injection produced by context-awareness-hook.sh.
# Handles both old format `[context: 32% (small) | ...` and the post-2026-05
# format `[context: 32% used (small) | ...`.
PREDICTION_RE = re.compile(
    r"\[context:\s*(\d+)%(?:\s+used)?\s*\([^)]+\)\s*"
    r"\|[^|]+"          # delta field
    r"\|[^|]+"          # burn-rate field
    r"\|\s*~(\d+|>1000)\s*tool calls remaining\]"
)

# The plugin documentation shipped via SessionStart contains a frozen example
# string with the exact values "0.38%/tool | ~179 tool calls remaining". We do
# NOT want to count those as real predictions. Filter them out.
DOC_EXAMPLE_FRAGMENT = "0.38%/tool | ~179 tool calls remaining"


def find_sessions(root: Path) -> list[Path]:
    """Return every JSONL transcript under the projects root."""
    return sorted(root.rglob("*.jsonl"))


def count_tool_uses(message: dict) -> int:
    """Count tool_use blocks inside an assistant message dict."""
    if not isinstance(message, dict):
        return 0
    content = message.get("content")
    if not isinstance(content, list):
        return 0
    return sum(1 for c in content if isinstance(c, dict) and c.get("type") == "tool_use")


def extract_predictions(line: str) -> list[tuple[int, str]]:
    """Return every (used_pct, predicted_K_str) appearing in a JSONL line.

    Filters out the SessionStart documentation example. Returns matches in the
    order they appear in the line. The same injection often appears two or
    three times in a single attachment record (in stdout, content, and
    additionalContext); we deduplicate by matching string at the call site.
    """
    if "tool calls remaining" not in line:
        return []
    matches: list[tuple[int, str]] = []
    for m in PREDICTION_RE.finditer(line):
        full = m.group(0)
        if DOC_EXAMPLE_FRAGMENT in full:
            continue
        used_pct = int(m.group(1))
        k_str = m.group(2)
        matches.append((used_pct, k_str))
    return matches


def parse_session(path: Path) -> dict | None:
    """Return per-session prediction records or None if it doesn't qualify.

    Each record is a dict with:
      - prediction_index (int, sequential within session)
      - predicted_K (int) or None if predictor returned ">1000"
      - cumulative_tools (int) — tool_use blocks in assistant messages
        strictly before this prediction line
      - used_pct (int)
    """
    predictions: list[dict] = []
    cumulative_tools = 0
    pred_index = 0

    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return None

    for line in lines:
        # Update tool count first if this line is an assistant message.
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(d, dict):
            continue

        line_type = d.get("type")

        # Look for predictions in attachment lines from UserPromptSubmit hook.
        if line_type == "attachment":
            attachment = d.get("attachment", {})
            if isinstance(attachment, dict) and attachment.get("hookEvent") == "UserPromptSubmit":
                # Each prediction injection appears multiple times in the
                # attachment payload (stdout, content, etc). Deduplicate so
                # we count one prediction event per attachment line.
                local_seen: set[tuple[int, str]] = set()
                for used_pct, k_str in extract_predictions(line):
                    key = (used_pct, k_str)
                    if key in local_seen:
                        continue
                    local_seen.add(key)
                    pred_index += 1
                    predictions.append({
                        "prediction_index": pred_index,
                        "used_pct": used_pct,
                        "predicted_K": None if k_str == ">1000" else int(k_str),
                        "cumulative_tools": cumulative_tools,
                    })

        # Count tool_uses in assistant messages.
        if line_type == "assistant":
            cumulative_tools += count_tool_uses(d.get("message", {}))

    # Qualifies if at least 5 real predictions exist.
    if len(predictions) < 5:
        return None
    return {
        "path": str(path),
        "predictions": predictions,
    }


def compute_residuals(predictions: list[dict]) -> list[dict]:
    """Compute residual_i = (K_i - K_{i+1}) - (tools_{i+1} - tools_i).

    Skips pairs where either prediction is None (the >1000 cap).
    """
    residuals: list[dict] = []
    for i in range(len(predictions) - 1):
        a, b = predictions[i], predictions[i + 1]
        if a["predicted_K"] is None or b["predicted_K"] is None:
            continue
        delta_pred = a["predicted_K"] - b["predicted_K"]
        delta_tools = b["cumulative_tools"] - a["cumulative_tools"]
        residual = delta_pred - delta_tools
        residuals.append({
            "from_idx": a["prediction_index"],
            "to_idx": b["prediction_index"],
            "delta_pred": delta_pred,
            "delta_tools": delta_tools,
            "residual": residual,
            "from_used_pct": a["used_pct"],
            "to_used_pct": b["used_pct"],
        })
    return residuals


def percentile(values: list[float], p: float) -> float:
    """Linear-interpolation percentile (p in [0, 100]). Empty -> nan."""
    if not values:
        return float("nan")
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * (p / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    frac = k - lo
    return s[lo] * (1 - frac) + s[hi] * frac


def main() -> int:
    # ~/.claude/projects/
    projects_root = Path.home() / ".claude" / "projects"
    if not projects_root.exists():
        print(f"ERROR: projects root not found at {projects_root}", file=sys.stderr)
        return 1

    sessions: list[dict] = []
    files = find_sessions(projects_root)
    print(f"Scanning {len(files)} JSONL transcripts under {projects_root} ...")
    for p in files:
        result = parse_session(p)
        if result is not None:
            sessions.append(result)
    print(f"Qualifying sessions (>=5 predictions): {len(sessions)}")

    all_residuals: list[dict] = []
    for s in sessions:
        for r in compute_residuals(s["predictions"]):
            r["session"] = s["path"]
            all_residuals.append(r)

    n = len(all_residuals)
    print(f"Total prediction pairs (excluding >1000 cap on either side): {n}")
    if n == 0:
        print("No usable prediction pairs.")
        return 0

    residuals = [r["residual"] for r in all_residuals]
    abs_residuals = [abs(x) for x in residuals]

    print()
    print("=" * 60)
    print("Calibration statistics")
    print("=" * 60)
    print(f"Mean residual           : {mean(residuals):+.2f}  (positive=pessimistic, negative=optimistic)")
    print(f"Median residual         : {median(residuals):+.2f}")
    print(f"Mean |residual|         : {mean(abs_residuals):.2f}")
    print(f"Median |residual|       : {median(abs_residuals):.2f}")
    print(f"95th pct |residual|     : {percentile(abs_residuals, 95):.2f}")
    print(f"99th pct |residual|     : {percentile(abs_residuals, 99):.2f}")
    print(f"Max |residual|          : {max(abs_residuals):.2f}")

    # Min/max signed.
    print(f"Min residual (most opt.) : {min(residuals):+.2f}")
    print(f"Max residual (most pes.) : {max(residuals):+.2f}")

    # How many pairs are within ±5, ±10, ±25?
    for thresh in (1, 5, 10, 25, 50):
        within = sum(1 for x in abs_residuals if x <= thresh)
        print(f"|residual| <= {thresh:>3}        : {within}/{n}  ({100*within/n:.1f}%)")

    # Top spike events.
    print()
    print("Top 5 |residual| spikes:")
    top = sorted(all_residuals, key=lambda r: abs(r["residual"]), reverse=True)[:5]
    for r in top:
        sess = os.path.basename(r["session"])
        proj = os.path.basename(os.path.dirname(r["session"]))
        print(f"  residual={r['residual']:+5d}  pred {r['from_idx']:3d}->{r['to_idx']:3d}  "
              f"used%={r['from_used_pct']:>2}->{r['to_used_pct']:<2}  "
              f"deltaK={r['delta_pred']:+4d}  deltaTools={r['delta_tools']:+4d}  "
              f"{proj}/{sess}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
