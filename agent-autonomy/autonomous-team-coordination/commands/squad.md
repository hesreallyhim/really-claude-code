---
name: squad
description: Spawn a self-coordinating squad to design and coordinate a sub-team
argument-hint: [--sonnet] [task-description]
---

<!--
Usage: /squad [--sonnet] [task description]
Example: /squad Implement the authentication overhaul with OAuth2 and MFA support
Example: /squad --sonnet Refactor the legacy notification module
Requires: The trio agents (squad-leader, team-architect, skill-identifier) bundled
          in this plugin's agents/ directory. The contingent agent-explorer
          (also bundled) is spawned only on demand via a follow-up SPAWN REQUEST
          when the squad-leader determines a gap genuinely requires catalog search.
-->

# /squad: Spawn a Self-Coordinating Squad

## Overview

This command triggers the **trio pattern** from ADR-001 (Hierarchical Team Coordination). It spawns three agents in parallel -- a squad-leader, a team-architect, and a skill-identifier -- then assigns the user's task to the squad-leader, who runs the design phase and sends spawn requests back to you (the team-lead) for the workers it needs.

## Task

Parse `$ARGUMENTS` for an optional `--sonnet` flag at the start. If present, strip it from the task string and set `SONNET_DEFAULT = true`; otherwise `SONNET_DEFAULT = false`.

The remaining task to assign to the squad: `$ARGUMENTS` (with `--sonnet` removed if present).

If no task argument remains, ask the user what task the squad should handle before proceeding.

## Model Selection

This plugin biases toward Opus for reasoning-critical roles, but respects the user's default-model setting elsewhere. Two modes:

- **Default mode** (no `--sonnet` flag): the team-architect is spawned with `opus` explicitly because pattern selection is deeply reasoning-dependent and Sonnet's output here is materially worse. The other trio agents are spawned with `default` (whatever model the user has configured) since their work is more structured. Workers requested via SPAWN REQUEST follow the squad-leader's per-role recommendation.
- **`--sonnet` mode**: the user has explicitly opted to run the entire squad on Sonnet. Spawn all trio agents with `sonnet`, and pass an instruction to the squad-leader that workers should default to `sonnet` in spawn requests unless a role genuinely cannot function with it. We do not encourage this for team-architect specifically, but if the user has asked for it, honor the request.

## Execution Steps

### Step 1: Spawn the Trio (in parallel)

Spawn all three agents simultaneously using the Task tool with `team_name` set to the current team name. Use the agent definitions from `${CLAUDE_PLUGIN_ROOT}/agents/`:

1. **squad-leader**
   - Agent: `squad-leader` (from `${CLAUDE_PLUGIN_ROOT}/agents/squad-leader.md`)
   - Model: `sonnet` if `SONNET_DEFAULT`, else `default`
   - Role: Delegated coordinator -- will design the sub-team and manage workers
   - This agent receives the task assignment

2. **team-architect**
   - Agent: `team-architect` (from `${CLAUDE_PLUGIN_ROOT}/agents/team-architect.md`)
   - Model: `sonnet` if `SONNET_DEFAULT`, else `opus` (explicit -- pattern selection benefits materially from deeper reasoning)
   - Role: Pattern selection expert -- analyzes the task and recommends team structure

3. **skill-identifier**
   - Agent: `skill-identifier` (from `${CLAUDE_PLUGIN_ROOT}/agents/skill-identifier.md`)
   - Model: `sonnet` if `SONNET_DEFAULT`, else `default`
   - Role: Skill identification specialist -- identifies required skills, maps them to available skills, and flags gaps when present

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

If `SONNET_DEFAULT` is true, append this line to the message above before sending:

```
MODEL POLICY: The user invoked /squad with --sonnet. Default workers in your
SPAWN REQUEST to `sonnet` unless a role genuinely cannot function with it.
```

### Step 3: Wait for the Spawn Request

The squad-leader will:
1. Consult the team-architect for pattern/topology recommendations
2. Consult the skill-identifier for capability gap analysis
3. Synthesize both inputs into a structured SPAWN REQUEST

When you receive the SPAWN REQUEST from the squad-leader, parse it and spawn the requested worker agents — **subject to the SendMessage requirement below**. Then confirm back to the squad-leader that the agents are available, noting any `subagent_type` substitutions you made.

**Expect multiple SPAWN REQUESTs across the squad's lifetime.** The squad-leader is instructed to send per-phase spawn requests by default rather than batching every worker into one up-front request. This is an anti-wedging measure — long-idle workers parked since the start of the run are the ones most likely to be stuck in their tmux panes when finally messaged, so the squad-leader spawns them just-in-time. Each incoming SPAWN REQUEST is validated against all four Hard Rules independently. Treat them as a normal stream of small requests, not as exceptions.

**Contingent agent-explorer.** A follow-up SPAWN REQUEST may also include the `agent-explorer` agent — this is the contingent fourth member of the design phase, requested by the squad-leader only when the trio has identified a gap that genuinely cannot be filled by composition (existing agent + skill, modified agent prompt, paired existing skills). Treat it like any other SPAWN REQUEST line; the agent-explorer is bundled in this plugin's `agents/` directory.

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

#### Rule 4 — Working-Directory Permissions

If you (the team-lead) decide to organize the squad-leader and its workers in a non-default working directory -- e.g., a `/tmp` scratch path, a sibling worktree, a project-relative `runs/` directory -- you must verify before spawning that **every agent in the squad has the necessary permissions to read, write, and (where applicable) execute scripts in that directory**. We have observed real failures where a squad was launched in `/tmp` and individual agents got confused mid-run because their tool-permission policies didn't extend there: file reads silently failed, writes hit `EACCES`, and the squad-leader saw "completed" reports for tasks that had actually no-oped.

The fix is upstream: before sending the assignment message in Step 2, check that the chosen working directory is reachable by all spawned agent types under their permission policies. If you're unsure, default to the project root or `~/.claude/<work-type>-runs/` (which Rule 2 already prefers for output persistence) -- both of those are well-trodden paths that every agent type can access. Don't try to debug permission failures inside a running squad; spawn it somewhere everyone can already reach.

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

> **Team-lead validation step:** before honoring `READY TO PROCEED: YES`, run all four Hard Rules above — every agent has `SendMessage`, the output root is persistent (not `/tmp`), every worker has explicit file scope plus permission to do destructive actions in that scope, and every spawned agent has the working-directory permissions it needs. Substitute, push back for clarification, or reject as needed.

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

## Notes

- The trio pattern is designed for complex tasks. For simple tasks (well-known pattern, 3 or fewer agents, no skill gaps), the squad-leader may short-circuit the design phase and send a spawn request directly without consulting the other two agents.
- All agents exist in one flat team namespace. Sub-team isolation is enforced by convention in the squad-leader's prompt, not by system boundaries.
- The team-lead (you) is the only agent that can spawn new agents. The squad-leader must always request spawns through you.
- Context isolation is the primary benefit: the squad-leader absorbs all coordination chatter, keeping your context clean for other work.
