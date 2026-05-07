# Squad Formation Profile: tdd-steel-thread-security

**Date:** 2026-02-14
**Source scenario:** `tdd-scenarios.md`, Scenario 2 (Veridian -- Zero-Trust Service Mesh Authentication Broker)
**Domain:** Kubernetes operator TDD for mTLS certificate lifecycle, Vault PKI integration, SOC 2 compliance

---

## Part A: Formation Analysis

> **Quick Reference**
> | | |
> |---|---|
> | **Formation** | Two-squad diverge/converge |
> | **Squads** | Squad-Implement (3 workers, hub-and-spoke) + Squad-Scaffold (3 workers, mesh) |
> | **Total agents** | 6 workers + 2 squad-leaders + 1 team-lead |
> | **Key sync** | scope-fence-handoff (required), test-utility-handoff (required), integration-review (optional) |
> | **Ready** | YES |
> | **Best for** | Steel-thread TDD in security-critical domains with compliance constraints and one-month timelines |

### Candidacy Assessment

| Criterion | Value | Rating |
|-----------|-------|--------|
| Component count | 6 workers, 2 squad-leaders, 1 team-lead, ~8 skill areas | MEDIUM |
| Role diversity | Architect, Implementer, Specialist (Testing), Specialist (Security), Documenter, Critic | HIGH |
| Skill complementarity | Two distinct clusters (Go operator TDD + test infrastructure/compliance) with shared test utility interface | HIGH |
| Domain complexity | Kubernetes CRDs, Vault PKI, mTLS, certificate state machines, SOC 2, envtest, fake clocks | HIGH |
| Parallelism potential | Golden-path state transitions are independently testable; scaffold work (E2E setup, scope fence, audit logs) fans out | HIGH |
| **Candidacy verdict** | **STRONG CANDIDATE** | |

### Scenario Mapping

| Scenario Type | Description | Pattern Fit |
|---------------|-------------|-------------|
| **Primary: Steel-thread TDD** | Prove one golden path end-to-end with full test coverage at every layer, under strict scope constraints | Two-squad diverge/converge: one squad drives TDD implementation, the other provides testing infrastructure and scope governance |
| **Secondary: Compliance-gated security implementation** | Build a security feature that must satisfy external auditors (SOC 2, customer security review) | Same formation; Squad-Scaffold owns compliance artifacts while Squad-Implement focuses on correctness |
| **Tertiary: Operator development with envtest** | Build a Kubernetes operator using controller-runtime with integration testing via envtest | Could short-circuit to single squad if no compliance constraints exist |

### Pattern Recommendation

| Level | Pattern | Topology | Rationale |
|-------|---------|----------|-----------|
| **Team-lead** | Pipeline with feedback loop | Linear (2 channels) | Governs scope-fence handoff from Scaffold to Implement and test-utility handoff in reverse; feedback loop for scope boundary disputes |
| **Squad-Implement** | Supervisor-Worker (TDD cadence) | Hub-and-spoke (3 channels) | TDD cycles benefit from centralized coordination: squad leader assigns one failing test at a time, reviews each green-to-refactor transition, and enforces scope boundaries |
| **Squad-Scaffold** | Small Mesh | Mesh (3 channels) | Diverse work (E2E framework, scope fence, audit logs, fake clock) requires free-flowing coordination between workers who depend on each other's decisions |

**Alternatives considered:**
- Single squad (all 6 workers): Rejected -- mixes TDD implementation discipline with infrastructure/documentation concerns; scope discipline degrades when the same people write both production tests and scope fence documentation
- Three squads (unit/integration/E2E): Rejected -- splits the test pyramid across teams, but the steel-thread golden path is a single coherent flow; fragmenting it across test layers creates coordination overhead that exceeds the one-month budget
- Adversarial (Red/Blue): Rejected -- the steel thread is too narrow for adversarial testing to add value; adversarial patterns are appropriate when expanding scope beyond the golden path

### Agent Role Mapping

#### Squad-Implement: Golden-Path TDD (3 workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Context Pressure | Rationale |
|---|---|---|---|---|---|
| operator-tdd-lead | Architect | Designs the certificate lifecycle state machine, defines CRD schema, owns the reconciler structure | opus | HIGH | State machine design and CRD schema require deep reasoning about Kubernetes controller patterns and Vault PKI interactions |
| cert-lifecycle-dev | Implementer | Writes failing tests and production code for the issuance and rotation state transitions | opus | HIGH | Core TDD loop for security-critical code; mTLS certificate semantics and Go test patterns require strong reasoning |
| vault-integration-dev | Implementer (Senior) | Writes failing tests and production code for Vault PKI client integration, fake Vault client for unit tests | opus | MEDIUM | Vault Go client library patterns are well-documented but the fake client must faithfully model PKI behavior |

#### Squad-Scaffold: Test Infrastructure and Scope Governance (3 workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Context Pressure | Rationale |
|---|---|---|---|---|---|
| envtest-engineer | Specialist (Testing) | Sets up envtest harness, configures CRD installation, writes the envtest lifecycle (start/stop) and the E2E test framework (test pod deployment, TLS verification) | opus | HIGH | envtest setup with custom CRDs and E2E pod orchestration in staging EKS is non-trivial; requires deep controller-runtime knowledge |
| scope-fence-author | Documenter + Critic | Authors the scope fence document, converts out-of-scope edge cases from Squad-Implement into documented exclusions with rationale and forward plans | sonnet | LOW | Primarily a writing and analysis role; the technical depth is in understanding what was excluded, not in implementation |
| audit-compliance-dev | Specialist (Testing) | Implements SOC 2 audit log assertions (CC6.1, CC6.3) for golden-path events, builds the fake-clock test utility | sonnet | MEDIUM | Audit log structure is well-defined by SOC 2 controls; fake-clock implementation follows established Go patterns (e.g., `clock` interface injection) |

### Skill Distribution

| Skill | Assigned To | Squad | Shared? |
|-------|-------------|-------|---------|
| Go operator development (controller-runtime) | operator-tdd-lead | Implement | No |
| Go TDD / table-driven tests | cert-lifecycle-dev | Implement | No |
| Vault PKI Go client | vault-integration-dev | Implement | No |
| envtest framework setup | envtest-engineer | Scaffold | No |
| E2E test orchestration (EKS staging) | envtest-engineer | Scaffold | No |
| Scope fence authoring | scope-fence-author | Scaffold | No |
| SOC 2 audit log testing | audit-compliance-dev | Scaffold | No |
| Fake clock / test utilities | audit-compliance-dev | Scaffold | Shared with cert-lifecycle-dev (Implement) for consumption |
| mTLS / X.509 certificate mechanics | vault-integration-dev | Implement | Shared with envtest-engineer (Scaffold) for E2E TLS handshake verification |

### Skill Gaps

| Gap | Impact | Resolution |
|-----|--------|------------|
| No dedicated Kubernetes/EKS infrastructure agent | envtest-engineer must also handle staging EKS namespace provisioning and Helm deployment for E2E tests | Accept gap -- envtest-engineer has sufficient scope; staging EKS cluster already exists and is managed by Stratum's platform team |
| No dedicated Vault administration agent | vault-integration-dev must configure the staging Vault PKI mount in addition to writing Go client code | Accept gap -- Vault PKI mount configuration is a one-time setup task, not an ongoing workstream |
| No Rego/OPA policy agent | OPA admission policies are mentioned in the technical environment but are out of scope for the steel thread | Accept gap -- explicitly excluded from steel-thread scope; will be documented in the scope fence |

### Task Graph

```
Phase: PREP
-----------
Task 1: Design ServiceIdentity CRD schema and certificate lifecycle state machine
  -> Owner: operator-tdd-lead (Squad-Implement)
  -> Done when: CRD schema YAML and state machine diagram are committed to repo

Task 2: Set up envtest harness with CRD installation and test lifecycle
  -> Owner: envtest-engineer (Squad-Scaffold)
  -> Parallel with: 1
  -> Done when: `go test ./... -run TestEnvtestSmoke` passes with a trivial reconciler

Task 3: Configure staging Vault PKI mount and verify Go client connectivity
  -> Owner: vault-integration-dev (Squad-Implement)
  -> Parallel with: 1, 2
  -> Done when: A Go test creates and reads back a cert from the staging Vault PKI mount

Task 4: Draft initial scope fence document with known exclusions
  -> Owner: scope-fence-author (Squad-Scaffold)
  -> Parallel with: 1, 2, 3
  -> Done when: Scope fence lists revocation, multi-cluster, non-K8s workloads, and OPA policies as excluded, with rationale for each

Task 5: Implement fake-clock test utility and decide fake-clock vs real-time-wait
  -> Owner: audit-compliance-dev (Squad-Scaffold)
  -> Parallel with: 1, 2, 3, 4
  -> Done when: clock.Interface is defined with fake and real implementations; decision document is committed

=== SYNC POINT: prep-complete (CRD schema, envtest harness, Vault connectivity, scope fence draft, fake clock) ===

Phase: CORE
-----------
Task 6: TDD: Service registration and certificate issuance (unit tests with fake Vault)
  -> Owner: cert-lifecycle-dev (Squad-Implement)
  -> Blocked by: 1, 5
  -> Done when: Failing test written first, then reconciler issues cert via fake Vault client; table-driven tests cover happy path

Task 7: TDD: Certificate rotation trigger and execution (unit tests with fake clock)
  -> Owner: cert-lifecycle-dev (Squad-Implement)
  -> Blocked by: 6
  -> Done when: Failing tests for approaching-expiry detection, new cert issuance, old cert drain, old cert deletion; all pass with fake clock

Task 8: TDD: Vault PKI integration (real Vault client wrapper with interface-based DI)
  -> Owner: vault-integration-dev (Squad-Implement)
  -> Blocked by: 1, 3
  -> Done when: Vault client wrapper implements the same interface as the fake; unit tests verify cert signing and SAN assignment

Task 9: envtest integration tests: ServiceIdentity CR -> Secret with client cert
  -> Owner: envtest-engineer (Squad-Scaffold)
  -> Blocked by: 2, 6
  -> Done when: envtest creates a ServiceIdentity CR, reconciler produces a Secret, test asserts Secret contains a valid X.509 cert with correct SAN

Task 10: Implement SOC 2 audit log emissions and test assertions (CC6.1, CC6.3)
  -> Owner: audit-compliance-dev (Squad-Scaffold)
  -> Blocked by: 6, 7
  -> Done when: Each golden-path state transition emits structured audit log entry; test asserts log entries contain required fields per CC6.1 and CC6.3

Task 11: Update scope fence with edge cases surfaced during core implementation
  -> Owner: scope-fence-author (Squad-Scaffold)
  -> Blocked by: 6 (ongoing as edge cases surface)
  -> Done when: All edge cases raised by Squad-Implement are documented with exclusion rationale

=== SYNC POINT: core-review (golden-path unit tests passing, envtest integration tests passing, audit logs tested) ===

Phase: CONVERGENCE
------------------
Task 12: E2E test: Deploy two test pods, verify mTLS handshake with broker-issued certs
  -> Owner: envtest-engineer (Squad-Scaffold)
  -> Blocked by: 8, 9
  -> Done when: E2E test deploys client and server pods in staging EKS, client authenticates to server using broker-issued cert, test verifies TLS handshake and extracts correct service identity from client cert

Task 13: E2E test: Verify zero-downtime certificate rotation in staging
  -> Owner: vault-integration-dev (Squad-Implement)
  -> Blocked by: 7, 12
  -> Done when: E2E test triggers cert rotation, verifies no connection failures during rotation window

Task 14: Finalize scope fence document for CISO review
  -> Owner: scope-fence-author (Squad-Scaffold)
  -> Blocked by: 11, 13
  -> Done when: Scope fence is complete, internally reviewed, and ready for CISO sign-off

Task 15: Integration of all test layers into CI pipeline (GitHub Actions)
  -> Owner: envtest-engineer (Squad-Scaffold)
  -> Blocked by: 9, 10, 12
  -> Done when: Unit tests run on every PR, envtest runs on every PR, E2E runs nightly against staging

=== CONVERGENCE: All golden-path tests passing at every layer; scope fence finalized; CI pipeline green ===
```

### Sync Point Details

#### SP1: prep-complete

| Field | Value |
|-------|-------|
| Initiated by | operator-tdd-lead (Squad-Implement) |
| Validated by | envtest-engineer (Squad-Scaffold) |
| Artifact format | Git commit containing: CRD schema YAML, envtest smoke test, Vault connectivity test, scope fence draft, fake-clock utility |
| Minimum content | CRD schema must define `ServiceIdentity` spec and status; envtest must start/stop without error; Vault must issue one test cert; scope fence must list at least 4 exclusions; fake-clock must implement `clock.Interface` |
| Gate condition | All prep artifacts committed and passing `go test`; scope fence draft reviewed by both squad leaders |
| Failure action | Extend prep phase; do not begin core TDD cycle until all prep artifacts are functional |

#### SP2: core-review

| Field | Value |
|-------|-------|
| Initiated by | cert-lifecycle-dev (Squad-Implement) |
| Validated by | scope-fence-author (Squad-Scaffold) |
| Artifact format | Test execution report (go test output) + updated scope fence |
| Minimum content | 100% branch coverage of golden-path state machine; envtest creates ServiceIdentity and verifies Secret; audit log assertions pass; scope fence updated with all newly surfaced edge cases |
| Gate condition | `go test ./...` passes with zero failures; scope fence has no undocumented exclusions |
| Failure action | Fix failing tests before proceeding to E2E phase; undocumented edge cases must be triaged (in-scope or added to scope fence) |

#### SP3: test-utility-handoff

| Field | Value |
|-------|-------|
| Initiated by | audit-compliance-dev (Squad-Scaffold) |
| Validated by | cert-lifecycle-dev (Squad-Implement) |
| Artifact format | Go package containing `clock.Interface`, `FakeClock`, and `RealClock` implementations |
| Minimum content | `FakeClock` supports `Now()`, `Advance(d)`, and `AfterFunc(d, f)` with deterministic behavior |
| Gate condition | Squad-Implement can import and use `FakeClock` in rotation unit tests |
| Failure action | Iterate on the clock interface until Squad-Implement confirms it meets their testing needs |

### Convergence Protocol

| Field | Value |
|-------|-------|
| Driver | Team lead |
| Participants | operator-tdd-lead (Squad-Implement), envtest-engineer (Squad-Scaffold) |
| Artifacts compared | Unit test coverage report vs. scope fence exclusion list; envtest results vs. E2E results; audit log test assertions vs. SOC 2 CC6.1/CC6.3 mapping |
| Method | Team lead reviews: (1) every golden-path state transition has unit + envtest + E2E coverage; (2) every out-of-scope behavior appears in the scope fence; (3) audit log assertions match the SOC 2 control mapping |
| Success criteria | Zero gaps between the golden-path specification and test coverage at all three layers; scope fence document is complete and internally consistent; CI pipeline runs all test layers |
| On discrepancy | Missing test coverage: Squad-Implement writes the test. Missing scope fence entry: Squad-Scaffold documents it. Audit log gap: audit-compliance-dev adds the assertion. |
| Max iterations | 2 convergence cycles before escalation to CISO for scope adjudication |
| Output artifact | Final test execution report + finalized scope fence document + CI pipeline configuration, all committed to the repository |

### Coordination Overhead

| Metric | Value |
|--------|-------|
| Squad-leaders needed | 2 (one per squad) |
| Design phase | SHORT-CIRCUIT -- the CRD schema and state machine design (Task 1) serve as the design artifact; no separate design-phase deliberation is needed beyond the prep phase |
| Announcer needed | NO (3 workers per squad, well within mesh/hub-spoke ceiling) |
| Total communication channels | 8 (3 hub-spoke in Implement + 3 mesh in Scaffold + 2 inter-squad) |
| Flat mesh equivalent | 15 channels (6 workers) |
| **Channel reduction** | **47%** |

### Risks

| Risk | Mitigation |
|------|------------|
| Scope creep from security-minded engineers wanting to test error paths | Scope fence document is a required artifact; Squad-Scaffold's scope-fence-author is the designated "scope police" who converts impulses into documented exclusions |
| Fake-clock decision delays core TDD cycle | Task 5 is in the prep phase and runs in parallel; the decision must be made before Squad-Implement begins rotation tests (Task 7) |
| Staging Vault PKI mount not provisioned in time | Task 3 is in the prep phase; if blocked, Squad-Implement can proceed with unit tests using the fake Vault client while DevOps provisions the staging mount |
| envtest does not faithfully reproduce EKS behavior for cert-related Secrets | envtest runs real etcd but lacks cloud-provider-specific behavior; the E2E test (Task 12) in the staging EKS cluster is the ground truth. Divergences are documented and escalated. |
| One-month timeline is insufficient for all three test layers | The task graph prioritizes: unit tests first (fastest feedback), envtest second (medium confidence), E2E last (highest confidence). If time runs short, E2E test coverage is the first thing to descope -- but this must be documented in the scope fence and flagged to the CISO. |
| SOC 2 audit log format requirements are ambiguous | audit-compliance-dev consults with Stratum's SOC 2 auditor contact (Big 4 firm) during the prep phase to confirm expected log structure before writing assertions |

---

## Part B: Squad Configuration

```yaml
formation:
  name: tdd-steel-thread-security
  scenario: veridian-zero-trust-service-mesh
  version: "1.0"
  structure: two-squad-diverge-converge
  task: "TDD implementation of the golden-path certificate lifecycle for a zero-trust
    service mesh authentication broker, producing a layered test suite (unit, envtest,
    E2E) and a scope fence document, within one month."
  ready_to_proceed: true

  team_lead:
    pattern: pipeline-with-feedback-loop
    topology: linear
    channels: 2

  squads:
    - name: squad-implement
      task: "Drive TDD implementation of the ServiceIdentity CRD, Kubernetes operator
        reconciler, Vault PKI client integration, and certificate lifecycle state machine.
        Write failing tests first at the unit and envtest layers. Enforce golden-path-only
        scope discipline."
      pattern: supervisor-worker
      topology: hub-and-spoke
      channels: 3
      briefing_context: |
        You are building a Kubernetes operator in Go using controller-runtime that
        mediates mTLS certificate issuance and rotation via HashiCorp Vault PKI.
        The steel thread covers exactly one flow: service registration, certificate
        issuance, mTLS handshake, and zero-downtime certificate rotation. You must
        write a failing test before every line of production code. You must NOT
        write tests for revocation, multi-cluster, or non-K8s workloads. When you
        identify out-of-scope edge cases, file them for Squad-Scaffold to document
        in the scope fence.
      leader:
        agent: squad-leader
        model: opus
        design_phase: short-circuit
      workers:
        - name: operator-tdd-lead
          source_agent: solid-architect
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "State machine design and CRD schema decisions require deep architectural reasoning"
          archetype: architect
          skills:
            - name: go-controller-runtime
            - name: kubernetes-crd-design
          role: "Design the certificate lifecycle state machine and CRD schema; lead the TDD cycle structure"
          briefing_context: |
            Your first task is to define the ServiceIdentity CRD schema and the
            certificate lifecycle state machine (registration, issuance, active,
            approaching-expiry, rotation, drain, cleanup). Commit both as artifacts
            in the prep phase. Then guide the TDD cadence for the core phase.

        - name: cert-lifecycle-dev
          source_agent: independent-contributor
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "Core TDD loop for security-critical state transitions; must reason about certificate semantics"
          archetype: implementer
          skills:
            - name: go-tdd-table-driven
            - name: certificate-lifecycle-testing
          role: "Write failing tests and production code for certificate issuance and rotation state transitions"
          briefing_context: |
            You consume the state machine design from operator-tdd-lead and the
            fake-clock utility from Squad-Scaffold. Each state transition gets a
            failing test first, then the minimal production code. Use table-driven
            tests with subtests for each transition.

        - name: vault-integration-dev
          source_agent: independent-contributor
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "Vault PKI client integration requires understanding of both the Go client library and certificate signing semantics"
          archetype: implementer
          skills:
            - name: vault-pki-go-client
            - name: mtls-x509-mechanics
              shared_with: envtest-engineer
          role: "Write the Vault PKI client wrapper with interface-based DI, implement the fake Vault client for unit tests, and own the E2E rotation test"
          briefing_context: |
            Your first task is to verify Go client connectivity to the staging
            Vault PKI mount. Then build the Vault client wrapper behind an
            interface so cert-lifecycle-dev can use the fake implementation.
            You own the E2E rotation test (Task 13) in the convergence phase.

    - name: squad-scaffold
      task: "Build the testing infrastructure (envtest harness, E2E framework, fake clock),
        author the scope fence document, implement SOC 2 audit log test assertions,
        and integrate all test layers into the CI pipeline."
      pattern: small-mesh
      topology: mesh
      channels: 3
      briefing_context: |
        You provide the testing infrastructure and governance that enables
        Squad-Implement to do TDD. Your deliverables are: (1) a working envtest
        harness, (2) an E2E test framework for the staging EKS cluster, (3) a
        fake-clock test utility, (4) SOC 2 audit log test assertions for CC6.1
        and CC6.3, (5) the scope fence document, and (6) CI pipeline integration.
        You are the scope police: every out-of-scope edge case that Squad-Implement
        surfaces must be documented in the scope fence with a rationale.
      leader:
        agent: squad-leader
        model: opus
        design_phase: short-circuit
      workers:
        - name: envtest-engineer
          source_agent: testing-expert
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "envtest setup with custom CRDs and E2E pod orchestration in staging EKS requires deep controller-runtime and Kubernetes knowledge"
          archetype: specialist
          skills:
            - name: envtest-framework
            - name: e2e-kubernetes-testing
            - name: mtls-x509-mechanics
              shared_with: vault-integration-dev
          role: "Set up envtest harness, build E2E test framework for staging EKS, integrate all test layers into CI"
          briefing_context: |
            Your first task is the envtest smoke test (Task 2). Then you write
            the envtest integration test for ServiceIdentity -> Secret (Task 9).
            In the convergence phase you own the E2E mTLS handshake test (Task 12)
            and CI pipeline integration (Task 15).

        - name: scope-fence-author
          source_agent: document-maintainer
          spawn_type: independent-contributor-sonnet
          model: sonnet
          model_rationale: "Primarily a writing and analysis role; technical depth is in understanding exclusions, not in implementation"
          archetype: documenter
          skills:
            - name: technical-documentation
            - name: scope-governance
          role: "Author and maintain the scope fence document; convert out-of-scope edge cases into documented exclusions with rationale"
          briefing_context: |
            Your first task is the initial scope fence draft (Task 4) covering
            revocation, multi-cluster, non-K8s workloads, and OPA policies.
            During the core phase, you receive edge cases from Squad-Implement
            and add them with exclusion rationale and forward plans. In
            convergence, you finalize the document for CISO review.

        - name: audit-compliance-dev
          source_agent: testing-expert
          spawn_type: independent-contributor-sonnet
          model: sonnet
          model_rationale: "Audit log structure follows well-defined SOC 2 controls; fake-clock follows established Go patterns"
          archetype: specialist
          skills:
            - name: soc2-audit-testing
            - name: go-test-utilities
          role: "Implement SOC 2 audit log assertions for CC6.1/CC6.3 and build the fake-clock test utility"
          briefing_context: |
            Your first task is the fake-clock utility and the fake-clock vs
            real-time-wait decision document (Task 5). Then you implement audit
            log emissions and test assertions (Task 10). The fake-clock package
            is shared with Squad-Implement's cert-lifecycle-dev.

  sync_points:
    - name: prep-complete
      type: gate
      from: squad-implement
      to: squad-scaffold
      artifact: "CRD schema, envtest smoke test, Vault connectivity test, scope fence draft, fake-clock utility"
      required: true
      initiated_by: operator-tdd-lead
      validated_by: envtest-engineer
      gate_condition: "All prep artifacts committed, `go test` passes for smoke tests, scope fence reviewed by both squad leaders"
      minimum_content:
        - ServiceIdentity CRD schema YAML with spec and status
        - envtest starts and stops without error
        - Vault PKI mount issues one test certificate
        - Scope fence lists at least 4 exclusions with rationale
        - FakeClock implements clock.Interface

    - name: test-utility-handoff
      type: artifact-transfer
      from: squad-scaffold
      to: squad-implement
      artifact: "clock.Interface package with FakeClock and RealClock implementations"
      required: true
      initiated_by: audit-compliance-dev
      validated_by: cert-lifecycle-dev
      minimum_content:
        - clock.Interface with Now(), Advance(d), AfterFunc(d, f)
        - FakeClock with deterministic time progression
        - RealClock delegating to time.Now()

    - name: core-review
      type: bidirectional-check
      between: [squad-implement, squad-scaffold]
      artifact: "Test execution report + updated scope fence"
      required: false

  skill_gaps:
    - domain: rego-opa-admission-policies
      affects: operator-tdd-lead
      source_candidate: "Out of scope for steel thread; documented in scope fence"
    - domain: vault-administration
      affects: vault-integration-dev
      source_candidate: "Accept gap; one-time staging PKI mount configuration handled by vault-integration-dev"
    - domain: eks-infrastructure-provisioning
      affects: envtest-engineer
      source_candidate: "Accept gap; staging EKS cluster managed by Stratum's existing platform team"
```

---

## Part C: Pattern Rationale

This formation splits the work along the **TDD implementation vs. testing infrastructure** axis. This is the natural fault line for a steel-thread project: one squad focuses exclusively on the red-green-refactor cycle for the golden path, while the other provides the scaffolding that makes that cycle possible (envtest harness, fake clock, E2E framework) and the governance that keeps it focused (scope fence document, audit log compliance). The alternative -- a single squad doing both -- was rejected because it undermines scope discipline. When the same engineers writing production tests also write the scope fence, the document becomes an afterthought rather than a first-class deliverable. Separating scope governance into its own squad creates healthy tension: Squad-Implement wants to expand scope to test edge cases, and Squad-Scaffold pushes back by converting those impulses into documented exclusions.

The intra-squad topologies reflect the different work styles. Squad-Implement uses hub-and-spoke because TDD cycles benefit from centralized coordination: the squad leader assigns one failing test at a time, reviews each transition from red to green, and catches scope violations before they become code. The workers implement in parallel only when working on independent state transitions (issuance and Vault integration can proceed simultaneously; rotation depends on issuance). Squad-Scaffold uses a small mesh because their work is varied and interdependent: the fake-clock design affects both the test utility and the scope fence rationale; the envtest harness configuration affects both the integration test structure and the E2E framework; the audit log format affects both the compliance assertions and the scope of what Squad-Implement must emit. Free-flowing coordination outperforms a hub-and-spoke model for this kind of cross-cutting work.

This formation excels at **time-constrained steel-thread projects in compliance-sensitive domains** where both implementation rigor and documentation completeness are required. It would be over-engineered for a prototype (where scope governance is unnecessary) or for a project without compliance obligations (where the Scaffold squad's audit log and scope fence work would not exist). For longer timelines (one quarter or more), the Scaffold squad should evolve into a platform-testing squad that owns CI infrastructure, test environments, and testing patterns across multiple feature squads.

### Formation Variants

| Scenario | Variant | Changes from default |
|----------|---------|---------------------|
| No compliance constraints (no SOC 2) | Reduced Scaffold | Drop audit-compliance-dev; merge fake-clock responsibility into envtest-engineer; scope-fence-author becomes part-time |
| Longer timeline (one quarter) | Expanded Implement | Add a second Implementer to Squad-Implement for parallel error-path TDD after golden path is proven; Scaffold squad adds a CI/CD specialist |
| No staging EKS cluster available | E2E descoped | Drop Tasks 12 and 13; envtest becomes the highest-fidelity test layer; document E2E gap in scope fence |
