# Example Team Design: Legacy Codebase Migration

A complete team design for migrating a Python 2 monolith to a Python 3 modular architecture. Demonstrates the Strangler Fig + Enabling Team pattern with pipeline topology.

---

## TEAM DESIGN: Legacy Migration Pipeline

### Situation Analysis

```
SITUATION ANALYSIS
==================
Task: Migrate a 150k-line Python 2.7 Django monolith to Python 3.12 with modular architecture
Domain: Backend services, e-commerce platform
Urgency: Normal (planned work, EOL-driven deadline but not emergency)
Complexity: Complex-entangled (deep coupling between modules, implicit dependencies, minimal test coverage)
Knowledge needs: Concentrated (2 engineers wrote 80% of the legacy code; they left 2 years ago)
Risk tolerance: Low (production e-commerce system, revenue-critical)
Scale: ~150k lines, 40+ Django apps, 200+ database tables
Duration: Multi-phase (estimated 6-9 months)
```

### Pattern Selection

**Primary pattern:** Strangler Fig (Pattern 7) for incremental migration
**Secondary pattern:** Enabling Team (from Team Topologies 1.7.2) for knowledge transfer
**Overlay:** Reflection/Self-Critique (Pattern 12) on every migration step

**Justification:** Low risk tolerance eliminates any "big bang" rewrite approach. Strangler Fig allows incremental replacement while maintaining production stability. The concentrated (and lost) knowledge problem requires an enabling team approach: an analysis phase to reconstruct understanding before any migration begins. Reflection loops ensure behavioral parity between old and new code.

**Communication topology:** Pipeline (analyze -> test -> migrate -> validate -> deploy) + Hub-and-spoke (migration architect coordinates).

### Topology Diagram

```
  Pipeline Flow:
  ==============

  +----------+     +----------+     +----------+     +----------+     +----------+
  | ANALYZE   +---->| TEST      +---->| MIGRATE   +---->| VALIDATE  +---->| DEPLOY    |
  | (map code)|     | (safety   |     | (convert  |     | (parity   |     | (route    |
  |           |     |  net)     |     |  module)  |     |  check)   |     |  traffic) |
  +-----+----+     +-----+----+     +-----+----+     +-----+----+     +-----+----+
        |                |                |                |                |
        +----------------+----------------+----------------+----------------+
                                     |
                              +------+------+
                              | MIGRATION    |
                              | ARCHITECT    |
                              | (coordinator)|
                              +-------------+
```

### Agents

#### Role 1: Migration Architect (Coordinator)
- **Type:** existing -- `solid-architect`
- **Responsibilities:** Defines migration strategy and module priority order. Maintains the routing/facade layer. Coordinates the pipeline. Decides when a module is "done" and traffic can be fully routed to the new version. Reports progress.
- **Skills needed:** team-patterns (existing)
- **Model:** opus (strategic decisions about migration order, dependency analysis, risk assessment)
- **Communicates with:** All agents (hub). Sets priorities, reviews progress, makes go/no-go decisions.

#### Role 2: Legacy Analyzer
- **Type:** existing -- `complexity-reducer`
- **Responsibilities:** Maps the legacy codebase: module boundaries, dependency graph, hotspots (high complexity + high change frequency), implicit coupling. Produces a migration priority map. Reconstructs undocumented business logic.
- **Skills needed:** None beyond base capabilities
- **Model:** opus (understanding undocumented, complex legacy code requires deep reasoning)
- **Communicates with:** Migration Architect (reports findings). Test Engineer (identifies what needs testing first).

#### Role 3: Test Engineer
- **Type:** existing -- `testing-expert`
- **Responsibilities:** Builds the safety net of automated tests before any migration begins. Creates characterization tests that capture current behavior (even if that behavior is buggy). Writes behavioral parity tests that run against both old and new implementations.
- **Skills needed:** None beyond base capabilities
- **Model:** sonnet (test generation is high-volume, pattern-based work)
- **Communicates with:** Migration Architect, Legacy Analyzer (needs analysis output), Migration Engineer (parity tests).

#### Role 4: Migration Engineer
- **Type:** existing -- `independent-contributor` (opus variant)
- **Responsibilities:** Converts modules from Python 2 to Python 3. Refactors toward modular architecture. Updates dependencies. Ensures the facade/routing layer correctly directs traffic.
- **Skills needed:** None beyond base capabilities
- **Model:** opus (migration of complex, entangled code requires careful reasoning about behavioral equivalence)
- **Communicates with:** Migration Architect (receives module assignments), Test Engineer (runs parity tests), Parity Validator.

#### Role 5: Parity Validator
- **Type:** existing -- `critical-code-reviewer`
- **Responsibilities:** Validates that migrated modules produce identical outputs to the legacy versions. Runs comparison tests. Reviews migration diffs for subtle behavioral changes. Acts as the reflection/critique loop.
- **Skills needed:** None beyond base capabilities
- **Model:** opus (catching subtle behavioral differences requires deep code analysis)
- **Communicates with:** Migration Engineer (reviews their work), Migration Architect (reports parity status).

### Task Dependency Graph

```
  Phase 0: Discovery (Enabling Team mode)
  Task 1: Map legacy codebase structure + dependencies    -->  Owner: Legacy Analyzer
  Task 2: Identify hotspots + migration priority order    -->  Owner: Legacy Analyzer (blocked by: 1)
  Task 3: Define migration strategy + module sequence     -->  Owner: Migration Architect (blocked by: 2)

  Phase 1: Safety Net
  Task 4: Write characterization tests for Module 1       -->  Owner: Test Engineer (blocked by: 3)
  Task 5: Write parity test harness                       -->  Owner: Test Engineer (parallel with: 4)

  Phase 2: First Module Migration (repeat for each module)
  Task 6: Migrate Module 1 to Python 3                    -->  Owner: Migration Engineer (blocked by: 4,5)
  Task 7: Run parity tests on Module 1                    -->  Owner: Parity Validator (blocked by: 6)
  Task 8: Route traffic to new Module 1 (feature flag)    -->  Owner: Migration Architect (blocked by: 7)
  Task 9: Monitor + validate in production                -->  Owner: Parity Validator (blocked by: 8)

  Phase 3: Iterate (Tasks 4-9 repeat for each module)
  ...

  Phase N: Decommission
  Task N: Remove legacy code + facade layer               -->  Owner: Migration Engineer
  Task N+1: Final validation                              -->  Owner: Parity Validator
```

### Agent Count Justification

**Total agents: 5**

Communication channels in hub-and-spoke: 4 (one per spoke to architect). The pipeline structure further reduces communication needs since agents primarily pass work to the next stage rather than communicating freely.

5 agents is within the optimal range (Harvard: 4.6 optimal). The pipeline pattern means agents are not all active simultaneously -- the Legacy Analyzer's work front-loads, then the Test Engineer and Migration Engineer take over. This natural phasing reduces effective concurrent coordination needs.

### Capability Gap Assessment

**Minor gap:** No dedicated DevOps agent for managing dual infrastructure (old and new running in parallel) and feature flag routing. The Migration Architect handles this, but for a larger migration, a dedicated agent would reduce architect cognitive load.

**Recommendation:** If the migration involves infrastructure changes (e.g., moving from bare metal to containers), consider adding a DevOps agent or using the `release-manager` agent for deployment coordination.

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Stalled migration (dual-system indefinitely) | Migration Architect maintains a visible progress tracker. Each module has a target date. Weekly progress reviews. |
| Undocumented business logic surprises | Phase 0 (Discovery) is dedicated to mapping the codebase. Characterization tests capture actual behavior before migration. Legacy Analyzer uses opus model for deep understanding. |
| Test coverage insufficient for safe migration | Test Engineer builds characterization tests first. Parity Validator runs comparison tests on every migration. No module goes live without passing parity. |
| Concentrated knowledge (original devs gone) | This is why the Legacy Analyzer role uses opus: it needs to reconstruct understanding from code alone. The analysis phase (Tasks 1-3) is explicitly time-boxed and documented. |
| Feature flag complexity accumulates | Migration Architect tracks all active feature flags. Each fully-migrated module has its flag removed within 1 sprint of full traffic routing. |

### Execution Readiness

**READY.** All roles can be filled by existing agents:
- `solid-architect` as Migration Architect
- `complexity-reducer` as Legacy Analyzer
- `testing-expert` as Test Engineer
- `independent-contributor` (opus) as Migration Engineer
- `critical-code-reviewer` as Parity Validator
