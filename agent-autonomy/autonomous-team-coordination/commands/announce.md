---
name: announce
description: Send a message to multiple agents via the announcer
argument-hint: [recipients] [message]
---

<!--
Usage: /announce [recipient1, recipient2, ...] message text
Example: /announce [worker-1, worker-2, worker-3] The shared config schema has changed. Please re-validate.
Example: /announce [squad-leader-api, squad-leader-frontend] Status check: report progress and blockers.
Requires: announcer agent (spawned automatically if not already present)
-->

# /announce: Send a Multi-Recipient Message via Announcer

## Overview

This command provides a shortcut for sending a message to multiple agents through the `announcer` agent (the stateless multi-send relay). Instead of manually formatting the announcer protocol headers, this command parses a natural argument format and sends the properly formatted relay request.

## Arguments

The argument format is: `$ARGUMENTS`

Expected format: `[recipient1, recipient2, ...] message text`

Examples:
- `/announce [worker-1, worker-2, worker-3] The shared config schema has changed. Please re-validate.`
- `/announce [squad-leader-api, squad-leader-frontend] Status check: report progress and blockers.`
- `/announce [api-eng, db-eng] Integration tests are passing. You may proceed with deployment.`

If no arguments are provided, ask the user for the recipient list and message before proceeding.

## Execution Steps

### Step 1: Parse the Arguments

Extract two components from `$ARGUMENTS`:

1. **Recipients** -- the comma-separated list inside square brackets `[...]`
2. **Message** -- everything after the closing bracket `]`, trimmed of leading whitespace

If the argument does not contain square brackets, attempt a best-effort parse:
- If the first word(s) look like agent names (lowercase, hyphenated), treat them as recipients (comma or space separated) and the rest as the message body.
- If parsing is ambiguous, ask the user to clarify using the bracket format.

### Step 2: Ensure the Announcer is Available

Check if an `announcer` agent is already part of the current team. If not, spawn one:

- Agent: `announcer` (from `${CLAUDE_PLUGIN_ROOT}/agents/announcer.md`)
- Model: haiku
- Tools: `["SendMessage"]` only
- Role: Stateless multi-send relay

### Step 3: Format and Send the Relay Request

Determine the sender name. The sender is **you** (the agent executing this command). Use your agent name (typically `team-lead` if you are the main session).

Send a message to the `announcer` agent with this exact format:

```
[TO: recipient-1, recipient-2, recipient-3]
[FROM: <your-agent-name>]
---
<message body>
```

For example, if the user ran `/announce [worker-1, worker-2] Please commit your work`, send:

```
[TO: worker-1, worker-2]
[FROM: team-lead]
---
Please commit your work
```

### Step 4: Confirm Delivery

The announcer will:
1. Forward the message individually to each recipient with `[FROM: <sender>] (via announcer)` attribution
2. Send a delivery confirmation back to you: `Delivered to: recipient-1, recipient-2`

Report the delivery confirmation to the user. If any deliveries failed, report the failures.

## Announcer Message Protocol (Reference)

### Relay request format (sender -> announcer):

```
[TO: recipient-1, recipient-2, recipient-3]
[FROM: sender-name]
---
Message body here.
```

### Forwarded message format (announcer -> each recipient):

```
[FROM: sender-name] (via announcer)
---
Message body here.
```

### Delivery confirmation (announcer -> sender):

```
Delivered to: recipient-1, recipient-2, recipient-3
```

If delivery failed for any recipient:
```
Delivered to: recipient-1, recipient-3
Failed: recipient-2 (reason)
```

## Error Handling

- **No announcer available and spawn fails:** Fall back to sending individual `SendMessage` calls directly to each recipient. Prefix each message with `[FROM: <your-agent-name>]` for consistency.
- **Invalid recipient names:** Send the relay request anyway. The announcer will attempt delivery and report failures. You do not need to validate recipient names.
- **Empty message body:** Ask the user what message to send.
- **Single recipient:** The announcer works fine with a single recipient, but note to the user that a direct `SendMessage` would be more efficient.

## Notes

- The announcer is a haiku-model agent restricted to the `SendMessage` tool only. It does not read, interpret, or modify message content.
- Any agent can use the announcer, not just the team-lead. This command is a convenience for the team-lead, but agents can send relay requests directly by messaging the announcer with the protocol format.
- The announcer processes one relay request at a time. If you need to send multiple different messages to different groups, send them sequentially.
- This command does not create tasks or track delivery history. It is a fire-and-forget relay.
