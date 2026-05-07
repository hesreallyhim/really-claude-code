# Squad Formation Profile: [plugin-name]

**Date:** [YYYY-MM-DD]
**Source plugin:** `[catalog]/plugins/[plugin-name]` (v[version])
**Domain:** [one-line domain summary]

---

## Part A: Formation Analysis

> **Quick Reference**
> | | |
> |---|---|
> | **Formation** | [structure type] |
> | **Squads** | [squad-name] ([N] workers, [topology]) [+ more squads] |
> | **Total agents** | [N] workers + [N] squad-leaders + 1 team-lead |
> | **Key sync** | [sync point names with required/optional] |
> | **Ready** | [YES / NO -- blockers] |
> | **Best for** | [scenario types from Scenario Mapping] |

### Candidacy Assessment

| Criterion | Value | Rating |
|-----------|-------|--------|
| Component count | [N] agents, [N] skills, [N] hooks, [N] commands | [HIGH/MEDIUM/LOW] |
| Role diversity | [archetypes present] | [HIGH/MEDIUM/LOW] |
| Skill complementarity | [overlap assessment] | [HIGH/MEDIUM/LOW] |
| Domain complexity | [complexity factors] | [HIGH/MEDIUM/LOW] |
| Parallelism potential | [parallelism description] | [HIGH/MEDIUM/LOW] |
| **Candidacy verdict** | **[STRONG / MODERATE / WEAK / NOT SUITABLE]** | |

### Scenario Mapping

| Scenario Type | Description | Pattern Fit |
|---------------|-------------|-------------|
| **Primary:** [scenario] | [description] | [pattern and formation style] |
| **Secondary:** [scenario] | [description] | [pattern and formation style] |
| **Tertiary:** [scenario] | [description] | [pattern and formation style] |

### Pattern Recommendation

| Level | Pattern | Topology | Rationale |
|-------|---------|----------|-----------|
| **Team-lead** | [pattern] | [topology] | [why] |
| **Squad 1: [name]** | [pattern] | [topology] | [why] |
| **Squad 2: [name]** | [pattern] | [topology] | [why] |

**Alternatives considered:**
- [pattern]: Rejected -- [reason]

### Agent Role Mapping

#### Squad 1: [name] ([N] workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Context Pressure | Rationale |
|---|---|---|---|---|---|
| [agent-name] | [archetype] | [role description] | [opus/sonnet/haiku] | [HIGH/MEDIUM/LOW] | [why this model] |

#### Squad 2: [name] ([N] workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Context Pressure | Rationale |
|---|---|---|---|---|---|
| [agent-name] | [archetype] | [role description] | [opus/sonnet/haiku] | [HIGH/MEDIUM/LOW] | [why this model] |

Context pressure: HIGH (likely to approach context limits), MEDIUM (moderate usage), LOW (completes comfortably).

### Skill Distribution

| Skill | Assigned To | Squad | Shared? |
|-------|-------------|-------|---------|
| [skill-name] | [agent-name] | [squad] | [No / Yes -- shared with [agent-name] for [purpose]] |

### Skill Gaps

| Gap | Impact | Resolution |
|-----|--------|------------|
| [missing capability] | [which agent is affected] | [source from another plugin / create new / accept gap] |

### Task Graph

```
Phase: PREP
-----------
Task 1: [description]
  -> Owner: [agent-name] ([squad])
  -> Done when: [acceptance criterion]

Task 2: [description]
  -> Owner: [agent-name] ([squad])
  -> Parallel with: [task numbers]
  -> Done when: [acceptance criterion]

═══ SYNC POINT: [name] ([artifact description]) ═══

Phase: CORE
-----------
Task N: [description]
  -> Owner: [agent-name] ([squad])
  -> Blocked by: [task numbers]
  -> Done when: [acceptance criterion]

═══ SYNC POINT: [name] ([artifact description], optional) ═══

Phase: CONVERGENCE
------------------
Task N: [description]
  -> Owner: [agent-name] ([squad])
  -> Blocked by: [task numbers]
  -> Done when: [acceptance criterion]

═══ CONVERGENCE: [description] ═══
```

### Sync Point Details

#### SP1: [name]

| Field | Value |
|-------|-------|
| Initiated by | [agent-name] ([squad]) |
| Validated by | [agent-name] ([squad]) |
| Artifact format | [markdown / yaml / json / directory] |
| Minimum content | [what must be in the artifact for the sync to pass] |
| Gate condition | [what must be true for downstream to proceed] |
| Failure action | [what happens if the artifact is incomplete or rejected] |

#### SP2: [name] (optional)

| Field | Value |
|-------|-------|
| Initiated by | [agent-name] ([squad]) |
| Validated by | [agent-name] ([squad]) |
| Artifact format | [format] |
| Minimum content | [requirements] |
| Gate condition | [condition, or "None (informational)"] |
| Failure action | [action] |

### Convergence Protocol

| Field | Value |
|-------|-------|
| Driver | [who initiates convergence] |
| Participants | [agent from each squad involved in reconciliation] |
| Artifacts compared | [what is being compared] |
| Method | [how comparison is performed] |
| Success criteria | [what constitutes successful convergence] |
| On discrepancy | [what happens for each type of mismatch] |
| Max iterations | [iteration limit before escalation] |
| Output artifact | [what convergence produces] |

### Coordination Overhead

| Metric | Value |
|--------|-------|
| Squad-leaders needed | [N] |
| Design phase | [FULL / SHORT-CIRCUIT -- reason] |
| Announcer needed | [YES/NO -- reason] |
| Total communication channels | [N] ([breakdown]) |
| Flat mesh equivalent | [N] channels |
| **Channel reduction** | **[N]%** |

### Risks

| Risk | Mitigation |
|------|------------|
| [risk description] | [mitigation strategy] |

---

## Part B: Squad Configuration

```yaml
formation:
  name: [formation-name]
  plugin: [plugin-name]
  version: [plugin-version]
  structure: [single-squad / two-squad-diverge-converge / multi-squad]
  task: "[overall mission description]"
  ready_to_proceed: true  # false if skill_gaps have no source_candidate or spawn_type is unresolved

  team_lead:
    pattern: [pattern-name]
    topology: [topology-name]
    channels: [N]

  squads:
    - name: [squad-name]
      task: "[squad-level task for spawn request]"
      pattern: [pattern-name]
      topology: [mesh / hub-and-spoke / pipeline / star]
      channels: [N]
      briefing_context: |
        [Domain context, constraints, key relationships, and deliverables
         that all squad members need to know. 3-5 sentences.]
      leader:
        agent: squad-leader
        model: [opus/sonnet/haiku]
        design_phase: [full / short-circuit]
      workers:
        - name: [agent-name]
          source_agent: [plugin agent name]   # documentary: traces lineage to source plugin
          spawn_type: [installed agent type]   # operational: agent type from ~/.claude/agents/
          model: [opus/sonnet/haiku]
          model_rationale: "[optional: brief phrase explaining model choice]"
          archetype: [architect/investigator/implementer/critic/specialist/documenter]
          skills:
            - name: [skill-name]
            - name: [skill-name]
              shared_with: [agent-name]  # also assigned to this agent (typically cross-squad)
          role: "[one-sentence role description]"
          briefing_context: |
            [Optional: agent-specific assignment, starting task, peer dependencies.
             2-3 sentences. Omit if squad-level context is sufficient.]

  sync_points:
    # Directional: one squad produces, the other consumes
    - name: [sync-point-name]
      type: artifact-transfer
      from: [squad-name]
      to: [squad-name]
      artifact: [artifact description]
      required: true
      initiated_by: [agent-name]
      validated_by: [agent-name]
      minimum_content:
        - [required element]
        - [required element]

    # Bidirectional: both squads participate symmetrically
    - name: [sync-point-name]
      type: bidirectional-check
      between: [squad-1, squad-2]
      artifact: [artifact description]
      required: false

    # sync_points schema:
    #   type: artifact-transfer   -> requires from + to (directional)
    #   type: bidirectional-check -> requires between (list of 2 squads)
    #   type: gate                -> requires from + to + gate_condition

  skill_gaps:
    - domain: [capability domain]
      affects: [agent-name]
      source_candidate: [plugin name or "create new"]
```

---

## Part C: Pattern Rationale

[2-3 paragraphs explaining:
- Why this workstream split was chosen over alternatives
- What makes the intra-squad patterns appropriate for each squad's work style
- What scenario types this formation excels at and where it would be over-engineered
- Any notable design choices (e.g., agents that could go in either squad, prep work during design phase)]

### Formation Variants (optional)

| Scenario | Variant | Changes from default |
|----------|---------|---------------------|
| [simpler scenario] | [reduced formation] | [what to drop/merge] |
