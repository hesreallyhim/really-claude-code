#!/usr/bin/env bash
# cross-boundary-warning.sh
# Purpose: PreToolUse hook for SendMessage that warns when a message crosses
#          sub-team boundaries. Per ADR D5, boundaries are convention, not
#          enforcement — this hook MUST exit 0 (warn/log) and NEVER exit 2 (block).
#
# Input: Reads the SendMessage tool_input JSON from stdin.
#        Expected fields: { "recipient": "agent-name", "type": "message", ... }
#        The hook also receives the tool_name as the first positional argument
#        from the hooks framework, but we only care about the stdin JSON.
#
# Environment:
#   CLAUDE_PLUGIN_ROOT — base directory of this plugin (set by Claude Code)
#   TEAM_NAME          — the current team name (defaults to "default")
#   SENDER_NAME        — the name of the agent running this hook (defaults to "unknown")
#
#   NOTE: TEAM_NAME and SENDER_NAME are NOT automatically set by the Claude Code
#   hook framework. They must be configured externally (e.g., in the hook's env
#   block in hooks.json, or exported by the spawning agent). Without them, the
#   boundary check will silently skip (agents default to "unknown" which has no
#   squad assignment, so no boundary can be detected).
#
# Behavior:
#   - Reads the recipient from the SendMessage tool input
#   - Looks up both sender and recipient in the squad roster
#   - If they are in different squads, outputs a warning to stderr
#   - Always exits 0 — never blocks the message
#
# Dependencies:
#   - jq (for JSON parsing)
#   - roster.sh (sibling script in the plugin)

# SAFETY: Do NOT use "set -e" or "set -o pipefail" in this hook.
# Any non-zero exit from a PreToolUse hook BLOCKS the tool call.
# Per ADR D5, this hook must NEVER block — only warn.
# The ERR trap below guarantees exit 0 even on unexpected failures.
set -u
trap 'exit 0' ERR

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
ROSTER_SCRIPT="${PLUGIN_ROOT}/scripts/roster.sh"
TEAM_NAME="${TEAM_NAME:-default}"
SENDER_NAME="${SENDER_NAME:-unknown}"

# Log file for cross-boundary message audit trail
LOG_DIR="${HOME}/.claude/teams/${TEAM_NAME}/logs"
LOG_FILE="${LOG_DIR}/cross-boundary.log"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

log_warning() {
  local msg="$1"
  mkdir -p "$LOG_DIR"
  echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] WARNING: $msg" >> "$LOG_FILE"
  # Also emit to stderr so it shows up in hook diagnostics
  echo "CROSS-BOUNDARY WARNING: $msg" >&2
}

log_debug() {
  local msg="$1"
  # Only log debug messages if HOOK_DEBUG is set
  if [[ "${HOOK_DEBUG:-}" == "1" ]]; then
    echo "[cross-boundary-hook] $msg" >&2
  fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# Read the tool input JSON from stdin (with safety fallback for empty/closed stdin)
tool_input="$(cat 2>/dev/null || true)"

log_debug "Received tool input: $tool_input"

# Validate that jq is available
if ! command -v jq &>/dev/null; then
  log_debug "jq not available, skipping boundary check"
  exit 0
fi

# Extract the message type and recipient from the tool input
msg_type="$(echo "$tool_input" | jq -r '.type // "message"')"
recipient="$(echo "$tool_input" | jq -r '.recipient // ""')"

log_debug "Message type=$msg_type, recipient=$recipient, sender=$SENDER_NAME"

# Only check direct messages (not broadcasts — those go to everyone by design)
if [[ "$msg_type" != "message" ]]; then
  log_debug "Skipping non-DM message type: $msg_type"
  exit 0
fi

# If no recipient specified, nothing to check
if [[ -z "$recipient" ]]; then
  log_debug "No recipient specified, skipping"
  exit 0
fi

# If the roster script doesn't exist, skip silently
if [[ ! -x "$ROSTER_SCRIPT" ]]; then
  log_debug "Roster script not found or not executable: $ROSTER_SCRIPT"
  exit 0
fi

# If no roster file exists for this team, skip silently (roster not initialized)
roster_file="${HOME}/.claude/teams/${TEAM_NAME}/squads.json"
if [[ ! -f "$roster_file" ]]; then
  log_debug "No roster file found at $roster_file, skipping"
  exit 0
fi

# Look up sender and recipient squads
sender_squad="$("$ROSTER_SCRIPT" get-squad "$TEAM_NAME" "$SENDER_NAME" 2>/dev/null || echo "")"
recipient_squad="$("$ROSTER_SCRIPT" get-squad "$TEAM_NAME" "$recipient" 2>/dev/null || echo "")"

log_debug "Sender squad=$sender_squad, Recipient squad=$recipient_squad"

# If either agent is unassigned (no squad), no boundary to cross
if [[ -z "$sender_squad" ]] || [[ -z "$recipient_squad" ]]; then
  log_debug "One or both agents have no squad assignment, skipping"
  exit 0
fi

# If they're in the same squad, all clear
if [[ "$sender_squad" == "$recipient_squad" ]]; then
  log_debug "Same squad ($sender_squad), no warning needed"
  exit 0
fi

# --- Cross-boundary detected ---
warning_msg="${SENDER_NAME} (squad: ${sender_squad}) -> ${recipient} (squad: ${recipient_squad})"
log_warning "$warning_msg"

# Print a user-visible notice. Claude Code surfaces stderr from hooks.
# This is advisory only — the message will still be sent.
cat >&2 <<EOF
[hierarchical-team-coordination] Cross-boundary message detected:
  From: ${SENDER_NAME} (squad: ${sender_squad})
  To:   ${recipient} (squad: ${recipient_squad})
  Tip:  Route cross-squad messages through the team-lead or squad-leader.
EOF

# CRITICAL: Always exit 0. Per ADR D5, boundaries are convention, not enforcement.
# Exit code 2 would block the message — we must never do that.
exit 0
