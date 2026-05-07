#!/usr/bin/env bash
# scan-agents.sh
#
# Scans ~/.claude/agents/ and outputs a table of installed agents with their
# name, model tier, and description (first 80 chars).
#
# Part of the team-patterns skill for Claude Code agent team design.
#
# Usage:
#   bash scan-agents.sh
#   bash scan-agents.sh --json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_DIR="$HOME/.claude/agents"

if [ ! -d "$AGENTS_DIR" ]; then
    echo "Error: Agents directory not found at $AGENTS_DIR" >&2
    exit 1
fi

json_mode=false
if [ "$1" = "--json" ]; then
    json_mode=true
fi

# Parse frontmatter from a markdown file
# Extracts name, model, and description fields
parse_agent() {
    local file="$1"
    local name="" model="" description="" in_frontmatter=false

    while IFS= read -r line; do
        if [ "$line" = "---" ]; then
            if $in_frontmatter; then
                break
            else
                in_frontmatter=true
                continue
            fi
        fi
        if $in_frontmatter; then
            case "$line" in
                name:*)
                    name="${line#name:}"
                    name="${name## }"
                    ;;
                model:*)
                    model="${line#model:}"
                    model="${model## }"
                    ;;
                description:*)
                    description="${line#description:}"
                    description="${description## }"
                    ;;
            esac
        fi
    done < "$file"

    # Fallback: derive name from filename if not in frontmatter
    if [ -z "$name" ]; then
        name="$(basename "$file" .md)"
    fi

    # Default model if not specified
    if [ -z "$model" ]; then
        model="(default)"
    fi

    # Truncate description to 80 chars
    if [ ${#description} -gt 80 ]; then
        description="${description:0:77}..."
    fi

    echo "$name|$model|$description"
}

# Collect all .md files recursively
agent_files=()
while IFS= read -r -d '' file; do
    agent_files+=("$file")
done < <(find "$AGENTS_DIR" -name "*.md" -type f -print0 | sort -z)

if [ ${#agent_files[@]} -eq 0 ]; then
    echo "No agent files found in $AGENTS_DIR"
    exit 0
fi

if $json_mode; then
    echo "["
    first=true
    for file in "${agent_files[@]}"; do
        IFS='|' read -r name model desc <<< "$(parse_agent "$file")"
        if $first; then
            first=false
        else
            echo ","
        fi
        # Escape quotes in description for JSON
        desc="${desc//\"/\\\"}"
        printf '  {"name": "%s", "model": "%s", "description": "%s", "file": "%s"}' \
            "$name" "$model" "$desc" "$file"
    done
    echo ""
    echo "]"
else
    # Print table header
    printf "%-35s %-12s %s\n" "AGENT NAME" "MODEL" "DESCRIPTION"
    printf "%-35s %-12s %s\n" "-----------------------------------" "------------" "$(printf '%0.s-' {1..80})"

    for file in "${agent_files[@]}"; do
        IFS='|' read -r name model desc <<< "$(parse_agent "$file")"
        printf "%-35s %-12s %s\n" "$name" "$model" "$desc"
    done

    echo ""
    echo "Total agents: ${#agent_files[@]}"
fi
