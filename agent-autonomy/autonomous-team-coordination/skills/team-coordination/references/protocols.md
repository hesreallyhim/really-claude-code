# Protocol Reference: Hierarchical Team Coordination

Detailed specifications for the three communication protocols used in hierarchical team coordination.

---

## 1. Spawn Request Protocol

**Sender:** squad-leader
**Receiver:** team-lead
**Purpose:** Request the team-lead to create worker agents for a task.

### Format

```
SPAWN REQUEST
=============
Task: [brief task description]
Pattern: [selected pattern name]
Topology: [communication topology]
Design phase: [FULL | SHORT-CIRCUITED -- reason]

AGENTS REQUESTED:
1. Name: [agent-name]
   Type: [existing agent type]
   Model: [opus/sonnet/haiku]
   Role: [one-sentence description]

2. Name: [agent-name]
   Type: [existing agent type]
   Model: [opus/sonnet/haiku]
   Role: [one-sentence description]

[...]

SKILLS NEEDED:
- Existing: [skill-name] -> assigned to [agent-name]
- Missing: [skill-name] -> [brief spec or "create with skill-creator-enhanced"]

TASK GRAPH:
Task 1: [description] -> Owner: [agent-name]
Task 2: [description] -> Owner: [agent-name] (blocked by: 1)
Task 3: [description] -> Owner: [agent-name] (parallel with: 2)
[...]

READY TO PROCEED: [YES | NO -- reason]
```

### Field Specifications

#### Header Section

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| Task | Yes | Free text, one sentence | Brief description of the overall task |
| Pattern | Yes | Pattern name from team-patterns skill | The team pattern selected for this task (e.g., "Supervisor-Worker with Reflection Loop", "Pipeline", "Fan-Out/Fan-In") |
| Topology | Yes | `hub-and-spoke`, `pipeline`, `mesh`, `tree`, `star`, `adversarial` | Communication topology for the sub-team |
| Design phase | Yes | `FULL` or `SHORT-CIRCUITED -- [reason]` | Whether the squad-leader consulted the team-architect and skill-identifier, or skipped the design phase |

#### AGENTS REQUESTED Section

Each agent entry has four fields:

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| Name | Yes | Lowercase, hyphenated, descriptive (e.g., `api-implementer`) | Unique name within the team |
| Type | Yes | An agent type from `~/.claude/agents/` (e.g., `independent-contributor`) | Existing agent definition to use |
| Model | Yes | `opus`, `sonnet`, or `haiku` | Model tier with brief rationale |
| Role | Yes | One sentence | What this agent does in the context of this task |

**Naming rules:**
- Agent names must be unique within the team.
- Use lowercase with hyphens (e.g., `backend-api-worker`, not `BackendApiWorker`).
- Names should be descriptive of the agent's role in this specific task.

**Model selection guidance:**
- `opus` -- Complex reasoning, coordination, architecture decisions.
- `sonnet` -- Standard implementation, code writing, analysis.
- `haiku` -- Simple/repetitive tasks, relay, formatting.

#### SKILLS NEEDED Section

Each line starts with `Existing:` or `Missing:`:

- **Existing:** `[skill-name] -> assigned to [agent-name]` -- An installed skill mapped to a specific agent.
- **Missing:** `[skill-name] -> [brief spec]` -- A skill that does not exist yet. Include either a one-sentence spec or `"create with skill-creator-enhanced"`.

#### TASK GRAPH Section

Each line follows the format:

```
Task N: [description] -> Owner: [agent-name]
Task N: [description] -> Owner: [agent-name] (blocked by: M)
Task N: [description] -> Owner: [agent-name] (parallel with: M)
```

Dependency annotations:
- `(blocked by: N)` -- Cannot start until Task N completes.
- `(blocked by: N, M)` -- Cannot start until both Task N and Task M complete.
- `(parallel with: N)` -- Can run concurrently with Task N (informational, not a constraint).

#### READY TO PROCEED

- `YES` -- All agents and skills are available or can be created. The team-lead can proceed with spawning.
- `NO -- [reason]` -- Something prevents execution. Examples: "critical skill X is missing and cannot be auto-created", "task requires an agent type that does not exist".

### Short-Circuit Criteria

The squad-leader may skip the full design phase (consulting team-architect and skill-identifier) when ALL of the following are true:

1. The task maps to a single, well-known pattern (e.g., critic-reviser loop, simple pipeline).
2. Requires 3 or fewer worker agents.
3. No skill gaps are expected -- standard agent types suffice.
4. The communication topology is obvious.

When short-circuiting, set `Design phase: SHORT-CIRCUITED -- [reason]`, for example:

```
Design phase: SHORT-CIRCUITED -- well-known critic-reviser pattern, 2 agents, no skill gaps
```

### Example: Full Design Phase

```
SPAWN REQUEST
=============
Task: Refactor authentication module from session-based to JWT
Pattern: Cross-functional Squad with Reflection Loop
Topology: hub-and-spoke
Design phase: FULL

AGENTS REQUESTED:
1. Name: auth-implementer
   Type: independent-contributor
   Model: sonnet
   Role: Implements JWT auth middleware and token management

2. Name: test-writer
   Type: testing-expert
   Model: sonnet
   Role: Writes unit and integration tests for auth changes

3. Name: auth-reviewer
   Type: critical-code-reviewer
   Model: opus
   Role: Reviews all auth code for security vulnerabilities

SKILLS NEEDED:
- Existing: team-patterns -> squad-leader (for coordination)
- Existing: webapp-testing -> test-writer
- Missing: jwt-security-patterns -> auth-reviewer (common JWT pitfalls and best practices)

TASK GRAPH:
Task 1: Remove session middleware, add JWT signing -> Owner: auth-implementer
Task 2: Write unit tests for token generation -> Owner: test-writer (parallel with: 1)
Task 3: Security review of JWT implementation -> Owner: auth-reviewer (blocked by: 1)
Task 4: Write integration tests for auth flow -> Owner: test-writer (blocked by: 1, 3)
Task 5: Final security sign-off -> Owner: auth-reviewer (blocked by: 4)

READY TO PROCEED: YES
```

### Example: Short-Circuited Design Phase

```
SPAWN REQUEST
=============
Task: Review and improve API documentation
Pattern: Critic-Reviser Loop
Topology: point-to-point
Design phase: SHORT-CIRCUITED -- well-known 2-agent pattern, no skill gaps, obvious topology

AGENTS REQUESTED:
1. Name: doc-writer
   Type: document-maintainer
   Model: sonnet
   Role: Revises API documentation based on reviewer feedback

2. Name: doc-critic
   Type: critical-code-reviewer
   Model: opus
   Role: Reviews documentation for accuracy, completeness, and clarity

SKILLS NEEDED:
- Existing: documentation-expert -> doc-writer

TASK GRAPH:
Task 1: Initial documentation revision -> Owner: doc-writer
Task 2: Review round 1 -> Owner: doc-critic (blocked by: 1)
Task 3: Address review feedback -> Owner: doc-writer (blocked by: 2)
Task 4: Review round 2 (final) -> Owner: doc-critic (blocked by: 3)

READY TO PROCEED: YES
```

---

## 2. Completion Report Protocol

**Sender:** squad-leader
**Receiver:** team-lead
**Purpose:** Report the outcome of a delegated task after all work is done.

### Format

```
COMPLETION REPORT
=================
Task: [original task description]
Status: [COMPLETE | PARTIAL -- explanation]

Summary:
[2-5 sentences describing what was accomplished]

Artifacts:
- [key files created/modified]

Agents Used:
- [agent-name]: [what they accomplished]

Issues:
- [unresolved problems, or "None"]

Recommendations:
- [follow-up work, or "None"]
```

### Field Specifications

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| Task | Yes | Free text | The original task description, matching what was in the spawn request |
| Status | Yes | `COMPLETE` or `PARTIAL -- [explanation]` | Whether all work was finished |
| Summary | Yes | 2-5 sentences | What was accomplished at a high level |
| Artifacts | Yes | Bulleted list of file paths | Key files and directories created or modified |
| Agents Used | Yes | Bulleted list of `[name]: [accomplishment]` | What each agent contributed |
| Issues | Yes | Bulleted list or `"None"` | Unresolved problems that the team-lead should know about |
| Recommendations | Yes | Bulleted list or `"None"` | Suggested follow-up work |

### Status Values

- **COMPLETE** -- All tasks in the task graph were completed successfully. All acceptance criteria met.
- **PARTIAL -- [explanation]** -- Some tasks were not completed. The explanation must state what is incomplete and why. Examples:
  - `PARTIAL -- Task 4 (integration tests) blocked by unresolved API contract disagreement`
  - `PARTIAL -- auth-reviewer agent context filled before final review round`

### Example: Complete

```
COMPLETION REPORT
=================
Task: Refactor authentication module from session-based to JWT
Status: COMPLETE

Summary:
Replaced session-based authentication with JWT tokens across all API endpoints.
Token generation uses RS256 signing with 15-minute expiry and refresh token rotation.
All existing tests updated and 12 new integration tests added covering token lifecycle.

Artifacts:
- src/middleware/jwt-auth.ts (new)
- src/services/token-manager.ts (new)
- src/middleware/session-auth.ts (deleted)
- tests/integration/auth-flow.test.ts (updated, +12 tests)
- docs/api/authentication.md (updated)

Agents Used:
- auth-implementer: Built JWT middleware, token manager, and migration script
- test-writer: Wrote 12 integration tests and updated 8 existing unit tests
- auth-reviewer: Reviewed 4 PRs, identified and resolved 2 token expiry edge cases

Issues:
- None

Recommendations:
- Add rate limiting to the token refresh endpoint
- Consider Redis-backed token blacklist for immediate revocation support
```

### Example: Partial

```
COMPLETION REPORT
=================
Task: Build data pipeline for analytics dashboard
Status: PARTIAL -- ETL pipeline complete but dashboard UI blocked by missing design spec

Summary:
Built the ETL pipeline that extracts from PostgreSQL, transforms via dbt models, and loads
into the analytics warehouse. Dashboard frontend was started but could not be completed
because no design spec exists for the visualization layout.

Artifacts:
- etl/extract.py (new)
- etl/transform/models/ (new, 6 dbt models)
- etl/load.py (new)
- dashboard/src/App.tsx (partial -- skeleton only)

Agents Used:
- etl-engineer: Built complete extract-transform-load pipeline with error handling
- dashboard-dev: Created project skeleton but blocked on missing design spec
- data-reviewer: Validated ETL output accuracy against source data

Issues:
- Dashboard UI incomplete -- needs design specification from product team
- dbt model for user_sessions has a known 3-second latency on large datasets

Recommendations:
- Obtain dashboard design spec and spawn a new squad for the UI work
- Optimize user_sessions dbt model with incremental materialization
```

---

## 3. Announcer Protocol

**Sender:** any agent
**Receiver:** announcer agent
**Purpose:** Fan out a single message to multiple named recipients.

### Relay Request Format

Sent by any agent to the announcer:

```
[TO: recipient-1, recipient-2, recipient-3]
[FROM: sender-name]
---
Message body here.
Multiple lines are fine.
```

### Field Specifications

| Field | Required | Format | Description |
|-------|----------|--------|-------------|
| TO | Yes | `[TO: name1, name2, ...]` | Comma-separated list of recipient agent names. Whitespace around names is trimmed. |
| FROM | Yes | `[FROM: sender-name]` | The name of the agent sending the message. Used for attribution in forwarded messages. |
| Separator | Yes | `---` | Three hyphens on a line by themselves, separating headers from body. |
| Body | Yes | Free text, one or more lines | The message content. Forwarded exactly as-is, with no modification. |

### Forwarded Message Format

The announcer sends to each recipient:

```
[FROM: sender-name] (via announcer)
---
Message body here.
Multiple lines are fine.
```

The `(via announcer)` suffix indicates the message was relayed, not sent directly. The body is forwarded verbatim.

### Delivery Confirmation

After forwarding to all recipients, the announcer sends back to the original sender:

```
Delivered to: recipient-1, recipient-2, recipient-3
```

If any delivery failed:

```
Delivered to: recipient-1, recipient-3
Failed: recipient-2 (agent not found)
```

### Error Handling

If the incoming message does not match the expected format (missing `[TO: ...]`, missing `[FROM: ...]`, or missing `---` separator), the announcer sends the message back to the sender with:

```
Could not parse relay request. Expected format:
[TO: ...]
[FROM: ...]
---
Body
```

### Rules

1. The announcer **never** reads, interprets, summarizes, or responds to message content. It is a dumb pipe.
2. The announcer **never** modifies the message body. It forwards exactly as received.
3. The announcer **never** decides who should receive a message. The sender's `[TO: ...]` list is authoritative.
4. The announcer **never** engages in conversation beyond parse-forward-confirm.
5. If a recipient name looks unusual, the announcer attempts delivery anyway and reports errors after the fact.
6. One relay request is processed at a time. All deliveries and the confirmation are completed before handling the next incoming message.

### Example: Squad-Leader Briefing Workers

Squad-leader sends to announcer:

```
[TO: api-worker, db-worker, test-writer]
[FROM: squad-leader-backend]
---
Sprint kickoff: the shared API contract is in docs/api-spec.yaml.
Your individual task assignments are in the task list.
Please start with your unblocked tasks and message me if you hit any issues.
```

Announcer forwards to `api-worker`:

```
[FROM: squad-leader-backend] (via announcer)
---
Sprint kickoff: the shared API contract is in docs/api-spec.yaml.
Your individual task assignments are in the task list.
Please start with your unblocked tasks and message me if you hit any issues.
```

(Same message forwarded to `db-worker` and `test-writer`.)

Announcer confirms to `squad-leader-backend`:

```
Delivered to: api-worker, db-worker, test-writer
```

### Example: Peer-to-Peer Notification

A worker notifies peers about a breaking change:

```
[TO: api-worker, db-worker]
[FROM: auth-worker]
---
Auth token format changed from JWT to opaque tokens.
Update your integration tests to use the new token format.
See src/auth/token.ts for the new interface.
```

### Example: Team-Lead Status Request

The team-lead checks on specific squads:

```
[TO: squad-leader-api, squad-leader-frontend]
[FROM: team-lead]
---
Status check: please report your squad's current progress and any blockers.
```

---

## 4. Pub/Sub Relayer Protocol

**Sender:** any agent
**Receiver:** pub-sub-relayer agent
**Purpose:** Topic-based message routing via a file-backed channel registry, decoupling publishers from subscribers.

### Registry File

The pub-sub-relayer manages a JSON registry file at `${CLAUDE_PLUGIN_ROOT}/state/pubsub-channels.json`.

```json
{
  "channels": {
    "build-events": ["tester", "deployer"],
    "code-changes": ["reviewer", "tester", "docs-writer"],
    "errors": ["debugger", "team-lead"]
  }
}
```

The registry is the single source of truth for subscriptions. The relay reads it fresh before every PUBLISH operation and writes it on every SUBSCRIBE/UNSUBSCRIBE.

### PUBLISH Format

Sent by any agent to the pub-sub-relayer:

```
PUBLISH topic-name
[FROM: sender-name]
---
Message body here.
Multiple lines are fine.
```

#### Field Specifications

| Field | Required | Format | Description |
|-------|----------|--------|-------------|
| PUBLISH | Yes | `PUBLISH topic-name` | First line. The topic/channel to publish to. |
| FROM | Yes | `[FROM: sender-name]` | The name of the publishing agent. |
| Separator | Yes | `---` | Three hyphens, separating headers from body. |
| Body | Yes | Free text, one or more lines | The message content. Forwarded exactly as-is. |

#### Forwarded Message Format

The pub-sub-relayer sends to each subscriber:

```
[FROM: sender-name] (via pub-sub-relayer, topic: topic-name)
---
Message body here.
Multiple lines are fine.
```

The `(via pub-sub-relayer, topic: topic-name)` suffix indicates the message was routed by topic, not sent directly. The body is forwarded verbatim.

#### Delivery Confirmation

After forwarding to all subscribers, the pub-sub-relayer sends back to the publisher:

```
Published to topic: topic-name
Delivered to: subscriber-1, subscriber-2, subscriber-3
```

If any delivery failed:

```
Published to topic: topic-name
Delivered to: subscriber-1, subscriber-3
Failed: subscriber-2 (agent not found)
```

If no subscribers exist for the topic:

```
No subscribers for topic: topic-name. Message not delivered.
```

### SUBSCRIBE Format

```
SUBSCRIBE topic-name
[AGENT: agent-name]
```

| Field | Required | Format | Description |
|-------|----------|--------|-------------|
| SUBSCRIBE | Yes | `SUBSCRIBE topic-name` | First line. The topic/channel to subscribe to. |
| AGENT | Yes | `[AGENT: agent-name]` | The agent to add to the subscriber list. |

#### Confirmation

```
Subscribed: agent-name -> topic-name
Current subscribers: subscriber-1, subscriber-2, agent-name
```

If already subscribed:

```
agent-name is already subscribed to topic-name.
```

### UNSUBSCRIBE Format

```
UNSUBSCRIBE topic-name
[AGENT: agent-name]
```

| Field | Required | Format | Description |
|-------|----------|--------|-------------|
| UNSUBSCRIBE | Yes | `UNSUBSCRIBE topic-name` | First line. The topic/channel to unsubscribe from. |
| AGENT | Yes | `[AGENT: agent-name]` | The agent to remove from the subscriber list. |

#### Confirmation

```
Unsubscribed: agent-name from topic-name
Remaining subscribers: subscriber-1, subscriber-2
```

If the channel is now empty:

```
Unsubscribed: agent-name from topic-name. Channel removed (no remaining subscribers).
```

If the agent was not subscribed:

```
agent-name is not subscribed to topic-name.
```

### Error Handling

If the incoming message does not match any expected format:

```
Could not parse request. Expected one of:
PUBLISH topic-name / [FROM: ...] / --- / Body
SUBSCRIBE topic-name / [AGENT: ...]
UNSUBSCRIBE topic-name / [AGENT: ...]
```

### Rules

1. The pub-sub-relayer **never** reads, interprets, summarizes, or responds to published message content. It is a dumb pipe.
2. The pub-sub-relayer **never** modifies the message body. It forwards exactly as received.
3. The pub-sub-relayer **never** decides who should receive messages. The registry is authoritative.
4. The pub-sub-relayer **never** engages in conversation beyond parse-route-confirm.
5. The pub-sub-relayer **does not** forward a message back to the publisher, even if the publisher is a subscriber.
6. The pub-sub-relayer reads the registry fresh before every PUBLISH -- it never caches subscriber lists.
7. One request is processed at a time. All deliveries and the confirmation are completed before handling the next message.

### Example: Build Pipeline Notifications

Setup -- squad-leader subscribes agents to channels:

```
SUBSCRIBE build-events
[AGENT: tester]
```

```
SUBSCRIBE build-events
[AGENT: deployer]
```

Build worker publishes a result:

```
PUBLISH build-events
[FROM: build-worker]
---
Build #42 succeeded. Artifacts at dist/. Ready for testing and deploy.
```

Pub-sub-relay forwards to `tester`:

```
[FROM: build-worker] (via pub-sub-relayer, topic: build-events)
---
Build #42 succeeded. Artifacts at dist/. Ready for testing and deploy.
```

(Same message forwarded to `deployer`.)

Pub-sub-relay confirms to `build-worker`:

```
Published to topic: build-events
Delivered to: tester, deployer
```

### Example: Error Channel

Multiple agents subscribe to an error channel for monitoring:

```
SUBSCRIBE errors
[AGENT: debugger]
```

```
SUBSCRIBE errors
[AGENT: team-lead]
```

Any agent can publish errors:

```
PUBLISH errors
[FROM: api-worker]
---
Unhandled exception in /api/users endpoint: TypeError: Cannot read property 'id' of undefined
Stack trace: ...
```

Both `debugger` and `team-lead` receive the error notification automatically.

---

## Protocol Versioning

These protocols are defined in the plugin's architecture decision record. Changes to protocol formats should be documented with clear migration guidance. The `SPAWN REQUEST` and `COMPLETION REPORT` headers serve as version-independent markers that the team-lead uses to identify and parse these structured messages.
