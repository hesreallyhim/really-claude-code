# Squad Formation Profile: cloud-infrastructure

**Date:** 2026-02-14
**Source plugin:** `agents-wshobson/plugins/cloud-infrastructure` (v1.2.2)
**Domain:** Multi-cloud architecture, IaC, Kubernetes, service mesh, FinOps

---

## Part A: Formation Analysis

### Candidacy Assessment

| Criterion | Value | Rating |
|-----------|-------|--------|
| Component count | 7 agents, 8 skills, 0 hooks, 0 commands | HIGH |
| Role diversity | Architect, Investigator, Implementer, Specialist | HIGH |
| Skill complementarity | Two distinct clusters (architecture + mesh) with minimal overlap | HIGH |
| Domain complexity | Multi-cloud, hybrid, K8s, service mesh, IaC, compliance | HIGH |
| Parallelism potential | Design and implementation are naturally separable; IaC tasks fan out | HIGH |
| **Candidacy verdict** | **STRONG CANDIDATE** | |

### Scenario Mapping

| Scenario Type | Description | Pattern Fit |
|---------------|-------------|-------------|
| **Primary: Greenfield cloud build** | Design and provision a new multi-cloud or hybrid infrastructure from scratch | Design/Ops two-squad with full design phase |
| **Secondary: Cloud migration** | Migrate existing workloads to cloud or between providers | Same formation; Squad-Design focuses on migration strategy, Squad-Ops on IaC implementation |
| **Tertiary: Infrastructure audit** | Review and optimize existing cloud infrastructure | Could short-circuit to single squad (mesh) since there's no implementation phase |

### Pattern Recommendation

**Formation:** Two-squad diverge/converge

| Level | Pattern | Topology | Rationale |
|-------|---------|----------|-----------|
| **Team-lead** | Pipeline with feedback loop | Linear (2 channels) | Governs spec handoff from Design to Ops with bidirectional amendment channel |
| **Squad-Design** | Small Mesh + ARB | Mesh (3 channels) | Exploratory architecture work requires free-flowing debate with periodic quality gates |
| **Squad-Ops** | Supervisor-Worker + Fan-Out | Hub-and-spoke (4 channels) | IaC tasks are largely independent once design is locked; fan-out maximizes parallelism |

**Alternatives considered:**
- Single squad (all 7 workers): Rejected — exceeds mesh ceiling, context exhaustion risk, mixes design debates with IaC minutiae
- NetSec vs CompStore split: Rejected — infrastructure layers are too tightly coupled, would require constant cross-squad sync
- Adversarial (attack/defend): Rejected — design and implementation are collaborative, not adversarial

### Agent Role Mapping

#### Squad-Design (3 workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Rationale |
|---|---|---|---|---|
| cloud-architect | Architect | Design lead — multi-cloud architecture, FinOps, compliance | opus | Broadest architectural scope; needs deep reasoning for tradeoff analysis |
| hybrid-cloud-architect | Investigator | Multi-cloud/hybrid feasibility, migration patterns, edge computing | opus | Deep OpenStack/VMware/hybrid expertise; explores options and constraints |
| network-engineer | Critic | Validates networking feasibility, security posture, zero-trust boundaries | sonnet | Networking validation is well-scoped; sonnet sufficient for review-style work |

#### Squad-Ops (4 workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Rationale |
|---|---|---|---|---|
| terraform-specialist | Implementer | IaC lead — module architecture, state management, policy-as-code | opus | Advanced Terraform patterns require deep reasoning (module composition, state locking) |
| kubernetes-architect | Implementer | Container orchestration, GitOps, service mesh infrastructure | opus | EKS/AKS/GKE + operator development is reasoning-heavy |
| service-mesh-expert | Specialist | Istio/Linkerd configuration, traffic management, mTLS | sonnet* | Well-scoped domain; applies known patterns from skills |
| deployment-engineer | Implementer | CI/CD pipelines, progressive delivery, monitoring setup | haiku | Procedural pipeline setup; well-defined, not reasoning-heavy |

*service-mesh-expert has no model specified in the source plugin; sonnet recommended based on role scope.

### Skill Distribution

| Skill | Assigned To | Squad | Shared? |
|-------|-------------|-------|---------|
| multi-cloud-architecture | cloud-architect | Design | No |
| hybrid-cloud-networking | hybrid-cloud-architect | Design | No |
| cost-optimization | cloud-architect | Design | No |
| terraform-module-library | terraform-specialist | Ops | No |
| istio-traffic-management | service-mesh-expert | Ops | No |
| linkerd-patterns | service-mesh-expert | Ops | No |
| mtls-configuration | service-mesh-expert | Ops | Shared with network-engineer (Design) for review |
| service-mesh-observability | kubernetes-architect | Ops | No |

### Skill Gaps

| Gap | Impact | Resolution |
|-----|--------|------------|
| No CI/CD pipeline skill | deployment-engineer has no supporting skill | Source from `cicd-automation` plugin (5 agents, 4 skills) or create new |
| No compliance/audit skill | cloud-architect mentions SOC2/HIPAA/PCI-DSS but no skill backs it | Source from `security-compliance` plugin or accept gap |

### Task Graph Template

```
Task 1: Define architecture requirements and constraints
  → Owner: cloud-architect (Squad-Design)

Task 2: Research multi-cloud/hybrid feasibility and options
  → Owner: hybrid-cloud-architect (Squad-Design)
  → Parallel with: 1

Task 3: Set up IaC project scaffolding and CI/CD pipeline
  → Owner: deployment-engineer (Squad-Ops)
  → Parallel with: 1, 2 (design-independent prep)

Task 4: Build reusable Terraform modules for common patterns
  → Owner: terraform-specialist (Squad-Ops)
  → Parallel with: 3

Task 5: Set up monitoring/observability framework
  → Owner: kubernetes-architect (Squad-Ops)
  → Parallel with: 3, 4

Task 6: Validate networking and security design
  → Owner: network-engineer (Squad-Design)
  → Blocked by: 1, 2

Task 7: Produce architecture specification
  → Owner: cloud-architect (Squad-Design)
  → Blocked by: 6

═══ SYNC POINT 1: Design Handoff (spec artifact) ═══

Task 8: Implement networking layer (VPCs, subnets, security groups)
  → Owner: terraform-specialist (Squad-Ops)
  → Blocked by: 7

Task 9: Implement compute/K8s layer
  → Owner: kubernetes-architect (Squad-Ops)
  → Blocked by: 8

Task 10: Implement service mesh layer (Istio/Linkerd, mTLS)
  → Owner: service-mesh-expert (Squad-Ops)
  → Blocked by: 9

Task 11: Implement deployment pipelines and progressive delivery
  → Owner: deployment-engineer (Squad-Ops)
  → Parallel with: 9, 10

═══ SYNC POINT 2: Implementation Review (optional) ═══

Task 12: Produce ADRs and compliance documentation
  → Owner: cloud-architect (Squad-Design)
  → Parallel with: 8-11

Task 13: Integration testing and runbook production
  → Owner: deployment-engineer (Squad-Ops)
  → Blocked by: 8, 9, 10, 11

═══ CONVERGENCE: Reconcile spec vs implementation ═══
```

### Coordination Overhead

| Metric | Value |
|--------|-------|
| Squad-leaders needed | 2 (one per squad) |
| Design phase | FULL (domain complexity warrants team-architect + skill-identifier consultation) |
| Announcer needed | NO (team size < 6 per squad; direct messaging sufficient) |
| Total communication channels | 9 (3 mesh + 4 hub-spoke + 2 inter-squad) |
| Flat mesh equivalent | 21 channels (7 agents) |
| **Channel reduction** | **57%** |

### Risks

| Risk | Mitigation |
|------|------------|
| Squad-Ops blocked waiting for design spec | Preparation work (tasks 3-5) is design-independent; keeps all 4 workers productive |
| Design spec too vague for implementation | Minimum spec template required before Sync Point 1; team-lead validates completeness |
| Late design amendments cascade through implementation | Squad-Ops implements in dependency order; Sync Point 2 catches issues before compute layer |
| Convergence discovers spec/implementation drift | Sync Point 2 is the primary detection mechanism; convergence is a safety net |
| Squad-Design context exhaustion from mesh debate | Kept to 3 members; structured artifact sharing over free-form discussion |

---

## Part B: Squad Configuration

```yaml
formation:
  name: cloud-infrastructure-design-ops
  plugin: cloud-infrastructure
  version: 1.2.2
  structure: two-squad-diverge-converge

  team_lead:
    pattern: pipeline-with-feedback-loop
    channels: 2

  squads:
    - name: squad-design
      pattern: small-mesh-with-arb
      topology: mesh
      channels: 3
      leader:
        agent: squad-leader
        model: opus
        design_phase: full
      workers:
        - name: cloud-architect
          type: cloud-architect
          model: opus
          archetype: architect
          skills: [multi-cloud-architecture, cost-optimization]
          role: "Design lead — multi-cloud architecture, FinOps, compliance"
        - name: hybrid-cloud-architect
          type: hybrid-cloud-architect
          model: opus
          archetype: investigator
          skills: [hybrid-cloud-networking]
          role: "Multi-cloud/hybrid feasibility, migration patterns"
        - name: network-engineer
          type: network-engineer
          model: sonnet
          archetype: critic
          skills: [mtls-configuration]
          role: "Validates networking feasibility, security posture"

    - name: squad-ops
      pattern: supervisor-worker-fan-out
      topology: hub-and-spoke
      channels: 4
      leader:
        agent: squad-leader
        model: opus
        design_phase: short-circuit
      workers:
        - name: terraform-specialist
          type: terraform-specialist
          model: opus
          archetype: implementer
          skills: [terraform-module-library]
          role: "IaC lead — module architecture, state management"
        - name: kubernetes-architect
          type: kubernetes-architect
          model: opus
          archetype: implementer
          skills: [service-mesh-observability]
          role: "Container orchestration, GitOps, service mesh infra"
        - name: service-mesh-expert
          type: service-mesh-expert
          model: sonnet
          archetype: specialist
          skills: [istio-traffic-management, linkerd-patterns, mtls-configuration]
          role: "Istio/Linkerd config, traffic management, mTLS"
        - name: deployment-engineer
          type: deployment-engineer
          model: haiku
          archetype: implementer
          skills: []
          role: "CI/CD pipelines, progressive delivery, monitoring"

  sync_points:
    - name: design-handoff
      type: artifact-transfer
      from: squad-design
      to: squad-ops
      artifact: architecture-specification
      required: true
    - name: implementation-review
      type: bidirectional-check
      between: [squad-design, squad-ops]
      artifact: progress-report-with-issues
      required: false

  skill_gaps:
    - domain: cicd-pipeline
      affects: deployment-engineer
      source_candidate: cicd-automation plugin
    - domain: compliance-audit
      affects: cloud-architect
      source_candidate: security-compliance plugin
```

---

## Part C: Pattern Rationale

This formation splits cloud infrastructure work along the **design-vs-implementation** axis — a fault line that maps directly to the skill-identification framework's "Design vs. Execution Distinction." Squad-Design operates as a small mesh with architectural review boards, appropriate for the exploratory, debate-heavy nature of architecture work where agents need free-flowing discussion and periodic quality gates. Squad-Ops operates as a supervisor-worker fan-out, appropriate for the deterministic, parallelizable nature of IaC implementation where tasks are independent once the specification is locked.

The critical design choice is that Squad-Ops is **not idle during the design phase**. IaC scaffolding, CI/CD pipeline setup, reusable module development, and monitoring framework configuration are all design-independent preparation work. This eliminates the primary risk of pipeline-style formations (upstream blocking downstream) while preserving the clean handoff artifact at Sync Point 1.

The Option B split (networking/security vs compute/storage) was rejected because infrastructure layers are too tightly coupled — nearly every compute decision has networking implications. This would require constant cross-squad synchronization, defeating the purpose of squad isolation. The design-vs-implementation split creates a cleaner divergence with well-defined convergence through specification artifacts.

This formation is strongest for **greenfield cloud builds** and **cloud migrations** where both design and implementation are substantial workstreams. For **infrastructure audits** (review-only, no implementation), the two-squad structure is over-engineered; a single mesh squad of the architecture-oriented agents would suffice.
