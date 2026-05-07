# Squad Formation Profile: [plugin-name]

**Date:** [YYYY-MM-DD]
**Source plugin:** `[catalog]/plugins/[plugin-name]` (v[version])
**Domain:** [one-line domain summary]

---

## Quick Reference

| | |
|---|---|
| **Formation** | [structure type] |
| **Squads** | [squad-name] ([N] workers, [topology]) [+ more squads] |
| **Total agents** | [N] workers + [N] squad-leaders + 1 team-lead |
| **Key sync** | [sync point names with required/optional] |
| **Output root** | [where the squad's deliverables persist; see Operational Rules §C2] |
| **Ready** | [YES / NO -- blockers] |
| **Best for** | [scenario types from Scenario Mapping] |

---

## Part A: Formation Analysis

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

  output_root: "[review-output-root | feature-output-root | etc. — persistent path, NOT /tmp]"

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
          spawn_type_has_sendmessage: true     # MUST be true; substitute if false (see Operational Rules §C1)
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

## Part C: Operational Contracts

Part A describes the squad's *shape*; Part C describes the *contracts* every member operates under. A profile without contracts produces variable, hard-to-merge output even when the formation is right.

### C1. Output Contract (every worker)

The contract every worker is bound to. Inline this verbatim into every role prompt's preamble (see Part D).

```
[OPERATIONAL CONSTRAINTS]
- [What workers may NOT touch in the project, e.g. "Do NOT edit, create, or
  modify any file in the plugin under review. Static analysis only."]
- [Where workers MAY write, e.g. "You MAY write your final report to
  <output-root>/<component>.md."]

[SEVERITY RUBRIC]  (or equivalent quality/category framing for non-review squads)
- [TIER 1]: [definition + ship-blocking implication]
- [TIER 2]: [definition + recommended-fix implication]
- [TIER 3]: [definition + polish implication]

[OUTPUT SCHEMA]
- Every <work unit> MUST be a <markdown bullet | YAML entry | JSON object>
  with this exact shape:
  [literal example with all required fields]
- <Work units> missing [required field] will be REJECTED by the synthesizer.
- [Cap rules: e.g., Tier 1 unlimited; Tier 2 ≤ N; Tier 3 ≤ M.]

[FILE LAYOUT]
# <Component-name> <Output-type>

## Summary
<2-4 sentences>

## Tier 1 <items>
<bullets per schema; "None" if zero>

## Tier 2 <items>
<bullets per schema; "None" if zero>

## Tier 3 <items>
<bullets per schema; "None" if zero>

## What's Done Well   ← keep section even on non-review squads to balance critique
<2-5 concrete bullets>

[HONESTY CLAUSE]
If your output is empty / clean / unremarkable, say so plainly. Do NOT
manufacture content to look thorough. Padding is as bad as rubber-stamping.

[COMPLETION SIGNAL]
When you finish, SendMessage <coordinator-name> with: a one-line status,
the absolute path to your output file, and your tier counts. Do not paste
the full report in the message — the coordinator will read the file directly.
```

Adapt the bracketed slots to the squad's domain. The structure is universal; the labels (severity vs. category, findings vs. recommendations, etc.) are profile-specific.

### C2. Cross-Cutting Operational Rules (universal)

These rules apply to every squad regardless of domain. Each was learned the hard way; do not relax without documenting the rationale.

#### Rule R1 — Delivery-Channel: every spawned agent MUST have `SendMessage`

Workers and squad-leaders without `SendMessage` cannot deliver work output, cannot acknowledge `shutdown_request`, and cannot participate in peer coordination. Before honoring any spawn request, the team-lead verifies each `subagent_type` includes `SendMessage`. If not, substitute (typically `general-purpose`) and enforce read-only intent via the worker prompt rather than via tool-list narrowing.

In the YAML config (Part B): every `worker.spawn_type_has_sendmessage` must be `true` before `ready_to_proceed: true`.

See: `commands/squad.md` "Hard Rule" section for the full team-lead enforcement protocol.

#### Rule R2 — Output Persistence: never default to `/tmp`

`/tmp` is volatile. The OS may clean it, it does not survive reboot, and it is invisible to the project tree. Default `<output-root>` to a persistent location:

```
~/.claude/<work-type>-runs/<plugin-slug>/<YYYYMMDD-HHMMSS>/
```

If `/tmp` is used as scratch (e.g., a worker has restricted write paths), the squad-leader's completion protocol MUST copy durable outputs to the persistent location before declaring the run complete. The Quick Reference's "Output root" field is the single source of truth for where deliverables live.

#### Rule R3 — Worktree Isolation: parallel contributors share a tree at their own risk

Multiple worker agents operating in the same git worktree can sweep each other's unstaged WIP into their own commits via `git add` of the wrong path. Mitigations, in order of preference:

1. Spawn each worker with its own `git worktree add` instance.
2. If sharing a worktree, mandate atomic `git add <specific-path>` followed immediately by commit, and `git stash` for any unrelated WIP.
3. In completion messages, the worker reports its commit hashes and the squad-leader spot-checks for cross-scope contamination.

#### Rule R4 — File Scope: workers own files, not findings

When multiple workers fix issues across overlapping topics, partition by **file ownership**, not by **finding type**. Two workers both touching `agents/foo.md` from different angles will conflict; one worker owning `agents/foo.md` entirely will not.

Workers who notice a cross-scope issue must NOT fix it; they flag it back to the squad-leader, who routes to the appropriate owner or to the team-lead.

#### Rule R5 — Lifecycle Coverage: every agent must be reachable for shutdown

Same root as R1. Without `SendMessage`, agents cannot acknowledge `shutdown_request` and must be force-terminated. The harness eventually catches up but it produces noisy logs and slows team teardown. R1 is the prerequisite.

### C3. Profile-Specific Rules (optional)

Add rules that apply to *this* squad but not all squads. Examples: "the synthesizer must run on opus", "no worker may reach the LLM more than 3 times per task", "outputs must include a citation count".

| Rule ID | Statement | Why |
|---------|-----------|-----|
| P1 | [profile-specific rule] | [rationale] |
| P2 | [profile-specific rule] | [rationale] |

---

## Part D: Role Prompt Templates

Part B's `briefing_context` is intentionally thin (3-5 sentences). Part D provides the actual prompts the team-lead will inline into Agent calls when spawning workers. Parameterized with `<placeholders>` so a fresh run substitutes them and ships.

### D0. Common Preamble (inlined into every role)

```
You are <agent-name> on the <squad-name> squad of the <formation-name> formation.

<C1 OUTPUT CONTRACT — pasted verbatim from Part C1>

<TARGET CONTEXT>
- Target under work: <plugin-path | feature-spec | bug-report | etc.>
- Output root: <output-root>
- Coordinator: <squad-leader-name>
- Team-lead: <team-lead-name>

<RECENT-RUN CONTEXT (optional)>
- Notable changes since last run: <one or two sentences>
- Things to specifically check: <if any>
```

### D.1 [Role-name-1] — `<subagent_type>`

```
<paste D0 with <agent-name> = role-1, <squad-name>, etc.>

YOUR FILE / SCOPE OWNERSHIP
You own and may modify ONLY:
- <file-path-1>
- <file-path-2>

Other workers handle other files. Do NOT touch them. If you observe a
cross-scope issue, flag it back to <squad-leader-name>; do not fix it.

YOUR ASSIGNED TASK
<role-specific task: what this role does that no other role does>

<role-specific instructions, references, constraints>

WHEN YOU FINISH
SendMessage <coordinator-name> with: <completion-message-format>
Per R1 you have SendMessage; if for some reason this fails, halt and
flag to team-lead — do not silently complete.
```

### D.2 [Role-name-2] — `<subagent_type>`

[same structure, role-2 specifics]

### D.3 ... [one section per role]

### D.N Squad-Leader (if applicable)

```
<paste D0 with <agent-name> = squad-leader>

YOUR ROLE
You are the squad-leader for <squad-name>. You design and coordinate the
sub-team. You do NOT spawn workers yourself — you send SPAWN REQUEST
messages to the team-lead, who validates per Rule R1 and spawns.

Your consultants are <team-architect-name> and <skill-identifier-name>
(addressable by name via SendMessage).

YOUR PROCESS
1. Consult the team-architect for pattern/topology recommendations.
2. Consult the skill-identifier for capability gap analysis.
3. Synthesize their input into a SPAWN REQUEST to the team-lead.
4. Coordinate workers: assign tasks, receive completions, handle blockers.
5. Send a COMPLETION REPORT to the team-lead when the squad's work ends.

Reference the formation profile at <profile-path> for the canonical task
graph, sync points, and operational rules.
```

---

## Part E: Pattern Rationale

[2-3 paragraphs explaining:
- Why this workstream split was chosen over alternatives
- What makes the intra-squad patterns appropriate for each squad's work style
- What scenario types this formation excels at and where it would be over-engineered
- Any notable design choices (e.g., agents that could go in either squad, prep work during design phase)]

### Formation Variants (optional)

| Scenario | Variant | Changes from default |
|----------|---------|---------------------|
| [simpler scenario] | [reduced formation] | [what to drop/merge] |
| [scaled scenario] | [expanded formation] | [what to add] |

---

## Anti-Patterns and Mitigations

Concrete failure modes observed in this squad's runs. Review this list before spawning to avoid repeating known errors.

| ID | Anti-Pattern | Symptom | Mitigation |
|----|---|---|---|
| AP1 | [name] | [how it shows up] | [how to prevent / what rule applies] |
| AP2 | [name] | [symptom] | [mitigation] |

Common anti-patterns observed across squads (carry forward unless proven irrelevant):

| ID | Anti-Pattern | Mitigation |
|----|---|---|
| AP-COMMON-1 | Worker spawned without `SendMessage`; cannot deliver output | Rule R1; substitute `general-purpose` |
| AP-COMMON-2 | Outputs land in `/tmp/` and are lost on reboot or session end | Rule R2; default `<output-root>` to persistent path |
| AP-COMMON-3 | Parallel workers in shared worktree contaminate each other's commits | Rule R3; per-worker worktree or strict atomic-add discipline |
| AP-COMMON-4 | Workers partitioned by finding-type instead of file-ownership; conflicts | Rule R4; assign by file scope |
| AP-COMMON-5 | Team-lead deletes scratch directory before verifying durable copy | Verify destination `ls` before any `rm -rf` of source |

