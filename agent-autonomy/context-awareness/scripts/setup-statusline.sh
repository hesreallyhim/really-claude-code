#!/usr/bin/env bash
# SessionStart hook: installs the context-awareness statusline wrapper.
#
# Strategy (Approach A — stable path):
#   1. Copy statusline-wrapper.sh from plugin root to a stable location
#      (~/.claude/context-awareness/statusline-wrapper.sh) so it survives
#      plugin cache changes and version upgrades.
#   2. Patch the user's statusline in ~/.claude/settings.json (global) to
#      tee stdin to the wrapper while preserving any existing statusline command.
#
# Idempotent — exits silently if already configured.
# The wrapper is guarded with `test -x` so it's a no-op if the file is removed.

set -euo pipefail

# --- Prerequisites -----------------------------------------------------------

if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-}"
if [[ -z "$PLUGIN_ROOT" ]]; then
  exit 0
fi

SOURCE_WRAPPER="${PLUGIN_ROOT}/scripts/statusline-wrapper.sh"
if [[ ! -f "$SOURCE_WRAPPER" ]]; then
  exit 0
fi

# --- Stable install location --------------------------------------------------

STABLE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-awareness"
STABLE_WRAPPER="${STABLE_DIR}/statusline-wrapper.sh"

mkdir -p "$STABLE_DIR"

# Always copy (picks up upgrades); preserve executable bit
cp "$SOURCE_WRAPPER" "$STABLE_WRAPPER"
chmod +x "$STABLE_WRAPPER"

# --- Patch statusline in user settings ----------------------------------------

USER_SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

# Guard: already configured?
if [[ -f "$USER_SETTINGS" ]] && grep -q "context-awareness/statusline-wrapper.sh" "$USER_SETTINGS" 2>/dev/null; then
  exit 0
fi

# Read existing settings
if [[ -f "$USER_SETTINGS" ]]; then
  EXISTING="$(cat "$USER_SETTINGS")"
else
  EXISTING="{}"
fi

# Extract existing statusline command and padding (if any)
EXISTING_CMD="$(echo "$EXISTING" | jq -r '.statusLine.command // empty' 2>/dev/null || true)"
EXISTING_PADDING="$(echo "$EXISTING" | jq '.statusLine.padding // null' 2>/dev/null || true)"

# Build the new statusline command.
# POSIX sh-compatible — no bash process substitution (>(...)) since Claude Code
# may run statusline commands with /bin/sh.
# Strategy: read stdin into a variable, feed it to the wrapper first, then to
# the existing statusline command.
WRAPPER_CALL="test -x \"${STABLE_WRAPPER}\" && \"${STABLE_WRAPPER}\" >/dev/null 2>&1 || true"

if [[ -n "$EXISTING_CMD" ]]; then
  # Preserve existing statusline: feed stdin to wrapper, then to original command
  NEW_CMD="INPUT=\$(cat); printf '%s' \"\$INPUT\" | (${WRAPPER_CALL}); printf '%s' \"\$INPUT\" | ${EXISTING_CMD}"
else
  # No existing statusline — just run the wrapper (consume stdin silently)
  NEW_CMD="INPUT=\$(cat); printf '%s' \"\$INPUT\" | (${WRAPPER_CALL})"
fi

# Merge into settings, preserving all other keys and existing padding
if [[ "$EXISTING_PADDING" != "null" ]]; then
  echo "$EXISTING" | jq --arg cmd "$NEW_CMD" --argjson pad "$EXISTING_PADDING" \
    '.statusLine = {"type": "command", "command": $cmd, "padding": $pad}' > "${USER_SETTINGS}.tmp"
else
  echo "$EXISTING" | jq --arg cmd "$NEW_CMD" \
    '.statusLine = {"type": "command", "command": $cmd}' > "${USER_SETTINGS}.tmp"
fi
mv "${USER_SETTINGS}.tmp" "$USER_SETTINGS"

exit 0
