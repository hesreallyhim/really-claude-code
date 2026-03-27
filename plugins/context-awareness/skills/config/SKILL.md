---
name: config
description: View or change context-awareness plugin configuration. Use this when the user asks to configure the settings for the context-awareness plugin, or when they ask to view the current configuration.
user-invocable: true
argument-hint: "[show|change]"
---

# Context-Awareness Configuration

Manage the context-awareness plugin configuration. The config controls which
data providers are active (context window, cost, rate limits), effort mode,
and which guidelines are injected at session start.

## Config locations

- **Defaults**: `${CLAUDE_PLUGIN_ROOT}/defaults/config.yaml`
- **User overrides**: `${CLAUDE_PLUGIN_DATA}/config.yaml`
- **Effort mode** (session-scoped): stored in the session tracking file at
  `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-awareness/state/session-*-tracking.json`

The user config takes precedence. If it doesn't exist, defaults apply.

## Instructions

### Determine the subcommand

- No argument or `show` → **show** the current configuration
- `change` → **prompt the user** for what they want to change

### show

1. Check if `${CLAUDE_PLUGIN_DATA}/config.yaml` exists.
   - If yes, read it — this is the active config.
   - If no, read `${CLAUDE_PLUGIN_ROOT}/defaults/config.yaml` — note that
     defaults are active.

2. Present the config to the user in a readable format. For each provider, show:
   - Whether it's enabled or disabled
   - Its current parameters (e.g., `session_budget: 5.00`)
   - A one-line description of what it does

3. Show the current effort mode by reading the most recent tracking file:
   ```bash
   ls -t ${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-awareness/state/session-*-tracking.json | head -1
   ```
   Display the `effort_mode` value (`off`, `adaptive`, or `planMode`).

4. Show the current guidelines setting (`default` or a custom path).

5. Mention that `/context-awareness:config change` can be used to modify settings.

### change

1. Read the current active config (user override if it exists, else defaults).

2. Use **AskUserQuestion** to ask the user what they'd like to change. Offer
   clear options, for example:

   > What would you like to change?
   >
   > - Enable/disable a provider (context, cost, rate_limits)
   > - Set a session budget for cost tracking
   > - Cycle effort mode (off → adaptive → planMode → off)
   > - Use custom guidelines (provide a file path)
   > - Reset to defaults

3. Apply the requested changes:
   - **Provider/guidelines changes**: read the current user config (or copy
     defaults if none exists), modify the relevant fields, write to
     `${CLAUDE_PLUGIN_DATA}/config.yaml`.
   - **Effort mode changes**: read the current session's tracking file,
     cycle to the next mode (`off` → `adaptive` → `planMode` → `off`),
     update `effort_mode` in the JSON (preserve all other fields), write back.

4. Confirm what changed and show the updated value.

5. Note: provider and guideline changes take effect on the **next session
   start** (when hooks re-read the config). Effort mode changes take effect
   immediately.

## Effort modes

| Mode | Behavior |
|------|----------|
| `off` | No autonomous effort adjustment. Thinking effort stays wherever the user set it. |
| `adaptive` | Automatically downshift thinking effort as context pressure increases (medium at 50%, low at 70%). |
| `planMode` | High effort for planning and reasoning, low/medium for execution. |

## Example config

See `references/example-config.yaml` for a ready-to-use config with all
providers enabled and a $5 session budget. When helping the user set up
their config for the first time, offer to copy this example as a starting point.

## Provider reference

| Provider | Field | Description |
|----------|-------|-------------|
| `context` | `enabled` | Track context window usage percentage |
| `cost` | `enabled` | Track session spend in USD |
| `cost` | `session_budget` | Budget cap in USD (required when enabled) |
| `rate_limits` | `enabled` | Track 5-hour and 7-day API rate limit usage |

## Validation

- `session_budget` must be a positive number when cost provider is enabled.
- `guidelines` must be `"default"` or a valid file path.
- If validation fails, explain the issue and do not write an invalid config.
