---
name: agent-prompt-engineering
description: Techniques for writing comprehensive, self-contained prompts when spawning sub-agents or teammates via the Task tool. Use when delegating work to agents, designing multi-agent workflows, or when spawned agents are returning poor results due to insufficient context. Covers frontloading, file path enumeration, deliverable specification, constraint injection, and pattern reuse across spawn calls.
---

# Agent Prompt Engineering

How to write prompts that let spawned agents work autonomously without follow-up.

## Core Principle

A spawned agent has no memory of your conversation. Everything it needs must be in the prompt. The goal is zero round-trips -- the agent reads the prompt, does the work, and returns a complete result.

## The Five Components

Every agent spawn prompt should contain these sections, in this order:

### 1. Role and Scope

One sentence stating what the agent IS and what it is NOT responsible for.

```
You are the Brand Architect for [project]. Your job is to create the brand
identity skill and visual guidelines. You are NOT writing the README or
creating demos -- other agents handle those.
```

Why: Prevents scope creep. Agents with unclear boundaries will attempt everything.

### 2. File Paths to Read (exhaustive)

List every file the agent needs, with absolute paths. Group by purpose.

```
## READ THESE FIRST

**Brand resources:**
- ~/.claude/skills/brand-guidelines/SKILL.md
- ~/.claude/skills/brand-guidelines/references/tone-guide.md

**Source code (for technical accuracy):**
- /path/to/project/src/main.sh
- /path/to/project/config.json

**Current state (your starting point):**
- /path/to/project/README.md
```

Why: Agents cannot guess file locations. Missing a single path means missing context. Absolute paths eliminate ambiguity.

### 3. Deliverables with Exact Output Paths

Numbered list. Each deliverable has a file path and acceptance criteria.

```
YOUR DELIVERABLES (in order):

1. CREATE the brand skill at ~/.claude/skills/project-brand/
   Requirements:
   - Color palette with hex codes
   - Tone of voice guidelines with do/don't examples
   - README template

2. WRITE the social preview concept to /path/to/project/docs/social-preview.md
   Requirements:
   - 1280x640 dimensions
   - Exact color specs
```

Why: "Create a brand guide" is vague. "Create SKILL.md at this path with these sections" is unambiguous. The agent knows exactly what to produce and where to put it.

### 4. Constraints (non-negotiable rules)

Labeled as CRITICAL. Repeated if they are easy to violate.

```
CRITICAL CONSTRAINTS:
- NO EMOJIS anywhere. This is absolute.
- All content must be technically accurate -- read the source code.
- Dark-mode optimized -- test all colors against #1a1a2e background.
```

Why: Agents optimize for completion. Without explicit constraints, they will take shortcuts. Labeling constraints as CRITICAL increases compliance. Repeating important constraints in multiple sections (role, deliverables, constraints) provides redundancy.

### 5. Communication Protocol

How the agent should report back.

```
After completing all deliverables, send a message to the team lead
summarizing what you created and where the files are located.
```

Or for background agents:

```
Commit your work when done.
```

Why: Without this, agents may finish silently or produce output in unexpected formats.

## Techniques

### Frontloading

Put the most important context first. If the agent hits a token limit or loses focus, the critical information was already processed.

Order: Role > Context > File paths > Deliverables > Constraints

### Pattern Reuse

When spawning multiple agents in a session, establish a template with the first spawn and adapt it for subsequent ones. Consistent structure across spawns means:
- You write faster (copy-adapt, not write-from-scratch)
- Agents produce consistent output formats
- Review is easier (you know where to look)

### Dependency Declaration

When an agent's work depends on another agent's output, state it explicitly:

```
BEFORE YOU START:
- Read the brand skill at ~/.claude/skills/project-brand/SKILL.md
  (created by the brand-architect agent in Phase 1)
- If this file does not exist, STOP and report the dependency failure.
```

### Context Bridging

Spawned agents cannot see your conversation. When referencing decisions made earlier in the session, include the decision and its rationale:

```
The team decided on a cyan/amber/red color palette derived from the
project's existing TUI output. These are not arbitrary choices -- they
match the ANSI colors already used in the codebase.
```

Don't say "use the colors we discussed" -- the agent wasn't there.

### Constraint Repetition

For rules that are easy to violate (no emojis, no marketing speak, technical accuracy), state them:
1. In the role section ("you are a technically precise writer who never uses emojis")
2. In the deliverables section ("ensure no emojis in any output")
3. In the constraints section ("CRITICAL: NO EMOJIS")

Three mentions is not redundant -- it is insurance.

### File Path Enumeration vs. Discovery

Prefer giving explicit paths over asking the agent to find files:

```
# Good: agent reads immediately
Read ~/.claude/skills/brand-guidelines/SKILL.md

# Bad: agent wastes turns searching
Find and read the brand guidelines skill
```

Exception: when the agent's job IS discovery (e.g., "scan ~/.claude/agents/ and report what exists").

### Output Path Specification

Always specify where the agent should write. Never let it choose:

```
# Good: predictable output location
Write to: /path/to/project/docs/launch-content/hacker-news.md

# Bad: agent picks a location you don't expect
Write the HN draft somewhere appropriate
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| "Do what the previous agent did" | Agent has no memory of previous agents | Include the relevant output or file paths |
| Vague deliverables ("improve the README") | Agent has no acceptance criteria | Specify exactly what to change and why |
| Missing file paths | Agent guesses or searches, wasting turns | Enumerate every file it needs |
| No constraints section | Agent takes shortcuts | Add explicit CRITICAL CONSTRAINTS |
| Overloading one agent | Agent loses focus after 5+ deliverables | Split into multiple agents with 2-3 deliverables each |
| "Be creative" without boundaries | Unpredictable output | Provide examples of what good output looks like |

## Scaling: When to Split Agents

- **1-3 deliverables:** Single agent
- **4-6 deliverables:** Consider splitting if deliverables are in different domains
- **7+ deliverables:** Always split. No agent maintains quality across 7+ tasks.

## Model Selection

- **opus:** Creative work (brand identity, copywriting, architecture decisions), complex reasoning
- **sonnet:** Structured execution (applying a template, reformatting, review checklists)
- **haiku:** Simple lookups, file scanning, status checks
