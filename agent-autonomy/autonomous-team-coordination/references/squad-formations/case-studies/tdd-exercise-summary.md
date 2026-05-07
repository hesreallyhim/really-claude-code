---
name: TDD Squad Formation Exercise Summary
description: End-to-end summary of the two-squad TDD formation planning exercise, independent evaluation, and convergence review.
date: 2026-02-14
branch: test-crier
---

# TDD Squad Formation Exercise — Summary

## What Happened

Two parallel squads each took a project scenario from `tdd-scenarios.md` and produced a TDD squad formation plan (completed `tdd.md` template variant + detailed squad formation profile following `SQUAD-PROFILE.TEMPLATE.md`). Then two `team-architect` agents evaluated the outputs independently, converged with a `project-manager` coordinator, and wrote a combined review with process improvements.

## The Scenarios

| Squad | Scenario | Maturity | Domain | Timeline | Formation |
|-------|----------|----------|--------|----------|-----------|
| **A** | Veridian (zero-trust auth broker) | Steel Thread | Security | 1 month | 2 squads, 6 workers |
| **B** | Atreus (implantable cardiac monitor) | Enterprise in high-regulation | Embedded + Security | 1 year | 4 squads, 11 workers |

These two were chosen because they represent the widest gap in the parametric space (maturity, domain, timeline) and produce maximally different squad formations.

**Squad A** produced a lean 2-squad formation splitting TDD implementation (hub-and-spoke) from test infrastructure and scope governance (mesh). The standout design decision was making the scope fence a squad-level structural responsibility rather than an individual discipline exercise.

**Squad B** produced a 4-squad formation mirroring the real-world sub-teams (Firmware, Cloud, AI/ML, V&V) with 7 sync points and a dedicated V&V squad owning DHF assembly and end-to-end test orchestration. The standout design decision was the AI/ML three-layer validation approach (golden snapshots + statistical validation + predetermined change control).

## Evaluation Scores

Both formations were independently reviewed by `team-architect` agents and scored identically:

| Criterion | Squad A | Squad B |
|-----------|---------|---------|
| Quality relative to scenario | 9/10 | 9/10 |
| Mastery of squad-orchestration architecture | 8/10 | 8/10 |
| Efficiency of the planning squad | 7/10 | 7/10 |
| Overall evaluation | 8/10 | 8/10 |

### Common Strengths
- Task graphs are realistic with correct dependency chains
- Technical specificity is high (names real technologies, regulations, patterns)
- Sync point design distinguishes hard gates from informational checkpoints
- Formation variants show adaptability thinking

### Common Weaknesses
- No Critic/Reviewer agent in either formation
- Some agents have thin workloads or idle phases
- Sync point YAML inconsistencies with prose descriptions
- Additive bias: tendency to add agents rather than consolidate roles

## Top 5 Actionable Improvements

1. **Require planning doc as intermediate step** — Produce the TDD planning doc first, then derive the profile from it. Forces top-down dependency reasoning before agent assignment.
2. **Add agent utilization matrix and review gates to template** — Track which phases each agent is active in; add explicit review gate mechanism for regulated domains.
3. **Fix sync point schema** — Add `between:` support for bidirectional gates; add consistency validation between YAML and prose.
4. **Implement pre-flight formation sizing heuristic** — Count distinct parallel work streams in prep phase; if parallel prep tasks < workers, formation is over-staffed. Rule of thumb: deliverables / 2 + coordination overhead.
5. **Generalize scope fence pattern** — The structural scope governance from Squad A should be a formation-level practice, not scenario-specific.

## Artifacts

| Commit | Files | Description |
|--------|-------|-------------|
| `54f1b00` | `tdd-steel-thread-security.md`, `tdd-steel-thread-security-profile.md` | Squad A: Veridian formation |
| `1125852` | `tdd-enterprise-medical.md`, `tdd-enterprise-medical-profile.md` | Squad B: Atreus formation |
| `2ae6681` | `tdd-formation-review-summary.md` | Combined evaluation and convergence review |

## Process

```
Phase 1: Formation (parallel)
  Squad A (independent-contributor-opus) ──→ 2 docs, committed
  Squad B (independent-contributor-opus) ──→ 2 docs, committed

Phase 2: Evaluation (parallel)
  reviewer-a (team-architect) ──→ Squad A scored 9/8/7/8
  reviewer-b (team-architect) ──→ Squad B scored 9/8/7/8

Phase 3: Convergence
  convergence-coordinator (project-manager)
    ← reviewer-a responses
    ← reviewer-b responses
    → combined summary with 5 actionable changes, committed
```
