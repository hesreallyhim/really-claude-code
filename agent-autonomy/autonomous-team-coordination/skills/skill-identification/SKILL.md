---
name: skill-identification
description: Analyze user objectives to identify and recommend the optimal set of skills, tools, and knowledge needed to complete tasks effectively. Provide skill gap analysis, pattern-based recommendations, and workflow design for complex tasks. This skill should be used when users need help determining what skills are required, when working on complex tasks requiring multiple capabilities, when detecting skill gaps or mismatches, or when designing skill ecosystems for workflows. Also use when users mention "what skills do I need", "skill discovery", "skill recommendation", "capability analysis", "skill gap", "which tools for this task", or "skill stack".
---

# Skill Identification

Analyze task requirements, identify capability gaps, and recommend optimal skill combinations. Start here, then drill into reference files as needed.

## Quick Start -- Skill Discovery

When a user presents a task or goal, perform this analysis:

```
SKILL DISCOVERY ANALYSIS
========================
Task: [User's stated objective]

Required Capabilities:
1. [Core capability needed]
2. [Supporting capability]
3. [Enhancement capability]

Recommended Skills:
- Existing: [skill-name] -- [why it helps]
- Missing: [proposed-skill] -- [what it would provide]
- Optional: [enhancement-skill] -- [additional value]

Optimal Workflow:
Step 1: [First skill/action]
Step 2: [Second skill/action]
Step 3: [Output/result]
```

## Core Analysis Framework

### Step 1: Goal Decomposition

Break down the user's objective into atomic capabilities covering:

- **Input** -- What data or content is involved?
- **Process** -- What transformations are needed?
- **Output** -- What deliverables are expected?
- **Constraints** -- What limitations apply?
- **Quality** -- What standards must be met?

**Automated analysis:** Run `scripts/skill-analyzer.py` for programmatic requirement decomposition.

### Step 2: Capability Mapping

Map required capabilities to skill types:

| Capability Category | Skill Types | Examples |
|---|---|---|
| Document Creation | Generators, Builders | docx, pptx, pdf-creator |
| Data Processing | Analyzers, Transformers | data-pipeline, csv-processor |
| Code Development | Builders, Debuggers | app-builder, code-reviewer |
| Content Analysis | Extractors, Parsers | pdf-reader, web-scraper |
| Workflow Automation | Orchestrators, Schedulers | task-automator, batch-processor |
| Quality Assurance | Validators, Testers | code-tester, accessibility-checker |
| Scenario & Persona Design | Generators, Explorers | scenario-architect, persona-builder |
| Optimization | Improvers, Refiners | performance-optimizer, seo-enhancer |

### Step 3: Skill Gap Analysis

Identify coverage against requirements:

```
GAP ANALYSIS
============
[AVAILABLE] Available Capabilities:
- [What Claude can already do]
- [Existing relevant skills]

[PARTIAL] Partial Capabilities:
- [What needs enhancement]
- [Skills that partially help]

[MISSING] Missing Capabilities:
- [What Claude cannot do]
- [Skills that need creation]

[PRIORITY] Priority Recommendations:
1. [Most critical skill to add]
2. [Second priority]
3. [Nice-to-have enhancement]
```

## Quick Reference: Common Task Patterns

| User Intent | Pattern | Core Skills | See Also |
|---|---|---|---|
| "Create/build/design [artifact]" | Creative Production | builder, templates, designer | `references/skill-patterns.md` |
| "Analyze/process/convert [data]" | Data Transformation | reader, transformer, writer | `references/skill-patterns.md` |
| "Connect/integrate/sync [systems]" | System Integration | api-connector, data-mapper, sync-manager | `references/skill-patterns.md` |
| "Improve/optimize/fix [artifact]" | Quality Improvement | analyzer, optimizer, validator | `references/skill-patterns.md` |

**Full pattern catalog:** See `references/skill-patterns.md` for complete skill combinations by domain (web, data science, content, automation, creative).

## Design vs. Execution Distinction

When analyzing team compositions for migration, transition, or transformation tasks,
distinguish between these orthogonal concerns:

| Concern | Question Answered | Example Role |
|---------|------------------|--------------|
| **Design** | What is the target state? | domain-architect, system-designer |
| **Execution** | How do we get there safely? | migration-strategist, release-coordinator |
| **Implementation** | Who builds it? | developer, engineer |

For any task involving a transition from state A to state B, always verify someone owns
the **execution strategy**: phased rollout planning, dual-system coordination, traffic
routing, rollback plans, and risk mitigation for intermediate states. Do not assume
that agents who design the target state can also plan the transition path -- these are
distinct skills.

## Proactive Skill Recognition

Watch for these signals that indicate additional skills are needed:

| Signal | Recommendation |
|---|---|
| Repetitive manual steps | Automation skill |
| Multiple format conversions | Universal converter skill |
| Accessibility not mentioned (public content) | Accessibility checker skill |
| No testing mentioned for code | Test generator skill |
| No documentation for complex systems | Documentation generator skill |
| Performance not considered | Performance analyzer skill |
| Security not addressed | Security scanner skill |
| Product targets multiple user types or regulated industries | Scenario/persona generation skill (scenario-architect) |
| PRD lacks concrete user personas or test scenarios | Scenario generation skill (scenario-architect) |

## Skill Creation Guidance

When a needed skill does not exist, produce a specification:

```
SKILL SPECIFICATION
===================
Name: [proposed-skill-name]

Purpose: [One sentence description]

Triggers:
- "When user asks to [action]"
- "When working with [file-type/domain]"

Core Functionality:
1. [Primary capability]
2. [Secondary capability]

Resources Needed:
- Scripts: [Code to include]
- References: [Documentation needed]

Integration Points:
- Inputs from: [upstream skills]
- Outputs to: [downstream skills]
```

**Full templates:** See `references/skill-templates.md` for complete skill creation templates by category (document processing, data transformation, automation, API integration).

## Skill Discovery Checklist

When analyzing any task, verify:

- [ ] Input handling covered
- [ ] Processing capabilities adequate
- [ ] Output generation handled
- [ ] Error handling included
- [ ] Validation skills included
- [ ] Automation possible where beneficial
- [ ] Appropriate complexity level for user

## Detailed References

Drill into these files when you need full detail:

| File | Content | When to Read |
|---|---|---|
| `references/skill-patterns.md` | Skill combinations by domain, dependency patterns, anti-patterns, decision trees | Recommending skills for a specific domain or workflow |
| `references/skill-templates.md` | Templates for creating document processing, data transformation, automation, and API integration skills | Creating a new skill that does not exist yet |

## Scripts

| Script | Purpose | Usage |
|---|---|---|
| `scripts/skill-analyzer.py` | Automated task requirement analysis and skill mapping | `python skill-analyzer.py` |
| `scripts/validate-identification.py` | Test skill identification accuracy across scenarios | `python validate-identification.py [optional-task-description]` |
