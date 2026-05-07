#!/usr/bin/env bash
# roster.sh
# Purpose: Utility script for reading/writing squad membership.
# Operates on squads.json at ~/.claude/teams/{team-name}/squads.json.
#
# Usage:
#   roster.sh [--quiet] <command> <team-name> [args...]
#
#   --quiet: Suppress errors for missing roster files. Returns empty output
#            and exits 0 instead of failing. Useful for hook scripts.
#
#   roster.sh get-squad <team-name> <agent-name>
#     Prints the squad name for the given agent, or "" if not found.
#
#   roster.sh set-squad <team-name> <agent-name> <squad-name>
#     Assigns an agent to a squad.
#
#   roster.sh remove <team-name> <agent-name>
#     Removes an agent from the roster.
#
#   roster.sh list <team-name> [squad-name]
#     Lists all agents (optionally filtered by squad).
#
#   roster.sh same-squad <team-name> <agent-a> <agent-b>
#     Exits 0 if both agents are in the same squad, 1 otherwise.
#
#   roster.sh init <team-name>
#     Creates an empty squads.json if it does not exist.
#
# File format (squads.json):
#   {
#     "squads": {
#       "backend": ["api-eng", "data-eng", "review-gate"],
#       "frontend": ["ui-eng", "state-eng"]
#     },
#     "agents": {
#       "api-eng": "backend",
#       "data-eng": "backend",
#       "ui-eng": "frontend"
#     },
#     "unassigned": ["announcer"]
#   }
#
# The "agents" map is the authoritative lookup (agent -> squad).
# The "squads" map is the reverse index (squad -> [agents]).
# "unassigned" lists agents with no squad affiliation.
#
# Concurrency:
#   Write operations (set-squad, remove, init) acquire an exclusive flock
#   on a .lock file next to squads.json. This prevents concurrent writes
#   from clobbering each other. If flock is unavailable (some minimal
#   containers), writes proceed without locking and a warning is emitted.

set -euo pipefail

# ---------------------------------------------------------------------------
# Global options
# ---------------------------------------------------------------------------

# --quiet: Suppress errors for missing roster files (return empty instead of
# exit 1). Useful for hook scripts that call roster.sh and need graceful
# degradation when the roster hasn't been initialized yet.
QUIET=0
if [[ "${1:-}" == "--quiet" ]]; then
  QUIET=1
  shift
fi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

roster_dir() {
  local team_name="$1"
  echo "${HOME}/.claude/teams/${team_name}"
}

roster_file() {
  local team_name="$1"
  echo "$(roster_dir "$team_name")/squads.json"
}

ensure_jq() {
  if ! command -v jq &>/dev/null; then
    echo "ERROR: jq is required but not found in PATH" >&2
    exit 1
  fi
}

ensure_roster() {
  local file
  file="$(roster_file "$1")"
  if [[ ! -f "$file" ]]; then
    if [[ "$QUIET" == "1" ]]; then
      # In quiet mode, return empty output and exit 0 instead of failing
      exit 0
    fi
    echo "ERROR: Roster file not found: $file" >&2
    echo "Run: roster.sh init $1" >&2
    exit 1
  fi
}

# File descriptor used for flock. Chosen to avoid collision with stdin/out/err.
LOCK_FD=9
HAS_FLOCK=""

check_flock() {
  if [[ -z "$HAS_FLOCK" ]]; then
    if command -v flock &>/dev/null; then
      HAS_FLOCK="yes"
    else
      HAS_FLOCK="no"
    fi
  fi
}

# Acquire an exclusive lock for write operations.
# Usage: acquire_lock <team-name>
# The lock is held until the file descriptor is closed (script exit or
# explicit release). This prevents concurrent set-squad / remove calls
# from clobbering each other via the read-modify-write pattern.
acquire_lock() {
  local team_name="$1"
  local lock_file
  lock_file="$(roster_dir "$team_name")/squads.json.lock"

  check_flock
  if [[ "$HAS_FLOCK" == "yes" ]]; then
    mkdir -p "$(roster_dir "$team_name")"
    eval "exec ${LOCK_FD}>\"${lock_file}\""
    flock --timeout 5 "$LOCK_FD" || {
      echo "WARNING: Could not acquire roster lock within 5s, proceeding without lock" >&2
      return 0
    }
  else
    echo "WARNING: flock not available; concurrent roster writes may conflict" >&2
  fi
}

release_lock() {
  check_flock
  if [[ "$HAS_FLOCK" == "yes" ]]; then
    eval "exec ${LOCK_FD}>&-" 2>/dev/null || true
  fi
}

# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

cmd_init() {
  local team_name="$1"
  local dir file
  dir="$(roster_dir "$team_name")"
  file="$(roster_file "$team_name")"

  mkdir -p "$dir"
  acquire_lock "$team_name"
  if [[ ! -f "$file" ]]; then
    echo '{"squads":{},"agents":{},"unassigned":[]}' | jq '.' > "$file"
    echo "Created roster: $file"
  else
    echo "Roster already exists: $file"
  fi
  release_lock
}

cmd_get_squad() {
  local team_name="$1"
  local agent_name="$2"
  ensure_roster "$team_name"

  local file
  file="$(roster_file "$team_name")"
  local squad
  squad="$(jq -r --arg agent "$agent_name" '.agents[$agent] // ""' "$file")"
  echo "$squad"
}

cmd_set_squad() {
  local team_name="$1"
  local agent_name="$2"
  local squad_name="$3"
  ensure_roster "$team_name"

  local file
  file="$(roster_file "$team_name")"
  local tmp="${file}.tmp.$$"

  acquire_lock "$team_name"
  # Remove agent from any existing squad and from unassigned
  jq --arg agent "$agent_name" --arg squad "$squad_name" '
    # Remove from old squad (if any)
    .squads |= with_entries(
      .value |= map(select(. != $agent))
    )
    # Remove empty squads
    | .squads |= with_entries(select(.value | length > 0))
    # Remove from unassigned
    | .unassigned |= map(select(. != $agent))
    # Add to new squad
    | .squads[$squad] = ((.squads[$squad] // []) + [$agent] | unique)
    # Update agent -> squad mapping
    | .agents[$agent] = $squad
  ' "$file" > "$tmp" && mv "$tmp" "$file"
  release_lock

  echo "Assigned $agent_name -> $squad_name"
}

cmd_remove() {
  local team_name="$1"
  local agent_name="$2"
  ensure_roster "$team_name"

  local file
  file="$(roster_file "$team_name")"
  local tmp="${file}.tmp.$$"

  acquire_lock "$team_name"
  jq --arg agent "$agent_name" '
    # Remove from all squads
    .squads |= with_entries(
      .value |= map(select(. != $agent))
    )
    | .squads |= with_entries(select(.value | length > 0))
    # Remove from agents mapping
    | .agents |= del(.[$agent])
    # Remove from unassigned
    | .unassigned |= map(select(. != $agent))
  ' "$file" > "$tmp" && mv "$tmp" "$file"
  release_lock

  echo "Removed $agent_name from roster"
}

cmd_list() {
  local team_name="$1"
  local squad_filter="${2:-}"
  ensure_roster "$team_name"

  local file
  file="$(roster_file "$team_name")"

  if [[ -n "$squad_filter" ]]; then
    jq -r --arg squad "$squad_filter" '
      .squads[$squad] // [] | .[]
    ' "$file"
  else
    # Print all agents grouped by squad
    jq -r '
      "=== Squads ===",
      (.squads | to_entries[] | "\(.key): \(.value | join(", "))"),
      "",
      if (.unassigned | length) > 0
      then "=== Unassigned ===", (.unassigned | join(", "))
      else empty
      end
    ' "$file"
  fi
}

cmd_same_squad() {
  local team_name="$1"
  local agent_a="$2"
  local agent_b="$3"
  ensure_roster "$team_name"

  local file
  file="$(roster_file "$team_name")"

  local squad_a squad_b
  squad_a="$(jq -r --arg agent "$agent_a" '.agents[$agent] // ""' "$file")"
  squad_b="$(jq -r --arg agent "$agent_b" '.agents[$agent] // ""' "$file")"

  # If either agent has no squad, they are not in the same squad
  if [[ -z "$squad_a" ]] || [[ -z "$squad_b" ]]; then
    exit 1
  fi

  if [[ "$squad_a" == "$squad_b" ]]; then
    exit 0
  else
    exit 1
  fi
}

# ---------------------------------------------------------------------------
# Main dispatch
# ---------------------------------------------------------------------------

usage() {
  echo "Usage: roster.sh [--quiet] <command> <team-name> [args...]" >&2
  echo "" >&2
  echo "Options:" >&2
  echo "  --quiet    Suppress errors for missing roster; return empty and exit 0" >&2
  echo "" >&2
  echo "Commands:" >&2
  echo "  init       <team-name>                        Create empty roster" >&2
  echo "  get-squad  <team-name> <agent-name>           Get agent's squad" >&2
  echo "  set-squad  <team-name> <agent-name> <squad>   Assign agent to squad" >&2
  echo "  remove     <team-name> <agent-name>           Remove agent from roster" >&2
  echo "  list       <team-name> [squad-name]           List agents" >&2
  echo "  same-squad <team-name> <agent-a> <agent-b>    Check if same squad" >&2
  exit 1
}

ensure_jq

command="${1:-}"
shift || true

case "$command" in
  init)
    [[ $# -ge 1 ]] || usage
    cmd_init "$1"
    ;;
  get-squad)
    [[ $# -ge 2 ]] || usage
    cmd_get_squad "$1" "$2"
    ;;
  set-squad)
    [[ $# -ge 3 ]] || usage
    cmd_set_squad "$1" "$2" "$3"
    ;;
  remove)
    [[ $# -ge 2 ]] || usage
    cmd_remove "$1" "$2"
    ;;
  list)
    [[ $# -ge 1 ]] || usage
    cmd_list "$1" "${2:-}"
    ;;
  same-squad)
    [[ $# -ge 3 ]] || usage
    cmd_same_squad "$1" "$2" "$3"
    ;;
  *)
    usage
    ;;
esac
