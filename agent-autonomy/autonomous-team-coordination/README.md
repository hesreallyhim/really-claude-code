# Autonomous Team Coordination Plugin

A Claude Code plugin that enables autonomous multi-agent team management and collaboration patterns using only the native Claude Code agent teams feature.

## Quickstart

No.

## Installation

TODO

## Usage

### The `/squad` Command

Use `/squad` to delegate a complex task to a self-coordinating sub-team. This triggers the **trio pattern**: a squad-leader, team-architect, and skill-identifier work together to design the optimal team, then the squad-leader coordinates execution.

```
/squad Build a REST API with authentication, rate limiting, and comprehensive tests
```

What happens:

1. The team-lead spawns three agents in parallel: `squad-leader`, `team-architect`, and `skill-identifier`.
2. The squad-leader consults the team-architect for team structure and the skill-identifier for gap analysis.
3. The squad-leader synthesizes both inputs and sends a structured **spawn request** back to the team-lead.
4. The team-lead spawns the requested worker agents.
5. The squad-leader coordinates the workers autonomously -- creating tasks, assigning work, managing dependencies, and handling blockers.
6. When all work is done, the squad-leader sends a **completion report** to the team-lead.

The team-lead's context stays clean throughout. It only processes the initial spawn request and the final completion report.

### The `/announce` Command

Use `/announce` to send a message to multiple specific agents without broadcasting to the entire team.

```
/announce [worker-api, worker-db, worker-auth] The shared config schema has changed. Pull latest and re-validate.
```

This spawns the `announcer` agent (if not already active), which parses the recipient list and forwards the message individually to each named agent.

### The `/publish` Command

Use `/publish` to send a message to all subscribers of a pub/sub topic.

```
/publish build-events Build succeeded for commit abc123. Artifacts at dist/.
```

This spawns the `pub-sub-relayer` agent (if not already active), which reads the channel registry at `${CLAUDE_PLUGIN_ROOT}/state/pubsub-channels.json`, looks up subscribers for the topic, and forwards the message to each of them. The publisher does not need to know who is subscribed.

### Direct Agent Usage

You can also spawn agents directly without slash commands:

- Spawn a `squad-leader` for any task that needs a coordinated sub-team.
- Spawn a `team-architect` standalone when you need a team design document without executing it.
- Spawn a `skill-identifier` standalone when you need a capability gap analysis.
- Spawn an `announcer` when any agent needs to fan out messages to a subset of the team.

## The Trio Pattern

The trio pattern is the core workflow of this plugin. It separates concerns across three specialized agents:

```
                    +-----------------+
                    |  SQUAD-LEADER   |  <-- orchestration only, no domain expertise
                    +--------+--------+
                             |
                    consults | both
                   +---------+---------+
                   |                   |
           +-------+-------+  +-------+--------+
           | TEAM-ARCHITECT |  | SKILL-IDENTIFIER|
           | (patterns)     |  | (capabilities)  |
           +---------------+  +----------------+
```

**Squad-leader** -- Pure orchestration. Receives the task, consults the other two agents, synthesizes a spawn request, and then coordinates whatever workers get spawned. Has no domain expertise of its own.

**Team-architect** -- Selects the optimal team pattern (e.g., supervisor-worker, pipeline, fan-out) and communication topology based on the task's traits (urgency, complexity, knowledge needs, risk). References the `team-patterns` skill.

**Skill-identifier** -- Analyzes what skills each agent role needs, checks installed skills against requirements, and flags gaps. References the `skill-identification` skill.

### Short-Circuit Logic

For simple, well-known patterns (e.g., a critic-reviser loop with 2-3 agents), the squad-leader skips the design phase entirely. It evaluates four criteria:

1. The task maps to a single, well-known pattern
2. Requires 3 or fewer worker agents
3. No skill gaps are expected
4. The communication topology is obvious

If all four are met, the squad-leader constructs the spawn request directly, saving a round-trip through the team-architect and skill-identifier.

## Multi-Squad Architecture

For projects with independent workstreams, multiple squad-leaders can run in parallel:

```
                    +------------------+
                    |   TEAM LEAD      |  <-- minimal context: spawn requests + reports
                    +--------+---------+
                             |
                 +-----------+-----------+
                 |                       |
          +------+------+        +------+------+
          | SQUAD-LEAD  |        | SQUAD-LEAD  |
          | (backend)   |        | (frontend)  |
          +------+------+        +------+------+
                 |                       |
          +------+------+        +------+------+
          |      |      |        |      |      |
         API   Data  Review    UI    State  Review
         Eng   Eng   Gate      Eng   Eng    Gate
```

Each squad-leader:

- Runs its own design phase (optionally with team-architect + skill-identifier)
- Requests its own workers via spawn request
- Coordinates its sub-team independently
- Reports to the team-lead only for spawns, shutdowns, and completion

Cross-team communication goes through the team-lead, not directly between squads.

## Communication Protocols

The plugin defines three structured message protocols. See `skills/team-coordination/references/protocols.md` for full specifications.

### Spawn Request

Sent by the squad-leader to the team-lead when requesting worker agents:

```
SPAWN REQUEST
=============
Task: Build REST API with auth and rate limiting
Pattern: Supervisor-Worker with Reflection Loop
Topology: hub-and-spoke
Design phase: FULL

AGENTS REQUESTED:
1. Name: api-implementer
   Type: independent-contributor
   Model: sonnet
   Role: Implements API endpoints and middleware

2. Name: api-reviewer
   Type: critical-code-reviewer
   Model: opus
   Role: Reviews all code before integration

SKILLS NEEDED:
- Existing: team-patterns -> squad-leader
- Missing: rate-limiting-patterns -> create with skill-creator-enhanced

TASK GRAPH:
Task 1: Implement auth middleware -> Owner: api-implementer
Task 2: Implement rate limiter -> Owner: api-implementer (blocked by: 1)
Task 3: Review auth code -> Owner: api-reviewer (blocked by: 1)
Task 4: Write integration tests -> Owner: api-implementer (blocked by: 2, 3)

READY TO PROCEED: YES
```

### Completion Report

Sent by the squad-leader to the team-lead when all work is done:

```
COMPLETION REPORT
=================
Task: Build REST API with auth and rate limiting
Status: COMPLETE

Summary:
Implemented JWT authentication middleware and token-bucket rate limiter.
All endpoints have integration tests with 94% coverage.

Artifacts:
- src/middleware/auth.ts
- src/middleware/rate-limiter.ts
- tests/integration/api.test.ts

Agents Used:
- api-implementer: Built all endpoints, middleware, and tests
- api-reviewer: Reviewed 3 PRs, caught 2 security issues

Issues:
- None

Recommendations:
- Consider adding Redis-backed rate limiting for multi-instance deployments
```

### Announcer

Any agent can send a multi-recipient message through the announcer:

```
[TO: worker-1, worker-2, worker-3]
[FROM: squad-leader]
---
The shared config schema has changed. Please pull the latest and re-validate your modules.
```

The announcer forwards individually to each recipient and confirms delivery back to the sender.

#### Why a separate agent?

Claude Code's `SendMessage` tool only supports two modes: a direct message to one recipient, or a broadcast to every teammate. There is no "send to these 3 out of 8" primitive. To message a subset, someone has to emit N individual `SendMessage` calls.

If the team-lead (or any working agent) does this inline, it pays a cost:

- **Context window**: N tool calls + N tool results expand the agent's context with routing boilerplate that has nothing to do with its actual work.
- **Turn budget**: The agent spends a turn on message fan-out instead of productive work.
- **Prompt pollution**: The N delivery confirmations clutter the conversation history for the rest of the session.

The announcer absorbs all of this. It runs on haiku (cheapest model), is restricted to `SendMessage` only, and its context window is entirely disposable -- it exists solely to parse headers and fan out messages. The sending agent pays for exactly one `SendMessage` (to the announcer), and the announcer handles the rest in its own isolated context.

#### How parallel delivery works

When the announcer processes a relay request, it emits all N `SendMessage` calls in a single response. The runtime executes all tool calls from one response concurrently, so the forwards happen in parallel -- not sequentially. The full cycle for a relay with N recipients is:

1. **Turn 1** (incoming): Announcer receives the relay request as an incoming message. No tool call needed -- the `[TO:]`, `[FROM:]`, and body are already in its prompt context.
2. **Turn 2** (forward): Announcer emits N parallel `SendMessage` calls, one per recipient. All execute concurrently.
3. **Turn 3** (confirm): Announcer sends exactly one `SendMessage` back to the original sender with a delivery summary.

Total: 3 turns and N+1 `SendMessage` calls, regardless of recipient count. The sending agent's context grows by exactly 2 messages (its outbound relay request + the delivery confirmation).

#### Pub/Sub Relayer

The `pub-sub-relayer` follows the same disposable-agent pattern but adds topic-based routing. Instead of the sender listing recipients explicitly, it publishes to a topic and the relayer looks up subscribers from a file-backed registry at `${CLAUDE_PLUGIN_ROOT}/state/pubsub-channels.json`. This decouples publishers from subscribers -- a publisher doesn't need to know who is listening, and new subscribers can be added without changing any publisher code.

The same parallel delivery mechanics apply: all subscriber forwards are emitted in a single response and execute concurrently.

## Plugin Structure

```
hierarchical-team-coordination/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── agents/
│   ├── squad-leader.md          # Delegated coordinator
│   ├── team-architect.md        # Pattern selection expert
│   ├── skill-identifier.md      # Capability gap analyst
│   └── announcer.md            # Stateless message relay
├── commands/
│   ├── squad.md                 # /squad slash command
│   ├── announce.md              # /announce slash command
│   └── publish.md               # /publish slash command
├── hooks/
│   ├── hooks.json               # Hook configuration
│   └── scripts/
│       └── cross-boundary-warning.sh  # Sub-team boundary warning
├── skills/
│   ├── team-coordination/
│   │   ├── SKILL.md             # Skill definition and protocol reference
│   │   └── references/
│   │       └── protocols.md     # Detailed protocol specifications
│   ├── team-patterns/           # Bundled: team organization patterns
│   │   ├── SKILL.md
│   │   ├── references/          # Pattern catalogs, topology diagrams, etc.
│   │   ├── examples/            # Example team designs
│   │   └── scripts/             # pattern-selector.py, scan-agents.sh, etc.
│   └── skill-identification/    # Bundled: capability gap analysis framework
│       ├── SKILL.md
│       └── ...                  # Patterns, templates, analysis scripts
├── scripts/
│   └── roster.sh               # Squad roster management utility
└── README.md                   # This file
```

## Constraints and Limitations

1. **Spawn authority is centralized.** Only the team-lead can spawn agents. Every new agent requires a round-trip through the team-lead, which adds latency.

2. **No hard sub-team boundaries.** Any agent can message any other agent by name. Sub-team isolation is enforced by convention (agent prompts), not by the system. The cross-boundary warning hook provides a soft enforcement layer.

3. **No native multi-send.** The announcer mitigates this but still makes N individual `SendMessage` API calls under the hood.

4. **Team-lead availability.** If the team-lead is deep in its own work, there is latency before it processes spawn requests. Messages queue until the team-lead's turn ends.

5. **Agent context is lost on dismissal.** If a worker is shut down, any uncommitted work or unshared findings are gone. Squad-leaders should ensure agents commit and document before requesting dismissals.

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Squad-leader has no domain expertise | Keeps prompts focused; domain decisions belong to workers or consultants |
| Short-circuit for simple patterns | Avoids spawning team-architect + skill-identifier for a 2-agent critic-reviser loop |
| Structured spawn request format | Team-lead parses requests without back-and-forth clarification |
| Announcer uses haiku with tool restriction | Relay function needs zero reasoning; haiku minimizes cost; `["SendMessage"]` prevents unintended actions |
| Convention-based sub-team boundaries | No system-level enforcement exists; prompts + hook provide soft guardrails |
| Context isolation is the primary benefit | Team-lead context window stays clean; squad-leader absorbs coordination chatter |
