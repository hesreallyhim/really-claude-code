---
name: team-coordination
description: Protocol reference for hierarchical team coordination. Defines the spawn request, completion report, and announcer message formats that agents use to communicate within a hierarchical multi-agent team. This skill should be used when agents need to send spawn requests, write completion reports, relay messages to multiple recipients, or understand the communication conventions of a hierarchical team setup. Also use when you see terms like "spawn request", "completion report", "announcer", "relay protocol", "squad coordination", or "hierarchical team message format".
---

# Team Coordination Skill

Protocol reference for agents operating within a hierarchical team coordination structure. This skill defines the exact message formats and communication conventions that enable delegated, context-efficient team management.

## When to Use This Skill

- You are a **squad-leader** and need to send a spawn request or completion report
- You are **any agent** and need to relay a message to multiple recipients via the announcer
- You are a **team-lead** and need to parse an incoming spawn request or completion report
- You need to understand the communication boundaries and conventions of a hierarchical team

## Protocol Summary

| Protocol | Sender | Receiver | Purpose |
|----------|--------|----------|---------|
| Spawn Request | squad-leader | team-lead | Request creation of worker agents |
| Completion Report | squad-leader | team-lead | Report task completion or partial progress |
| Announcer | any agent | announcer | Fan out a message to multiple named recipients |

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

## Quick Reference: Announcer

Sending a relay request (any agent to announcer):

```
[TO: recipient-1, recipient-2, recipient-3]
[FROM: sender-name]
---
Message body here.
```

Forwarded message (announcer to each recipient):

```
[FROM: sender-name] (via announcer)
---
Message body here.
```

Delivery confirmation (announcer to sender):

```
Delivered to: recipient-1, recipient-2, recipient-3
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

### Using the announcer

- Any agent may send a relay request to the announcer.
- The announcer forwards to any named recipient regardless of squad boundaries.
- The cross-boundary warning hook monitors for messages that cross squad boundaries and logs a warning (does not block).

These boundaries are enforced by convention in agent prompts, not by system-level restrictions. The cross-boundary warning hook in `hooks/scripts/cross-boundary-warning.sh` provides a soft enforcement layer.

## Agent Roles Reference

| Agent | Model | Purpose | Tools |
|-------|-------|---------|-------|
| squad-leader | opus | Orchestrates sub-teams, sends spawn requests, manages workers | All standard tools |
| team-architect | opus | Selects team patterns and communication topologies | All standard tools |
| skill-identifier | opus | Analyzes capability requirements and identifies gaps | All standard tools |
| agent-explorer | sonnet | Searches plugin catalogs for existing agents/skills matching gaps | Read, Glob, Grep, LS |
| announcer | haiku | Stateless message relay for multi-recipient delivery | `SendMessage` only |

## Dependencies

Both skills referenced below are bundled with this plugin:

- **team-patterns** skill (`${CLAUDE_PLUGIN_ROOT}/skills/team-patterns/`) -- Used by the team-architect for pattern selection
- **skill-identification** skill (`${CLAUDE_PLUGIN_ROOT}/skills/skill-identification/`) -- Used by the skill-identifier for capability analysis
