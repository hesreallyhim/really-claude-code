---
name: publish
description: Publish a message to a pub/sub topic via the pub-sub-relayer
argument-hint: [topic] [message]
---

<!--
Usage: /publish <topic-name> message text
Example: /publish build-events Build succeeded for commit abc123. Artifacts at dist/.
Example: /publish schema-changes The users table now has a `role` column (enum: admin, member, guest).
Requires: pub-sub-relayer agent (spawned automatically if not already present)
-->

# /publish: Publish a Message to a Pub/Sub Topic

## Overview

This command publishes a message to a topic via the `pub-sub-relayer` agent. The relayer looks up all subscribers of the topic from its channel registry and forwards the message to each of them. The publisher does not need to know who is subscribed.

## Arguments

The argument format is: `$ARGUMENTS`

Expected format: `<topic-name> message text`

The first token is the topic name. Everything after it is the message body.

Examples:
- `/publish build-events Build succeeded for commit abc123. Artifacts at dist/.`
- `/publish schema-changes The users table now has a role column (enum: admin, member, guest).`
- `/publish errors Test suite failed: 3 failures in auth module. See test-results for details.`
- `/publish deploy-status Production deploy of v2.1.0 complete. All health checks passing.`

If no arguments are provided, ask the user for the topic and message before proceeding.

## Execution Steps

### Step 1: Parse the Arguments

Extract two components from `$ARGUMENTS`:

1. **Topic** -- the first whitespace-delimited token
2. **Message** -- everything after the topic, trimmed of leading whitespace

If only a topic is provided with no message body, ask the user what message to publish.

### Step 2: Ensure the Pub/Sub Relayer is Available

Check if a `pub-sub-relayer` agent is already part of the current team. If not, spawn one:

- Agent: `pub-sub-relayer` (from `${CLAUDE_PLUGIN_ROOT}/agents/pub-sub-relayer.md`)
- Model: haiku
- Tools: `["SendMessage", "Read", "Write"]`
- Role: Stateless pub/sub message relay
- Initial instructions must include the resolved registry path: `${CLAUDE_PLUGIN_ROOT}/state/pubsub-channels.json`

### Step 3: Format and Send the Publish Request

Determine the sender name. The sender is **you** (the agent executing this command). Use your agent name (typically `team-lead` if you are the main session).

Send a message to the `pub-sub-relayer` agent with this exact format:

```
PUBLISH <topic-name>
[FROM: <your-agent-name>]
---
<message body>
```

For example, if the user ran `/publish build-events Build succeeded for abc123`, send:

```
PUBLISH build-events
[FROM: team-lead]
---
Build succeeded for abc123
```

### Step 4: Confirm Delivery

The pub-sub-relayer will:
1. Read the channel registry to look up subscribers for the topic
2. Forward the message individually to each subscriber (skipping the sender if subscribed)
3. Send a delivery confirmation back to you

Possible confirmations:
- `Published to topic: build-events / Delivered to: tester, deployer, team-lead`
- `No subscribers for topic: build-events. Message not delivered.`

Report the confirmation to the user. If the topic has no subscribers, suggest using `/publish` after setting up subscriptions (via the pub-sub-relayer's SUBSCRIBE command).

## Pub/Sub Protocol (Reference)

### Publish request format (sender -> pub-sub-relayer):

```
PUBLISH topic-name
[FROM: sender-name]
---
Message body here.
```

### Forwarded message format (pub-sub-relayer -> each subscriber):

```
[FROM: sender-name] (via pub-sub-relayer, topic: topic-name)
---
Message body here.
```

### Delivery confirmation (pub-sub-relayer -> sender):

```
Published to topic: topic-name
Delivered to: subscriber-1, subscriber-2
```

If no subscribers:
```
No subscribers for topic: topic-name. Message not delivered.
```

## Error Handling

- **No pub-sub-relayer available and spawn fails:** Report the error to the user. Unlike the announcer, there is no simple fallback since the publisher does not know who is subscribed.
- **Topic does not exist:** The relayer will report `No subscribers for topic: <name>`. Inform the user.
- **Empty message body:** Ask the user what message to publish.
- **Registry file missing:** The relayer will recreate it with `{"channels": {}}`. The publish will report no subscribers.

## Notes

- The pub-sub-relayer is a haiku-model agent with access to `SendMessage`, `Read`, and `Write`. It needs file access to read and update the channel registry.
- Subscriptions are managed by sending SUBSCRIBE/UNSUBSCRIBE requests directly to the pub-sub-relayer, not through this command. This command only handles publishing.
- The relayer reads the registry fresh before each publish -- subscriber lists are never cached.
- The channel registry lives at `${CLAUDE_PLUGIN_ROOT}/state/pubsub-channels.json`. See `pubsub.example.jsonc` in the same directory for a documented example.
