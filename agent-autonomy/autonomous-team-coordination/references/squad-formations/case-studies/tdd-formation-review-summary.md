# TDD Formation Review: Combined Evaluation Summary

**Date:** 2026-02-14
**Reviewers:** reviewer-a (Squad A evaluation), reviewer-b (Squad B evaluation)
**Convergence coordinator:** convergence-coordinator
**Formations reviewed:**
- Squad A: Veridian -- Steel-thread zero-trust auth broker (Go/K8s/Vault, 1 month, 9 agents)
- Squad B: Atreus -- Enterprise implantable cardiac monitor (Firmware+Cloud+AI/ML+Dashboard, 1 year, 16 agents)

---

## 1. Combined Score Table

| Dimension | Squad A (Veridian) | Squad B (Atreus) | Notes |
|-----------|-------------------|------------------|-------|
| **Completeness** | 9/10 | 9/10 | Both formations comprehensively address their scenario requirements. Squad A covers all steel-thread deliverables plus compliance. Squad B covers 4 codebases, 6 regulatory frameworks, and cross-boundary E2E. |
| **Correctness** | 8/10 | 8/10 | Both have structural soundness with minor issues. Squad A: SP1 directionality inconsistency (bidirectional gate modeled as `from:/to:`). Squad B: firmware-test-vectors sync inconsistency (YAML sends to V&V but planning doc says Cloud consumes them). |
| **Efficiency** | 7/10 | 7/10 | Both formations are appropriately complex but slightly over-staffed. See cross-evaluation notes below. |
| **Actionability** | 8/10 | 8/10 | Both produce deployable YAML configurations with clear task graphs. Squad A's 15-task graph with correct dependencies is the strongest single artifact. Squad B's multi-phase 24-task graph is proportionally thorough. |

### Cross-Evaluation Notes on Efficiency

During convergence, each reviewer argued the *other* formation had the worse efficiency problem:

- **Reviewer-a** argued Squad B's efficiency should be 6/10 because 16 agents with phase-specific idleness (dhf-assembler idle during Core, 6 workers idle during Foundation) means absolute token waste compounds at scale.
- **Reviewer-b** argued Squad A's efficiency should be 6/10 because 9 agents for a single-codebase Go operator with one golden path is proportionally heavier than 16 agents for a 4-codebase, 6-regulation project.

**Resolution:** Both efficiency scores remain at 7/10. The cross-evaluators each identified genuine issues but lacked the deep context of the primary reviewer to fully weigh the mitigating factors. The disagreement itself is informative -- it demonstrates that efficiency scoring benefits from cross-evaluation, and future reviews should include a cross-evaluation step.

---

## 2. Cross-Formation Analysis

### 2.1 Standout Strengths

**Squad A -- Scope fence as structural mechanism.** The scope-fence-author creates an explicit organizational structure for saying "this is what we are NOT doing." This is not just documentation -- it is a governance mechanism that converts scope-creep impulses into documented exclusions. Both reviewers identified this as the most transferable insight from Squad A.

**Squad B -- Three-layer AI/ML validation.** The golden-model snapshot tests, statistical validation suite, and predetermined change control plan test infrastructure represent a sophisticated approach to "TDD for ML" that honestly acknowledges TDD does not apply to model development in a conventional sense. The pair topology for Squad-AI/ML (2 workers with complementary skills) is the right structural choice.

**Squad B -- V&V squad as integrating force.** The dedicated V&V squad owns the cross-cutting concerns (E2E test, DHF traceability, test result archival) that no domain squad can own alone. In an IEC 62304 + FDA 510(k) context, this is a structural necessity, not a luxury.

**Squad A -- Task graph quality.** 15 tasks with explicit dependencies, parallel-with annotations, phase boundaries, and done-when criteria. This is the most immediately deployable artifact across both formations.

### 2.2 Common Weaknesses

**No Critic/Reviewer agent in either formation.** This is the most consequential finding that applies to both formations. Both operate in safety/security-critical domains, yet neither includes an agent whose role is to verify that tests assert the right properties -- not just that they pass. Squad A explicitly rejected adversarial (Red/Blue) patterns as too narrow for a steel thread, but this conflated a full Red Team (overkill) with any review pressure (necessary). Squad B's safety-critical IEC 62304 Class C context makes the absence even more notable.

Both reviewers converged on this finding independently: reviewer-b flagged it during primary evaluation, and reviewer-a acknowledged during convergence that it should have been weighted more heavily in the Squad A evaluation.

**Agent utilization gaps across phases.** Neither formation analyzes which agents are active during which phases. Squad A's scope-fence-author has thin workload (approximately 3 tasks, primarily in Prep and Convergence). Squad B's dhf-assembler is idle during the entire Core phase. These are invisible in the current formation design process because formations are designed as snapshots of team composition rather than timelines of agent activity.

**Sync point modeling inconsistencies.** Both formations have divergences between the planning document prose and the YAML sync point configuration:
- Squad A: SP1 (`prep-complete`) is a bidirectional gate between both squads but is modeled with directional `from:/to:` fields.
- Squad B: `firmware-test-vectors` sync point sends from Squad-Firmware to Squad-V&V in YAML, but the planning doc states Squad-Cloud consumes BLE protocol test vectors for relay-side testing.

These are template expressiveness problems, not planning failures.

**Additive bias in role assignment.** Both formations default to one-responsibility-per-agent without a counterbalancing mechanism to merge thin roles. The planning template asks "what roles do we need?" but never asks "can any of these roles be combined?" or "what is the minimum agent count that covers all responsibilities?" This is a known cognitive bias in organizational design that the current process does not counteract.

### 2.3 Missing Structural Mechanism in Squad B

Reviewer-a's scope-fence insight exposed a gap in Squad B: there is no explicit scope governance mechanism for a multi-squad, one-year formation where scope creep is a severe risk. The V&V squad's traceability matrix implicitly constrains scope (tests that don't map to requirements are arguably out of scope), but this is discovered at convergence time, not enforced proactively.

**Recommendation:** Squad B should add a "Test Scope Document" produced during the Foundation phase that, for each squad, lists: (a) what is in scope for 510(k), (b) what is explicitly deferred to post-submission, and (c) the rationale for each deferral. This generalizes Squad A's scope fence for multi-squad contexts.

---

## 3. Systematic Biases in the Formation Design Process

The convergence discussion surfaced three systematic tendencies that affect all formations, not just these two:

| Bias | Description | Evidence |
|------|-------------|----------|
| **Additive bias** | Roles are added but never merged or questioned. No mechanism pushes back against agent count. | Squad A: 9 agents for 1-month single-codebase project. Squad B: dhf-assembler idle during Core phase. Neither formation documents a "why NOT this agent?" analysis. |
| **Template-driven modeling artifacts** | The sync point schema forces `from:/to:` directionality on flows that are bidirectional or multi-party, producing inconsistencies between prose and YAML. | SP1 directionality in Squad A. Firmware-test-vectors destination mismatch in Squad B. |
| **Absent verification pressure** | The process optimizes for coverage (are all deliverables assigned?) but not for correctness verification (are the deliverables right?). | No Critic/Reviewer agent in either formation despite safety/security-critical domains. Review mechanisms are limited to squad leaders, who are Architect archetypes, not Critics. |

---

## 4. Actionable Changes

### Change 1: Require a Planning Doc as an Intermediate Step Before Profile Authoring

**What to change:** Make the pre-spec planning document (the `tdd.md` template populated for a specific scenario, e.g., `tdd-steel-thread-security.md` or `tdd-enterprise-medical.md`) a mandatory prerequisite before writing the Squad Formation Profile. Currently, both artifacts exist for these formations, but there is no process requirement that the planning doc must come first.

**Why:** The planning doc forces top-down derivation: scenario classification -> team responsibilities -> team dependencies -> squad composition. This is the primary defense against additive bias, because agent roles are derived from responsibilities rather than invented from a role catalog. Both reviewers independently ranked this as the highest-impact process improvement. The planning docs for both formations are the strongest artifacts in the submission -- the domain reasoning, scope definition, and constraint identification in these documents are what make the profiles possible.

**How to implement:**
1. Add a "Prerequisites" section to `SQUAD-PROFILE.TEMPLATE.md` that requires a link to a completed planning doc (using the `tdd.md` template structure).
2. The planning doc must include: (a) the "Given" classification, (b) "The squads must" responsibilities derived from the classification, (c) "Must have" dependencies, and (d) a functional squad description -- all before any agent-level design begins.
3. Profile reviewers should verify that every agent in the profile traces back to a responsibility in the planning doc. Agents that cannot trace to a planning-doc responsibility should be flagged for justification or removal.
4. Add a "Why not?" analysis section to the profile template: for any responsibility that was considered for a dedicated agent but was instead absorbed by an existing agent, document the rationale.

### Change 2: Add Agent Utilization Analysis and Review Gate Sections to the Profile Template

**What to change:** Add two new required sections to `SQUAD-PROFILE.TEMPLATE.md`:

**(A) Agent Utilization Matrix** -- A table showing each agent's activity level (active, light, idle) during each phase of the task graph. This makes phase-specific idleness visible at design time rather than discoverable only during review.

**(B) Review Gate Specification** -- For formations operating in safety-critical, security-critical, or regulated domains, a section that explicitly defines who reviews what and when. This must go beyond squad-leader oversight to address the question: "Who verifies that tests assert the right properties, not just that they pass?"

**Why:** The utilization matrix addresses the systematic blind spot both reviewers identified: formations are designed as team snapshots, not as timelines of agent activity. A simple phase-by-phase table would have surfaced the scope-fence-author thinness in Squad A and the dhf-assembler idleness in Squad B at design time.

The review gate addresses the most consequential shared finding: neither formation includes Critic/Reviewer pressure despite operating in safety/security-critical domains. Making review gates an explicit template section forces formation authors to answer "who checks the checkers?" rather than assuming squad-leader review is sufficient.

**How to implement:**
1. Add an "Agent Utilization Matrix" section after the Task Graph in `SQUAD-PROFILE.TEMPLATE.md` with the following structure:

```
| Agent | Foundation | Core | Integration | Convergence | Utilization Notes |
|-------|-----------|------|-------------|-------------|-------------------|
| agent-name | Active (Tasks 1,3) | Light (Task 11) | Idle | Active (Task 14) | Consider merging with X if idle > 1 phase |
```

2. Add a "Review Gates" section after Sync Point Details:

```
| Review Target | Reviewer | Review Scope | Trigger |
|---------------|----------|--------------|---------|
| Test assertions (security properties) | [agent or role] | Verify tests assert correct properties, not just pass | After each Core phase task completion |
```

3. For the utilization matrix: flag any agent that is idle for more than one phase as a candidate for merging with another agent. Require a written justification if the agent is retained despite multi-phase idleness.
4. For review gates: make this section required when the domain classification includes "security-related," "embedded systems," or maturity level is "enterprise-ready" or "enterprise in high-regulation." Make it optional otherwise.

### Change 3: Add `between:` Support and Consistency Validation to the Sync Point Schema

**What to change:** Extend the YAML sync point schema to support three sync point topologies instead of two, and add a consistency check between the planning document prose and the YAML configuration.

**Current schema supports:**
- `from:/to:` -- directional artifact transfer (one squad sends to another)
- `between:` -- exists in some sync points (e.g., Squad A's `core-review`) but is not consistently used

**Proposed schema:**
- `from:/to:` -- directional artifact transfer (exactly one sender, one or more receivers)
- `between:` -- bidirectional check or multi-party gate (all listed squads participate as both senders and receivers)
- `participants:` -- multi-party gate where different squads play different roles (e.g., one squad initiates, another validates, a third provides artifacts)

**Why:** Both formations have sync point inconsistencies that stem from the template forcing directional modeling on non-directional flows. Squad A's SP1 is a multi-party gate where both squads contribute artifacts and both validate -- but the YAML models it as `from: squad-implement / to: squad-scaffold`, which misrepresents the data flow. Squad B's firmware-test-vectors sync point lists V&V as the receiver in YAML but Cloud as the consumer in the planning doc, because the actual flow is one-to-many but the schema only supports one-to-one.

**How to implement:**
1. Update the sync point schema in `SQUAD-PROFILE.TEMPLATE.md` to document three supported topologies with examples:
   - **Directional** (`from:/to:`): Used when one squad produces an artifact and one or more other squads consume it. Example: `model-artifact-handoff` (Squad-AI/ML -> Squad-Firmware).
   - **Bidirectional** (`between:`): Used when all participating squads both contribute and consume artifacts. Example: `core-review` (Squad-Implement and Squad-Scaffold exchange test results and scope fence updates).
   - **Multi-party** (`participants:`): Used when multiple squads participate with different roles (initiator, validator, contributor). Example: `prep-complete` where Squad-Implement initiates, Squad-Scaffold validates, and both contribute artifacts.
2. Add a `consumers:` field for directional sync points that have multiple downstream consumers, allowing `from: squad-firmware / to: squad-vv / consumers: [squad-vv, squad-cloud]` to model the firmware-test-vectors flow accurately.
3. Add a validation checklist to the profile template: "For each sync point, verify that the YAML `from:/to:/between:` fields match the prose description of the artifact flow in the Sync Point Details table."

### Change 4: Implement a Pre-Flight Formation Sizing Check

**What to change:** Add a lightweight sizing heuristic to the formation design process that serves as an early warning for over-staffing, applied before detailed agent role mapping begins.

**Why:** Both formations are slightly over-staffed relative to their parallel work capacity. Squad A has 5 parallel prep tasks but 6 workers, and the Core phase has only 3 truly parallel work streams. Squad B has 5 Foundation tasks but 11 workers. The additive bias in role assignment means formations tend to grow without a counterbalancing force. A sizing heuristic provides that force -- not as a hard constraint, but as a smell test that triggers justification.

**How to implement:**
1. After completing the planning doc and before starting agent role mapping, apply the following checks:
   - **Parallel work stream count:** For each phase, count the maximum number of truly independent tasks. If the worker count exceeds the maximum parallel work stream count by more than 50%, flag for review.
   - **Deliverable-to-agent ratio:** Count the major deliverables in the planning doc. If the total agent count (workers only, excluding leaders) exceeds `(deliverables * 0.6) + squad_count`, flag for review.
   - **Phase utilization forecast:** For each proposed agent, estimate activity across phases. If more than 25% of agents are idle for more than one phase, flag for review.
2. Flagged formations are not automatically rejected -- they require a written justification explaining why the agent count is necessary despite the flag. Valid justifications include: skill non-overlap (e.g., Rust and C testing require different agents), regulatory mandate (e.g., IEC 62304 requires independent verification), or domain complexity (e.g., AI/ML validation is a fundamentally different discipline from test automation).
3. Complement the heuristic with an optional cost model: for formations that pass the heuristic but still feel heavy, estimate opus-hours vs. sonnet-hours across the timeline to make the cost of over-staffing concrete.

### Change 5: Generalize the Scope Fence Pattern as a Formation-Level Practice

**What to change:** Extract Squad A's scope-fence-author concept into a generalizable practice that applies to all formations, adapted for different scales and contexts.

**Why:** Reviewer-b identified during convergence that Squad B lacks an explicit scope governance mechanism despite being a one-year enterprise formation where scope creep is a severe risk. Squad A's scope fence is the standout structural insight from the entire exercise, but it is currently specific to the steel-thread methodology. The pattern -- a first-class artifact that documents what is explicitly NOT in scope, with rationale and forward plans -- is valuable at every scale.

**How to implement:**
1. Add a "Scope Governance" section to `SQUAD-PROFILE.TEMPLATE.md` that requires:
   - **Scope document type:** Scope Fence (for focused, time-constrained projects), Test Scope Document (for multi-squad formations), or Regulatory Scope Matrix (for regulated domains mapping scope to regulatory requirements).
   - **Owner:** Which agent or role is responsible for maintaining the scope document.
   - **Trigger for updates:** When does the scope document get updated? (e.g., "when any worker identifies an out-of-scope edge case," "at each sync point," "when regulatory requirements change").
   - **Review cadence:** Who reviews the scope document and how often.
2. For steel-thread formations: retain the scope-fence-author as a dedicated role (or merged into a documenter agent that also handles other documentation).
3. For multi-squad enterprise formations: assign scope governance to a squad leader or V&V squad member, with a "Test Scope Document" that lists in-scope vs. deferred items per squad, updated at each sync point.
4. For prototype/MVP formations: a lightweight scope note in the task graph (no dedicated agent or artifact) that captures the top 5 things the team will NOT do.

---

## 5. Reviewer Agreement and Disagreements

### Areas of Full Agreement

- Planning doc as mandatory intermediate step (highest-impact change)
- Missing Critic/Reviewer agent is the most consequential shared finding
- Sync point inconsistencies are template problems, not planning failures
- Additive bias is a systematic tendency in formation design
- Scope fence should be generalized beyond steel-thread contexts
- Template gate schema needs `between:` support

### Areas of Productive Disagreement

| Topic | Reviewer A Position | Reviewer B Position | Resolution |
|-------|-------------------|-------------------|------------|
| Which formation has worse efficiency | Squad B should be 6/10 (absolute waste compounds at scale) | Squad A should be 6/10 (proportionally heavier for its scope) | Both remain 7/10; disagreement demonstrates value of cross-evaluation |
| Cost model vs. workload analysis priority | Cost model is secondary to pre-flight heuristic | Workload analysis per agent is Tier 1 | Combined into Change 4 (pre-flight check includes phase utilization forecast) |
| Agent-to-human-role mapping | Not ranked; specific to enterprise scenarios | Moderate impact; valuable for formations with specified human team structures | Made optional in template, required when scenario specifies human team size |

---

## 6. Recommendations for Future Review Exercises

1. **Include cross-evaluation.** Each reviewer should briefly evaluate the other's formation to surface the kind of insights that emerged during convergence (e.g., reviewer-a's efficiency critique of Squad B, reviewer-b's scope-governance gap observation).
2. **Score efficiency with a phase-by-phase lens.** The current efficiency score is a single number. A per-phase efficiency breakdown would catch the utilization gaps both reviewers identified.
3. **Test the scoring rubric at scale extremes.** The identical 9/8/7/8 scores for formations of radically different scales suggests the rubric may need a scale-awareness dimension, or at minimum, reviewers should explicitly state whether they are scoring relative to scenario complexity or on an absolute scale.
4. **Pair reviewers with complementary domain backgrounds.** Reviewer-b's regulated-domain expertise surfaced the Critic/Reviewer gap that reviewer-a's process-focused lens initially underweighted. Deliberate pairing increases coverage.
