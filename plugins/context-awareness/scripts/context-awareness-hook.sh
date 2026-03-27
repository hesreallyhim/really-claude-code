#!/usr/bin/env bash
# Hook handler:
# - Accepts event type as first argument (UserPromptSubmit, PostToolUse, etc.)
# - Reads persisted statusline context usage for the session.
# - Maintains a separate tracking file for burn rate projections.
# - On UserPromptSubmit: emits enriched context note with burn rate.
# - On PostToolUse/PostToolUseFailure: increments tool counter, emits simple note.

set -euo pipefail

EVENT_TYPE="${1:-unknown}"

if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

INPUT="$(cat 2>/dev/null || true)"
INPUT_SESSION_ID="$(jq -r '.session_id // empty' <<<"$INPUT" 2>/dev/null || true)"
ENV_SESSION_ID="${SESSION_ID:-}"
SESSION_ID="${INPUT_SESSION_ID:-$ENV_SESSION_ID}"

if [[ -z "${SESSION_ID}" ]]; then
  exit 0
fi

SAFE_SESSION_ID="$(printf '%s' "$SESSION_ID" | tr -cd '[:alnum:]_.-')"
if [[ -z "${SAFE_SESSION_ID}" ]]; then
  exit 0
fi

STATE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-awareness/state"
STATE_FILE="${STATE_DIR}/session-${SAFE_SESSION_ID}.json"
TRACKING_FILE="${STATE_DIR}/session-${SAFE_SESSION_ID}-tracking.json"


if [[ ! -s "$STATE_FILE" ]]; then
  exit 0
fi

# --- Read current percentage from statusline state ---

USED_PCT="$(jq -r '.context_window.used_percentage // empty' "$STATE_FILE" 2>/dev/null || true)"
if [[ -z "${USED_PCT}" ]]; then
  exit 0
fi

if ! [[ "$USED_PCT" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  exit 0
fi

USED_INT="$(printf '%.0f' "$USED_PCT")"

# Classify usage level
if (( USED_INT >= 90 )); then
  AMOUNT="critical"
elif (( USED_INT >= 80 )); then
  AMOUNT="very large"
elif (( USED_INT >= 70 )); then
  AMOUNT="large"
elif (( USED_INT >= 50 )); then
  AMOUNT="medium"
elif (( USED_INT >= 25 )); then
  AMOUNT="small"
else
  AMOUNT="very small"
fi

# --- Load tracking state (separate file to avoid races with statusline wrapper) ---

TRACKING="{}"
if [[ -s "$TRACKING_FILE" ]]; then
  TRACKING="$(cat "$TRACKING_FILE" 2>/dev/null || echo '{}')"
fi

TOOL_CALLS="$(jq -r '.tool_call_count // 0' <<<"$TRACKING" 2>/dev/null || echo 0)"
TURN_COUNT="$(jq -r '.turn_count // 0' <<<"$TRACKING" 2>/dev/null || echo 0)"
FIRST_SEEN="$(jq -r '.first_seen_pct // empty' <<<"$TRACKING" 2>/dev/null || true)"
LAST_PROMPT="$(jq -r '.last_prompt_pct // empty' <<<"$TRACKING" 2>/dev/null || true)"
EFFORT_MODE="$(jq -r '.effort_mode // "off"' <<<"$TRACKING" 2>/dev/null || echo off)"
ORIGINAL_EFFORT="$(jq -r '.original_effort // empty' <<<"$TRACKING" 2>/dev/null || true)"

# Read current effort level from Claude settings
SETTINGS_FILE="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
EFFORT_LEVEL="$(jq -r '.effortLevel // "default"' "$SETTINGS_FILE" 2>/dev/null || echo "default")"

# Capture the user's original effort level before any adaptive changes
if [[ -z "$ORIGINAL_EFFORT" ]]; then
  ORIGINAL_EFFORT="$EFFORT_LEVEL"
fi

# Initialize first_seen on first encounter
if [[ -z "$FIRST_SEEN" ]]; then
  FIRST_SEEN="$USED_PCT"
fi

# Detect compaction: current percentage dropped well below first_seen
if awk "BEGIN { exit !($USED_PCT < $FIRST_SEEN - 5) }" 2>/dev/null; then
  TOOL_CALLS=0
  TURN_COUNT=0
  FIRST_SEEN="$USED_PCT"
  LAST_PROMPT="$USED_PCT"
fi

if [[ -z "$LAST_PROMPT" ]]; then
  LAST_PROMPT="$USED_PCT"
fi

# --- Update counters and produce output ---

TMP_TRACKING="${TRACKING_FILE}.$$"

write_tracking() {
  jq -cn \
    --argjson tc "$TOOL_CALLS" \
    --argjson tn "$TURN_COUNT" \
    --argjson fs "$FIRST_SEEN" \
    --argjson lp "${LAST_PROMPT:-$USED_PCT}" \
    --arg el "$EFFORT_LEVEL" \
    --arg em "$EFFORT_MODE" \
    --arg oe "$ORIGINAL_EFFORT" \
    '{tool_call_count: $tc, turn_count: $tn, first_seen_pct: $fs, last_prompt_pct: $lp, effort_level: $el, effort_mode: $em, original_effort: $oe}' \
    >"$TMP_TRACKING" 2>/dev/null && mv "$TMP_TRACKING" "$TRACKING_FILE"
}

# --- Adaptive effort control ---
# Applies threshold-based effort downshifting when effort_mode == "adaptive".
# Only runs on UserPromptSubmit to avoid thrashing on every tool call.

apply_adaptive_effort() {
  if [[ "$EFFORT_MODE" != "adaptive" ]]; then
    return
  fi

  local target=""
  if (( USED_INT >= 70 )); then
    target="low"
  elif (( USED_INT >= 50 )); then
    target="medium"
  fi

  # No change needed if below thresholds or already at/below target
  if [[ -z "$target" ]]; then
    return
  fi

  # Map effort levels to numeric ranks for comparison (lower = less effort)
  local -A rank=( [low]=1 [medium]=2 [high]=3 [default]=2 )
  local current_rank="${rank[$EFFORT_LEVEL]:-2}"
  local target_rank="${rank[$target]:-2}"

  # Only downshift — never upshift (user chose their level for a reason)
  if (( current_rank > target_rank )); then
    local TMP_SETTINGS="${SETTINGS_FILE}.$$"
    jq --arg lvl "$target" '.effortLevel = $lvl' "$SETTINGS_FILE" \
      >"$TMP_SETTINGS" 2>/dev/null && mv "$TMP_SETTINGS" "$SETTINGS_FILE"
    EFFORT_LEVEL="$target"
  fi
}

# --- Restore effort on session end ---

restore_effort() {
  if [[ "$EFFORT_MODE" == "off" ]]; then
    return
  fi
  if [[ -z "$ORIGINAL_EFFORT" || "$ORIGINAL_EFFORT" == "$EFFORT_LEVEL" ]]; then
    return
  fi
  local TMP_SETTINGS="${SETTINGS_FILE}.$$"
  jq --arg lvl "$ORIGINAL_EFFORT" '.effortLevel = $lvl' "$SETTINGS_FILE" \
    >"$TMP_SETTINGS" 2>/dev/null && mv "$TMP_SETTINGS" "$SETTINGS_FILE"
}

case "$EVENT_TYPE" in
  PostToolUse|PostToolUseFailure)
    TOOL_CALLS=$((TOOL_CALLS + 1))
    write_tracking
    printf '[context: %s%% (%s)]\n' "$USED_INT" "$AMOUNT" | tee /dev/stderr
    ;;

  UserPromptSubmit)
    TURN_COUNT=$((TURN_COUNT + 1))

    # Apply adaptive effort before computing metrics (so effort_level is current)
    PREV_EFFORT="$EFFORT_LEVEL"
    apply_adaptive_effort

    # Delta from last prompt
    DELTA_FMT="$(awk "BEGIN {v = $USED_PCT - $LAST_PROMPT; if (v >= 0) printf \"+%.1f\", v; else printf \"%.1f\", v}" 2>/dev/null || echo "+0.0")"

    # Burn rate per tool call
    BURN_RATE=""
    REMAINING=""
    if (( TOOL_CALLS > 0 )); then
      BURN_RATE="$(awk "BEGIN {printf \"%.2f\", ($USED_PCT - $FIRST_SEEN) / $TOOL_CALLS}" 2>/dev/null || echo "")"
      IS_POSITIVE="$(awk "BEGIN {print (($USED_PCT - $FIRST_SEEN) / $TOOL_CALLS > 0.001) ? 1 : 0}" 2>/dev/null || echo 0)"
      if [[ "$IS_POSITIVE" == "1" ]]; then
        REMAINING="$(awk "BEGIN {
          r = (100 - $USED_PCT) / (($USED_PCT - $FIRST_SEEN) / $TOOL_CALLS)
          if (r > 1000) print \">1000\"
          else printf \"%.0f\", r
        }" 2>/dev/null || echo "")"
      fi
    fi

    # Save current pct as last_prompt_pct for next delta
    LAST_PROMPT="$USED_PCT"
    write_tracking

    # Build output
    OUTPUT="[context: ${USED_INT}% (${AMOUNT})"

    if (( TURN_COUNT > 1 )); then
      OUTPUT="${OUTPUT} | ${DELTA_FMT}% last turn"
    fi

    if [[ -n "$BURN_RATE" && -n "$REMAINING" ]]; then
      OUTPUT="${OUTPUT} | ~${BURN_RATE}%/tool | ~${REMAINING} tool calls remaining"
    elif (( TOOL_CALLS == 0 )); then
      OUTPUT="${OUTPUT} | burn rate: calculating..."
    fi

    # Show effort mode status when active
    if [[ "$EFFORT_MODE" != "off" ]]; then
      OUTPUT="${OUTPUT} | effort: ${EFFORT_MODE}(${EFFORT_LEVEL})"
      # Note if adaptive just changed the level
      if [[ "$EFFORT_MODE" == "adaptive" && "$PREV_EFFORT" != "$EFFORT_LEVEL" ]]; then
        OUTPUT="${OUTPUT} shifted ${PREV_EFFORT}->${EFFORT_LEVEL}"
      fi
    fi

    OUTPUT="${OUTPUT}]"
    printf '%s\n' "$OUTPUT" | tee /dev/stderr
    ;;

  SessionEnd)
    restore_effort
    write_tracking
    ;;

  *)
    printf '[context: %s%% (%s)]\n' "$USED_INT" "$AMOUNT" | tee /dev/stderr
    ;;
esac
