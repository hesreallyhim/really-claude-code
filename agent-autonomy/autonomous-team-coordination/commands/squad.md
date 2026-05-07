---
name: squad
description: Spawn a hierarchical squad to design and coordinate a sub-team
argument-hint: [task-description]
---

<!--
Usage: /squad [task description]
Example: /squad Implement the authentication overhaul with OAuth2 and MFA support
Requires: The trio agents (squad-leader, team-architect, skill-identifier) bundled
          in this plugin's agents/ directory.
-->

# /squad: Spawn a Hierarchical Squad

## Overview

This command triggers the **trio pattern** from ADR-001 (Hierarchical Team Coordination). It spawns three agents in parallel -- a squad-leader, a team-architect, and a skill-identifier -- then assigns the user's task to the squad-leader, who runs the design phase and sends spawn requests back to you (the team-lead) for the workers it needs.

## Task

The task to assign to the squad: `$ARGUMENTS`

If no task argument is provided, ask the user what task the squad should handle before proceeding.

## Execution Steps

### Step 1: Spawn the Trio (in parallel)

Spawn all three agents simultaneously using the Task tool with `team_name` set to the current team name. Use the agent definitions from `${CLAUDE_PLUGIN_ROOT}/agents/`:

1. **squad-leader**
   - Agent: `squad-leader` (from `${CLAUDE_PLUGIN_ROOT}/agents/squad-leader.md`)
   - Model: opus
   - Role: Delegated coordinator -- will design the sub-team and manage workers
   - This agent receives the task assignment

2. **team-architect**
   - Agent: `team-architect` (from `${CLAUDE_PLUGIN_ROOT}/agents/team-architect.md`)
   - Model: opus
   - Role: Pattern selection expert -- analyzes the task and recommends team structure

3. **skill-identifier**
   - Agent: `skill-identifier` (from `${CLAUDE_PLUGIN_ROOT}/agents/skill-identifier.md`)
   - Model: sonnet
   - Role: Capability gap analyst -- maps required skills to available skills and identifies gaps

All three agents MUST be spawned in the same message (parallel tool calls) to minimize latency.

### Step 2: Assign the Task to the Squad Leader

After all three agents are spawned, send a message to the `squad-leader` with:

```
You have been assigned the following task:

$ARGUMENTS

Your team-architect and skill-identifier are available for consultation.
- Message `team-architect` for team structure and pattern recommendations.
- Message `skill-identifier` for capability gap analysis.

When you have synthesized their input, send me a SPAWN REQUEST using the
protocol from ADR-001 and I will spawn the workers you need.
```

### Step 3: Wait for the Spawn Request

The squad-leader will:
1. Consult the team-architect for pattern/topology recommendations
2. Consult the skill-identifier for capability gap analysis
3. Synthesize both inputs into a structured SPAWN REQUEST

When you receive the SPAWN REQUEST from the squad-leader, parse it and spawn the requested worker agents — **subject to the SendMessage requirement below**. Then confirm back to the squad-leader that the agents are available, noting any `subagent_type` substitutions you made.

### Hard Rules (validate before honoring any SPAWN REQUEST)

#### Rule 1 — Every Spawned Agent MUST Have SendMessage

Before fulfilling any spawn request — **including for the trio agents in Step 1** — verify that each requested `subagent_type` exposes the `SendMessage` tool. If it does not, substitute a `subagent_type` that does (typically `general-purpose`), and notify the squad-leader of the substitution in your confirmation message.

Why this rule is non-negotiable:

- **Output delivery.** Agents without `SendMessage` cannot return work product to the team. Read-only types like `Explore`, `plugin-dev:skill-reviewer`, and similar (tools: `Read, Grep, Glob`) have no path to deliver their findings other than `Write`-to-disk, which fails silently when the agent type also lacks `Write`/`Bash`.
- **Lifecycle protocol.** Agents without `SendMessage` cannot acknowledge `shutdown_request`, so they must be force-terminated. This costs time and produces noisy team logs.
- **Peer coordination.** Hub-and-spoke and reflection patterns assume workers can talk to the squad-leader (and vice-versa). Without `SendMessage`, those topologies degrade.

The squad-leader may argue for read-only purity ("the reviewer should be `Explore` because we don't want it editing files"). Reject the argument: substitute `general-purpose` and add an explicit instruction in the worker's prompt — e.g., `"READ-ONLY: do not edit, create, or modify any file in the project under review. You may write your final report to the team's designated output directory only."` File-scope discipline belongs in the prompt, not in the tool list.

If you must reject a spawn request because no acceptable substitution exists (extremely rare), respond to the squad-leader with the rejection and ask for a redesign rather than spawning a non-functional agent.

#### Rule 2 — Output Persistence (don't lose work to `/tmp`)

`/tmp` is volatile (cleaned by the OS, lost on reboot, invisible to the project tree). Either:

- **Default the squad's output root to a persistent path** before spawning, e.g. `~/.claude/<work-type>-runs/<target-slug>/<YYYYMMDD-HHMMSS>/`. Pass that path into every worker prompt and into the squad-leader's coordination messages so all artifacts land there directly.
- **OR**, if `/tmp` must be used as scratch (e.g., a worker has restricted write paths), make the copy-out a **non-skippable step in the squad-leader's completion protocol**: durable artifacts must be moved to a persistent location before the squad-leader sends its COMPLETION REPORT. Verify the destination contents (`ls`) before any `rm` of the source.

When the squad-leader sends `READY TO PROCEED: YES`, confirm an output root is set in the spawn request and that it is not `/tmp`. If it is, push back before spawning.

#### Rule 3 — Coordination, Clarity, and File-Scope Permission

Workers running in parallel must know exactly what they own and what they don't. Before honoring a spawn request, verify the squad-leader's plan provides each worker with:

- **A specific file or directory scope** (not a topic or finding type). Two workers both editing `agents/foo.md` from different angles will conflict at commit time; one worker owning `agents/foo.md` entirely will not.
- **A "do not touch other files" rule** in their prompt. Workers who notice a cross-scope issue must NOT fix it — they flag it back to the squad-leader, who routes to the appropriate owner.
- **Explicit permission for whatever destructive actions are required** (e.g., commit, push, delete) so they don't have to ask mid-task. Keep the permission narrow (allow commit but not push; allow `rm` only inside the output root).
- **Worktree isolation** when commits are involved. Parallel workers in the same git worktree can sweep each other's unstaged WIP into their own commits via misdirected `git add`. Either spawn each worker in its own `git worktree add`, or mandate strict atomic `git add <specific-path>` + immediate commit, with `git stash` for unrelated WIP.

If the spawn request is silent on file scope, push back. Patching this in mid-run is harder than enforcing it up front.

### Step 4: Let the Squad Leader Coordinate

Once workers are spawned, the squad-leader manages the sub-team autonomously:
- Creates and assigns tasks
- Sends briefing messages to workers
- Monitors progress and handles blockers
- Sends a COMPLETION REPORT when done

You (the team-lead) only need to intervene for:
- Additional spawn requests
- Cross-team coordination (if multiple squads exist)
- Unresolvable blockers escalated by the squad-leader

## Spawn Request Protocol (Reference)

The squad-leader will send spawn requests in this format:

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

[...]

SKILLS NEEDED:
- Existing: [skill-name] -> assigned to [agent-name]
- Missing: [skill-name] -> [brief spec or "create with skill-creator-enhanced"]

TASK GRAPH:
Task 1: [description] -> Owner: [agent-name]
Task 2: [description] -> Owner: [agent-name] (blocked by: 1)
[...]

READY TO PROCEED: [YES | NO -- reason]
```

> **Team-lead validation step:** before honoring `READY TO PROCEED: YES`, run all three Hard Rules above — every agent has `SendMessage`, the output root is persistent (not `/tmp`), and every worker has explicit file scope plus permission to do destructive actions in that scope. Substitute, push back for clarification, or reject as needed.

## Completion Report Protocol (Reference)

The squad-leader will send a completion report in this format:

```
COMPLETION REPORT
=================
Task: [original task description]
Status: [COMPLETE | PARTIAL -- explanation]

Summary:
[2-5 sentences]

Artifacts:
- [key files created/modified]

Agents Used:
- [agent-name]: [what they accomplished]

Issues:
- [unresolved problems, or "None"]

Recommendations:
- [follow-up work, or "None"]
```

## Announcer (Optional)

If the squad-leader needs to send messages to multiple workers at once, you may also spawn an `announcer` agent:

- Agent: `announcer` (from `${CLAUDE_PLUGIN_ROOT}/agents/announcer.md`)
- Model: haiku
- Tools: `["SendMessage"]` only
- Role: Stateless multi-send relay

The squad-leader (or any agent) can use the announcer by sending messages in the format:
```
[TO: agent-1, agent-2, agent-3]
[FROM: sender-name]
---
Message body here.
```

Only spawn the announcer if the squad-leader requests it or if the team has 4+ workers who need group notifications.

## Notes

- The trio pattern is designed for complex tasks. For simple tasks (well-known pattern, 3 or fewer agents, no skill gaps), the squad-leader may short-circuit the design phase and send a spawn request directly without consulting the other two agents.
- All agents exist in one flat team namespace. Sub-team isolation is enforced by convention in the squad-leader's prompt, not by system boundaries.
- The team-lead (you) is the only agent that can spawn new agents. The squad-leader must always request spawns through you.
- Context isolation is the primary benefit: the squad-leader absorbs all coordination chatter, keeping your context clean for other work.
