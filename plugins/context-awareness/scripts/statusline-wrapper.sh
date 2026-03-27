#!/usr/bin/env bash
# Statusline wrapper:
# - Reads statusline JSON from stdin.
# - Persists session-scoped context-window usage for hook readers.
# - Produces no stdout so it can be safely prepended to existing statusline commands.

set -u

if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

INPUT="$(cat 2>/dev/null || true)"
if [[ -z "${INPUT}" ]]; then
  exit 0
fi

SESSION_ID="$(jq -r '.session_id // empty' <<<"$INPUT" 2>/dev/null || true)"
USED_PCT="$(jq -r '.context_window.used_percentage // empty' <<<"$INPUT" 2>/dev/null || true)"

if [[ -z "${SESSION_ID}" || -z "${USED_PCT}" ]]; then
  exit 0
fi

if ! [[ "$USED_PCT" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  exit 0
fi

SAFE_SESSION_ID="$(printf '%s' "$SESSION_ID" | tr -cd '[:alnum:]_.-')"
if [[ -z "${SAFE_SESSION_ID}" ]]; then
  SAFE_SESSION_ID="unknown"
fi

STATE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-awareness/state"
STATE_FILE="${STATE_DIR}/session-${SAFE_SESSION_ID}.json"
TMP_FILE="${STATE_FILE}.$$"

mkdir -p "$STATE_DIR"
jq -cn \
  --arg session_id "$SESSION_ID" \
  --argjson used_percentage "$USED_PCT" \
  --arg updated_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{
    session_id: $session_id,
    context_window: { used_percentage: $used_percentage },
    updated_at: $updated_at
  }' >"$TMP_FILE" 2>/dev/null || exit 0
mv "$TMP_FILE" "$STATE_FILE"

exit 0
