#!/usr/bin/env bash
# SessionStart hook: refresh the goal-duration corpus.
#
# Runs the hydrate in the BACKGROUND and always exits 0 — a slow or failed hydrate
# must never block or fail session startup. Hydration is incremental (only re-scans
# transcripts touched since last run), so steady-state cost is near zero; the first
# run does a full scan but detached, so startup is unaffected. Output is discarded
# so nothing leaks into the session context.
set -u
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
PY="$(command -v python3 || command -v python || true)"
[ -n "$PY" ] || exit 0
nohup "$PY" "$PLUGIN_ROOT/scripts/hydrate_corpus.py" >/dev/null 2>&1 &
exit 0
