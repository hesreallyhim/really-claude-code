---
name: team-coordination
description: Protocol reference for delegated squad coordination. Defines the spawn request and completion report message formats that agents use to communicate within a delegated multi-agent squad. This skill should be used when agents need to send spawn requests, write completion reports, or understand the communication conventions of a delegated squad setup. Also use when you see terms like "spawn request", "completion report", "squad coordination", or "team message format".
---

# Team Coordination Skill

Protocol reference for agents operating within a delegated squad coordination structure. This skill defines the exact message formats and communication conventions that enable delegated, context-efficient team management.

## When to Use This Skill

- You are a **squad-leader** and need to send a spawn request or completion report
- You are a **team-lead** and need to parse an incoming spawn request or completion report
- You need to understand the communication boundaries and conventions of a delegated squad

## Protocol Summary

| Protocol | Sender | Receiver | Purpose |
|----------|--------|----------|---------|
| Spawn Request | squad-leader | team-lead | Request creation of worker agents |
| Completion Report | squad-leader | team-lead | Report task completion or partial progress |

## Quick Reference: Spawn Request

```
SPAWN REQUEST
=============
Task: [one-sentence task description]
Pattern: [pattern name]
Topology: [hub-and-spoke | pipeline | mesh | tree | star | adversarial]
Design phase: [FULL | SHORT-CIRCUITED -- reason]

AGENTS REQUESTED:
1. Name: [agent-name]
   Type: [existing agent type]
   Model: [opus/sonnet/haiku]
   Role: [one-sentence role description]

SKILLS NEEDED:
- Existing: [skill-name] -> assigned to [agent-name]
- Missing: [skill-name] -> [spec or "create with skill-creator-enhanced"]

TASK GRAPH:
Task 1: [description] -> Owner: [agent-name]
Task 2: [description] -> Owner: [agent-name] (blocked by: 1)

READY TO PROCEED: [YES | NO -- reason]
```

## Quick Reference: Completion Report

```
COMPLETION REPORT
=================
Task: [original task description]
Status: [COMPLETE | PARTIAL -- explanation]

Summary:
[2-5 sentences]

Artifacts:
- [files created/modified]

Agents Used:
- [agent-name]: [what they accomplished]

Issues:
- [unresolved problems, or "None"]

Recommendations:
- [follow-up work, or "None"]
```

## Detailed Protocol Specifications

For field-by-field specifications, validation rules, edge cases, and examples, see [references/protocols.md](references/protocols.md).

## Communication Boundaries

### Within a squad (squad-leader + its workers)

- Workers communicate with their squad-leader freely.
- Workers may communicate with peers in the same squad.
- The squad-leader coordinates all work within the squad.

### Between squads

- Cross-squad messages go through the team-lead.
- Workers do not message agents in other squads directly.
- Squad-leaders do not message other squad-leaders directly.

These boundaries are enforced by convention in agent prompts, not by system-level restrictions.

## Agent Roles Reference

The trio (squad-leader + team-architect + skill-identifier) is the default design-phase team. The **agent-explorer** is a contingent fourth member, brought in only when a capability gap genuinely cannot be filled by extending or modifying existing skills/agents.

| Agent | Model | Purpose | Tools |
|-------|-------|---------|-------|
| squad-leader | default | Orchestrates sub-teams, sends spawn requests, manages workers | All standard tools |
| team-architect | opus | Selects team patterns and communication topologies | All standard tools |
| skill-identifier | default | Identifies required skills, maps to installed ecosystem, surfaces gaps | All standard tools |
| agent-explorer | default | Searches plugin catalogs for existing agents/skills matching gaps (contingent) | Read, Glob, Grep, LS, SendMessage |

Models above match the agents' frontmatter `model:` field. `default` lets the user's configured default model handle the role; `opus` is explicit because pattern selection benefits materially from deeper reasoning. Per-spawn overrides at `/squad` time (e.g., `--sonnet`) take precedence; see `commands/squad.md` for the full model policy.

## Dependencies

The skills referenced below are bundled with this plugin:

- **team-patterns** skill (`${CLAUDE_PLUGIN_ROOT}/skills/team-patterns/`) -- Used by the team-architect for pattern selection
- **skill-identification** skill (`${CLAUDE_PLUGIN_ROOT}/skills/skill-identification/`) -- Used by the skill-identifier for capability analysis
- **agent-prompt-engineering** skill (`${CLAUDE_PLUGIN_ROOT}/skills/agent-prompt-engineering/`) -- Used by the squad-leader when crafting initial briefing messages for workers (Phase 3, step 4)
