# Squad Formation Profile: tdd-enterprise-medical

**Date:** 2026-02-14
**Source scenario:** `tdd-scenarios.md` Scenario 5 -- Atreus (Implantable Cardiac Monitor Firmware and Cloud Telemetry Platform)
**Domain:** Medical device firmware (IEC 62304 Class C), cloud telemetry (HIPAA/GDPR), AI/ML arrhythmia classification (SaMD), clinical dashboard

---

## Part A: Formation Analysis

> **Quick Reference**
> | | |
> |---|---|
> | **Formation** | Multi-squad convergent pipeline |
> | **Squads** | Squad-Firmware (3 workers, mesh), Squad-Cloud (3 workers, hub-and-spoke), Squad-AI/ML (2 workers, pair), Squad-V&V (3 workers, hub-and-spoke) |
> | **Total agents** | 11 workers + 4 squad-leaders + 1 team-lead = 16 agents |
> | **Key sync** | firmware-test-vectors (required), model-artifact-handoff (required), coverage-aggregation (required), e2e-integration (required), dhf-assembly (required) |
> | **Ready** | NO -- gaps in embedded-ML-validation skill, clinical-data-science domain knowledge, HIL-bench-automation tooling |
> | **Best for** | Enterprise-in-high-regulation TDD with multi-sub-team coordination, regulatory-mandated test coverage, cross-boundary E2E verification |

### Candidacy Assessment

| Criterion | Value | Rating |
|-----------|-------|--------|
| Component count | 16 agents, 4 squads, multiple cross-squad sync points | HIGH |
| Role diversity | Architect, Implementer, Specialist (Testing, Security, ML), Investigator, Critic, Documenter | HIGH |
| Skill complementarity | Four distinct skill clusters (embedded, cloud, ML, V&V) with minimal overlap and well-defined interfaces | HIGH |
| Domain complexity | Medical device firmware + cloud + AI/ML + regulatory (IEC 62304, FDA, HIPAA, GDPR, EU MDR) | VERY HIGH |
| Parallelism potential | Four sub-teams work in parallel on distinct codebases; convergence only at integration and V&V boundaries | HIGH |
| **Candidacy verdict** | **STRONG CANDIDATE** | |

### Scenario Mapping

| Scenario Type | Description | Pattern Fit |
|---------------|-------------|-------------|
| **Primary: Regulated multi-platform TDD** | Establish TDD processes across 4 codebases with different regulatory classifications and testing philosophies | Multi-squad convergent pipeline with dedicated V&V integration squad |
| **Secondary: Legacy migration with parity testing** | Replace Sentinel platform while proving clinical equivalence | V&V squad owns parity regression suite; other squads produce migration-specific tests |
| **Tertiary: FDA submission preparation** | Assemble 510(k) design history file from automated test artifacts | V&V squad drives convergence; all squads contribute traceability-tagged test results |

### Pattern Recommendation

**Formation:** Multi-squad convergent pipeline (4 squads converging into V&V)

| Level | Pattern | Topology | Rationale |
|-------|---------|----------|-----------|
| **Team-lead** | Hub-and-spoke with convergence gate | Star (4 channels to squad leaders + 1 V&V convergence channel) | Governs 4 parallel workstreams with mandatory convergence at DHF assembly |
| **Squad-Firmware** | Small Mesh | Mesh (3 channels) | Firmware TDD requires debate between Rust/C testing approaches, host vs. target strategy, and ML inference wrapper design |
| **Squad-Cloud** | Supervisor-Worker | Hub-and-spoke (3 channels) | Cloud tests are well-scoped per service; leader assigns Lambda/Kinesis/security test work and reviews |
| **Squad-AI/ML** | Pair Programming | Pair (1 channel) | Two complementary roles (ML engineer + validation specialist) must collaborate tightly on statistical validation |
| **Squad-V&V** | Supervisor-Worker with cross-squad liaison | Hub-and-spoke (3 channels) + cross-squad channels | V&V leader coordinates cross-squad artifact collection; workers execute E2E tests, dashboard tests, and DHF assembly |

**Alternatives considered:**
- Two-squad (firmware+cloud vs. AI/ML+V&V): Rejected -- firmware and cloud testing have no skill overlap; forcing them together creates a 6-person mesh that exceeds context limits
- Three-squad (firmware, cloud+frontend, AI/ML+V&V): Rejected -- cloud security testing and frontend testing require different skills; combining forces one squad to cover too many domains
- Single V&V-less formation (each squad owns its own V&V): Rejected -- the end-to-end test and DHF assembly are inherently cross-cutting and cannot be owned by any single domain squad
- Five squads (separating frontend into its own squad): Rejected -- frontend testing scope (component tests, accessibility, 3 E2E workflows) is insufficient to justify a full squad; absorbed into V&V

### Agent Role Mapping

#### Squad-Firmware (3 workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Context Pressure | Rationale |
|---|---|---|---|---|---|
| firmware-rust-tester | Specialist (Testing) | Rust ECG pipeline test lead -- property-based tests with proptest, Embassy async test patterns, TFLM inference wrapper tests | opus | HIGH | IEC 62304 Class C demands exhaustive coverage; property-based testing strategy requires deep reasoning about signal processing invariants |
| firmware-c-tester | Implementer | C BLE stack test implementation -- CppUTest unit tests, BLE protocol resilience/forward-compatibility tests, fault injection | sonnet | MEDIUM | Well-scoped CppUTest work against a defined BLE protocol spec; sonnet sufficient for structured table-driven test generation |
| firmware-integration | Specialist (Testing) | QEMU integration tests, HIL bench test automation, host-vs-target test strategy, cross-core (app+network) integration | opus | HIGH | QEMU nRF5340 emulation is incomplete; requires creative mocking strategies and reasoning about host/target FP semantic differences |

#### Squad-Cloud (3 workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Context Pressure | Rationale |
|---|---|---|---|---|---|
| cloud-lambda-tester | Implementer | Lambda unit tests (pytest + moto), Kinesis ingestion pipeline integration tests (Localstack), k6 load tests | sonnet | MEDIUM | Structured test generation against well-defined AWS service interfaces; moto/Localstack patterns are well-established |
| cloud-security-tester | Specialist (Security) | HIPAA security control tests (encryption, access control, audit logging), DSAR workflow tests, GDPR/MDR retention logic tests | opus | HIGH | HIPAA/GDPR regulatory intersection requires deep reasoning about data retention tensions and access control edge cases |
| cloud-infra-tester | Implementer | AWS CDK infrastructure tests, Cognito auth flow tests, CloudWatch monitoring validation, SageMaker endpoint integration | sonnet | MEDIUM | Infrastructure-level tests follow established CDK assertion patterns; sonnet sufficient |

#### Squad-AI/ML (2 workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Context Pressure | Rationale |
|---|---|---|---|---|---|
| ml-validation-engineer | Specialist (Testing) | Golden model snapshot tests, statistical validation suite design, SageMaker Pipelines automation, predetermined change control plan test infrastructure | opus | HIGH | Translating FDA AI/ML SaMD guidance into automated test infrastructure requires deep regulatory and ML expertise |
| ml-data-scientist | Investigator | ECG dataset curation (MIT-BIH + Cardiax), annotation QA, statistical threshold definition, performance metric analysis, clinical significance review | opus | HIGH | Bridging clinical data science and automated testing requires reasoning about statistical validity, dataset bias, and clinical relevance |

#### Squad-V&V (3 workers + squad-leader)

| Plugin Agent | Archetype | Squad Role | Model | Context Pressure | Rationale |
|---|---|---|---|---|---|
| e2e-test-engineer | Specialist (Testing) | End-to-end test harness (Python orchestration of HIL bench + BLE monitor + cloud API + dashboard), nightly E2E execution, 5-minute alert SLA verification | opus | HIGH | Cross-boundary E2E test spanning 4 codebases, 3 languages, 2 hardware platforms requires deep coordination reasoning |
| dashboard-tester | Implementer | Clinical dashboard component tests (Jest + RTL), accessibility tests (axe-core), Playwright E2E for clinician workflows, Sentinel UI parity tests | sonnet | MEDIUM | Frontend testing is well-scoped with established React Testing Library / Playwright patterns |
| dhf-assembler | Documenter | DHF traceability matrix generation, test result archival pipeline, coverage report aggregation, version-pinned build manifests, regulatory document assembly | sonnet | MEDIUM | Documentation assembly from structured test metadata; requires precision but not deep reasoning |

### Skill Distribution

| Skill | Assigned To | Squad | Shared? |
|-------|-------------|-------|---------|
| Rust / Embassy testing | firmware-rust-tester | Firmware | No |
| proptest (property-based) | firmware-rust-tester | Firmware | No |
| CppUTest | firmware-c-tester | Firmware | No |
| BLE 5.3 protocol testing | firmware-c-tester | Firmware | Shared with e2e-test-engineer (V&V) for BLE sniffer integration |
| QEMU nRF5340 emulation | firmware-integration | Firmware | No |
| HIL bench automation | firmware-integration | Firmware | Shared with e2e-test-engineer (V&V) for E2E orchestration |
| TFLM inference testing | firmware-rust-tester | Firmware | Shared with ml-validation-engineer (AI/ML) for model artifact handoff |
| pytest + moto | cloud-lambda-tester | Cloud | No |
| Localstack | cloud-lambda-tester | Cloud | No |
| k6 load testing | cloud-lambda-tester | Cloud | No |
| HIPAA security testing | cloud-security-tester | Cloud | No |
| GDPR/MDR data retention | cloud-security-tester | Cloud | Shared with dhf-assembler (V&V) for regulatory documentation |
| AWS CDK testing | cloud-infra-tester | Cloud | No |
| SageMaker Pipelines | ml-validation-engineer | AI/ML | No |
| Statistical validation | ml-validation-engineer | AI/ML | No |
| ECG dataset curation | ml-data-scientist | AI/ML | No |
| FDA AI/ML SaMD guidance | ml-validation-engineer | AI/ML | Shared with dhf-assembler (V&V) for submission documentation |
| Playwright | dashboard-tester | V&V | No |
| axe-core accessibility | dashboard-tester | V&V | No |
| Traceability matrix generation | dhf-assembler | V&V | No |
| E2E orchestration (Python) | e2e-test-engineer | V&V | No |

### Skill Gaps

| Gap | Impact | Resolution |
|-----|--------|------------|
| No embedded ML validation specialist agent | ml-validation-engineer must cover both SageMaker pipeline automation and TFLM on-device validation; TFLM quantization testing is a specialized skill | Accept gap -- firmware-rust-tester covers TFLM integration from firmware side; ml-validation-engineer covers model validation from ML side; the gap is at the quantization boundary |
| No clinical data science agent | ml-data-scientist role requires domain expertise in ECG interpretation, arrhythmia classification ground truth, and clinical significance thresholds | Accept gap -- this role represents the human clinical data scientists on the team; the agent handles automation and tooling, not clinical judgment |
| No IEC 62304 compliance specialist agent | All squads need IEC 62304 awareness but no agent specializes in it | Accept gap -- squad leaders incorporate IEC 62304 requirements into task assignments; dhf-assembler validates traceability compliance at convergence |
| No Sentinel legacy analysis agent | Sentinel parity testing requires understanding the legacy system's behaviors | Source from complexity-reducer archetype or accept gap -- dashboard-tester can reverse-engineer Sentinel UI behaviors from documentation |
| No dedicated CI/CD agent | Test infrastructure requires GitHub Actions pipelines, SageMaker Pipelines, and self-hosted runner configuration | Accept gap -- distribute CI/CD work across squad leaders; each squad configures its own pipeline |

### Task Graph

```
Phase: FOUNDATION
-----------------
Task 1: Define firmware software unit boundaries per IEC 62304 Class C
  -> Owner: firmware-rust-tester (Squad-Firmware)
  -> Done when: Every Rust module and C function is classified as a software unit with
     documented test obligation

Task 2: Define cloud software unit boundaries per IEC 62304 Class B (risk-based)
  -> Owner: cloud-security-tester (Squad-Cloud)
  -> Done when: Risk assessment identifies which Lambda functions require unit tests vs.
     integration-only coverage

Task 3: Define AI/ML validation strategy per FDA SaMD guidance
  -> Owner: ml-validation-engineer (Squad-AI/ML)
  -> Done when: Software Validation Plan section for AI/ML is written, reviewed by
     Regulatory Affairs, and committed

Task 4: Establish traceability matrix schema and test metadata tagging convention
  -> Owner: dhf-assembler (Squad-V&V)
  -> Done when: All squads agree on requirement ID -> test case ID tagging format,
     and one example trace exists per squad

Task 5: Set up CI/CD pipelines for all four sub-teams
  -> Owner: squad leaders (all squads)
  -> Parallel with: 1, 2, 3, 4
  -> Done when: GitHub Actions runs unit tests on push for firmware/cloud/frontend;
     SageMaker Pipeline runs model validation on model artifact change

═══ SYNC POINT: foundation-alignment (Software Validation Plan + traceability schema) ═══

Phase: CORE -- PARALLEL SQUAD EXECUTION
----------------------------------------
Task 6: Implement Rust ECG pipeline property-based tests (proptest)
  -> Owner: firmware-rust-tester (Squad-Firmware)
  -> Blocked by: 1
  -> Done when: Every signal processing module has proptest tests verifying bounded
     output, heartbeat rate range (20-300 BPM), and filter stability invariants

Task 7: Implement C BLE stack unit tests (CppUTest)
  -> Owner: firmware-c-tester (Squad-Firmware)
  -> Blocked by: 1
  -> Parallel with: 6
  -> Done when: Every C function in BLE stack has table-driven CppUTest tests; fault
     injection tests for corrupted packet handling exist

Task 8: Implement TFLM inference wrapper tests
  -> Owner: firmware-rust-tester (Squad-Firmware)
  -> Blocked by: 1, model artifact from Task 12
  -> Done when: Frozen-weights deterministic tests pass; inference timing test verifies
     <50ms on nRF5340 (via HIL bench)

Task 9: Implement QEMU firmware integration tests
  -> Owner: firmware-integration (Squad-Firmware)
  -> Blocked by: 6, 7
  -> Done when: Full pipeline test (ECG input -> event detection -> BLE transmission)
     passes on QEMU with mocked BLE peripherals

Task 10: Implement Lambda unit tests and Kinesis integration tests
  -> Owner: cloud-lambda-tester (Squad-Cloud)
  -> Blocked by: 2
  -> Done when: All business-logic Lambda functions have pytest unit tests; ingestion
     pipeline integration test runs against Localstack

Task 11: Implement HIPAA security control tests and DSAR workflow tests
  -> Owner: cloud-security-tester (Squad-Cloud)
  -> Blocked by: 2
  -> Parallel with: 10
  -> Done when: Encryption at rest (S3), encryption in transit (TLS), RBAC (Cognito),
     audit logging (CloudTrail), DSAR export, and DSAR deletion (with MDR retention
     exception) each have passing tests

Task 12: Build golden model snapshot and statistical validation suite
  -> Owner: ml-validation-engineer (Squad-AI/ML)
  -> Blocked by: 3
  -> Done when: 20 curated ECG segments have deterministic input/output tests with frozen
     weights; statistical validation runs against MIT-BIH and Cardiax datasets; VF
     sensitivity >= 99.0% and overall accuracy >= 95.0% thresholds are enforced

Task 13: Build predetermined change control plan test infrastructure
  -> Owner: ml-validation-engineer (Squad-AI/ML)
  -> Blocked by: 12
  -> Done when: SageMaker Pipeline automatically validates new model versions against
     predicate model; regression on any metric blocks deployment

Task 14: Curate and validate ECG datasets for model validation
  -> Owner: ml-data-scientist (Squad-AI/ML)
  -> Parallel with: 12
  -> Done when: MIT-BIH and Cardiax datasets are versioned, annotation quality is
     verified, and statistical threshold justification is documented

Task 15: Implement clinical dashboard component and accessibility tests
  -> Owner: dashboard-tester (Squad-V&V)
  -> Blocked by: 4
  -> Done when: All clinician-facing views have Jest + RTL tests; axe-core WCAG 2.1 AA
     tests pass on all pages; 70% line coverage floor met

Task 16: Build Sentinel parity regression suite
  -> Owner: dashboard-tester (Squad-V&V)
  -> Parallel with: 15
  -> Done when: Sentinel clinical behaviors are catalogued, mapped to Atreus equivalents,
     and regression tests verify clinical equivalence for same input data

═══ SYNC POINT: coverage-checkpoint (per-squad coverage reports + test status) ═══

Phase: INTEGRATION
------------------
Task 17: Implement BLE protocol forward-compatibility tests
  -> Owner: firmware-c-tester (Squad-Firmware)
  -> Blocked by: 7
  -> Done when: Tests verify that new firmware versions work with deployed relay unit
     (Raspberry Pi) BLE client; protocol versioning strategy is validated

Task 18: Implement SageMaker endpoint integration tests
  -> Owner: cloud-infra-tester (Squad-Cloud)
  -> Blocked by: 10, 12 (model artifact)
  -> Done when: Cloud ingestion pipeline correctly invokes SageMaker inference endpoint
     and processes classification results

Task 19: Build end-to-end test orchestration harness
  -> Owner: e2e-test-engineer (Squad-V&V)
  -> Blocked by: 9, 10, 15
  -> Done when: Python harness sequences ECG signal generator -> nRF5340 DK ->
     BLE sniffer -> relay unit -> cloud ingestion -> AI classification ->
     dashboard alert; harness runs unattended

Task 20: Implement Playwright E2E tests for critical clinician workflows
  -> Owner: dashboard-tester (Squad-V&V)
  -> Blocked by: 15
  -> Done when: Three clinician workflows (review alert, view ECG strip, dismiss/escalate
     event) pass in Playwright against staging

═══ SYNC POINT: integration-validation (E2E test green, cross-boundary tests passing) ═══

Phase: CONVERGENCE
------------------
Task 21: Execute nightly E2E test and verify 5-minute alert SLA
  -> Owner: e2e-test-engineer (Squad-V&V)
  -> Blocked by: 19
  -> Done when: Nightly E2E test runs unattended on HIL bench; 5-minute SLA is verified;
     PagerDuty alert triggers on regression

Task 22: Generate traceability matrix from test metadata
  -> Owner: dhf-assembler (Squad-V&V)
  -> Blocked by: 6, 7, 8, 9, 10, 11, 12, 13, 15, 17, 18, 20
  -> Done when: Every design requirement ID maps to at least one test case ID;
     traceability matrix is auto-generated and renders as auditable document

Task 23: Assemble DHF verification and validation report
  -> Owner: dhf-assembler (Squad-V&V)
  -> Blocked by: 22
  -> Done when: Complete V&V report with coverage reports, test results, traceability
     matrix, tool version manifests, and regulatory cross-references is assembled
     and reviewed by Regulatory Affairs

Task 24: Conduct quarterly test health review (first iteration)
  -> Owner: e2e-test-engineer (Squad-V&V)
  -> Blocked by: 21, 22
  -> Done when: Coverage trends, flaky test rates, and test execution times across all
     four sub-teams are compiled and presented

═══ CONVERGENCE: DHF assembly complete; 510(k) test package ready for submission ═══
```

### Sync Point Details

#### SP1: foundation-alignment

| Field | Value |
|-------|-------|
| Initiated by | dhf-assembler (Squad-V&V) |
| Validated by | team-lead |
| Artifact format | Markdown (Software Validation Plan + traceability schema) |
| Minimum content | (1) IEC 62304 class assignment per sub-team, (2) unit definition per sub-team, (3) test obligation per software unit, (4) traceability tagging convention with one example per squad, (5) AI/ML validation strategy approved by Regulatory Affairs |
| Gate condition | All four squads have confirmed their unit boundaries and test obligations; Regulatory Affairs has reviewed the AI/ML validation strategy |
| Failure action | Block core phase; team-lead mediates disagreements on unit boundaries or AI/ML validation approach |

#### SP2: coverage-checkpoint

| Field | Value |
|-------|-------|
| Initiated by | squad-leaders (all squads) |
| Validated by | team-lead |
| Artifact format | Coverage reports (per-squad) + test status summary |
| Minimum content | (1) Per-squad test count and pass/fail status, (2) coverage metrics vs. targets (Class C: 100% unit, Class B: risk-based, AI/ML: statistical thresholds, Frontend: 70% line), (3) identified blockers or scope changes |
| Gate condition | None (informational checkpoint) -- but team-lead may trigger corrective action if any squad is significantly behind target |
| Failure action | Team-lead works with affected squad leader to re-scope or re-prioritize |

#### SP3: integration-validation

| Field | Value |
|-------|-------|
| Initiated by | e2e-test-engineer (Squad-V&V) |
| Validated by | team-lead + all squad-leaders |
| Artifact format | E2E test results + cross-boundary test results |
| Minimum content | (1) E2E test passes at least once end-to-end, (2) BLE forward-compatibility tests pass, (3) SageMaker endpoint integration tests pass, (4) Playwright clinician workflow tests pass |
| Gate condition | E2E test demonstrates the 5-minute alert path works at least once; all cross-boundary integration tests pass |
| Failure action | Block convergence; team-lead coordinates debugging across affected squads |

#### SP4: model-artifact-handoff

| Field | Value |
|-------|-------|
| Initiated by | ml-validation-engineer (Squad-AI/ML) |
| Validated by | firmware-rust-tester (Squad-Firmware) + cloud-infra-tester (Squad-Cloud) |
| Artifact format | Frozen model artifact (TFLM .tflite + PyTorch .pt) + validation report |
| Minimum content | (1) Frozen model weights with version tag, (2) 20 deterministic input/output pairs, (3) statistical validation results meeting hard-fail thresholds, (4) quantization accuracy comparison (float32 vs. int8) |
| Gate condition | Model artifact passes golden snapshot tests; statistical thresholds met; quantization accuracy degradation is within documented tolerance |
| Failure action | Block firmware TFLM integration (Task 8) and cloud SageMaker integration (Task 18); ml-validation-engineer investigates and retrains or adjusts thresholds with clinical data scientist input |

#### SP5: dhf-assembly (convergence)

| Field | Value |
|-------|-------|
| Initiated by | dhf-assembler (Squad-V&V) |
| Validated by | team-lead + Regulatory Affairs (external) |
| Artifact format | Design History File package (traceability matrix, coverage reports, test results, tool manifests) |
| Minimum content | (1) Every design requirement has at least one traced test case, (2) All coverage targets met, (3) All test results archived with version metadata, (4) AI/ML validation report complete, (5) E2E nightly test operational |
| Gate condition | Regulatory Affairs confirms DHF is sufficient for 510(k) submission |
| Failure action | Team-lead identifies gaps; affected squads remediate; dhf-assembler re-assembles |

### Convergence Protocol

| Field | Value |
|-------|-------|
| Driver | dhf-assembler (Squad-V&V) |
| Participants | One representative per squad (firmware-rust-tester, cloud-security-tester, ml-validation-engineer, e2e-test-engineer) |
| Artifacts compared | Per-squad coverage reports vs. IEC 62304 requirements; traceability matrix completeness; E2E test results; AI/ML validation report |
| Method | dhf-assembler collects all squad artifacts, runs traceability matrix generator, identifies unmapped requirements, reports gaps to squad representatives |
| Success criteria | Zero unmapped design requirements; all coverage targets met; E2E nightly test operational and green for 7 consecutive runs; AI/ML statistical thresholds met; Regulatory Affairs sign-off |
| On discrepancy | Unmapped requirement: assigned to owning squad for test creation. Coverage shortfall: squad leader re-prioritizes. E2E failure: team-lead coordinates cross-squad debugging. AI/ML threshold miss: model retraining with clinical data scientist review |
| Max iterations | 3 convergence cycles before escalation to VP of Engineering |
| Output artifact | 510(k)-ready Design History File verification and validation package |

### Coordination Overhead

| Metric | Value |
|--------|-------|
| Squad-leaders needed | 4 (one per squad) |
| Design phase | FULL (regulatory complexity warrants thorough foundation phase with Regulatory Affairs alignment) |
| Announcer needed | YES (team size > 5 per squad when counting cross-squad liaisons; team-lead broadcasts sync point status to all squad leaders) |
| Total communication channels | 17 (3 mesh + 3 hub-spoke + 1 pair + 3 hub-spoke + 5 cross-squad sync + 2 team-lead broadcast) |
| Flat mesh equivalent | 120 channels (16 agents in full mesh) |
| **Channel reduction** | **86%** |

### Risks

| Risk | Mitigation |
|------|------------|
| AI/ML team has never written automated tests; cultural resistance to "test-ifying" statistical validation | Squad-AI/ML leader frames validation pipeline as regulatory obligation (FDA SaMD), not cultural preference; ml-data-scientist focuses on dataset quality while ml-validation-engineer handles automation |
| QEMU nRF5340 emulation is incomplete; firmware integration tests may be unreliable | firmware-integration uses mocked BLE peripherals and focuses QEMU tests on application-core-only logic; HIL bench covers full integration; accept QEMU limitations and document coverage gaps |
| End-to-end test requires physical hardware (HIL bench); cannot run in cloud CI | E2E test runs nightly on self-hosted runner with HIL bench access; PagerDuty alerting on failure; e2e-test-engineer documents HIL bench setup for reproducibility |
| GDPR right-to-erasure vs. MDR 10-year retention creates ambiguous test requirements | cloud-security-tester implements both deletion and retention paths with clear code comments and tests; Regulatory Affairs provides written interpretation before tests are finalized |
| Sentinel parity testing requires understanding an 8-year-old legacy system with no automated tests | dashboard-tester works from Sentinel clinical documentation and recorded user workflows; Clinical Affairs validates parity mapping; accept that 100% behavioral parity is not achievable or necessary |
| Four squads create coordination overhead; sync points may become bottlenecks | team-lead monitors sync point cadence; coverage-checkpoint is intentionally informational (no blocking gate) to reduce sync friction; only foundation-alignment and integration-validation are hard gates |
| IEC 62304 Class C "every software unit" mandate may create unsustainable test maintenance burden | firmware-rust-tester defines "software unit" at module level (not function level) where architecturally justified; documents rationale for unit boundary decisions in DHF |
| Context exhaustion in opus-model agents handling regulatory + technical dual concerns | Squad-AI/ML kept to 2 workers (pair topology) to minimize coordination overhead; Squad-Firmware mesh limited to 3 workers; dhf-assembler uses sonnet since document assembly is structured, not reasoning-heavy |
| Model quantization (float32 -> int8) may degrade arrhythmia detection accuracy below FDA thresholds | ml-validation-engineer tests quantized model separately from full-precision model; quantization accuracy degradation is explicitly measured and documented; if degradation exceeds tolerance, model architecture is revised before deployment |

---

## Part B: Squad Configuration

```yaml
formation:
  name: tdd-enterprise-medical
  scenario: atreus-icm-telemetry
  version: "1.0.0"
  structure: multi-squad-convergent-pipeline
  task: >
    Establish TDD processes and test infrastructure across four sub-teams (Firmware, Cloud,
    AI/ML, Frontend) for an implantable cardiac monitor platform, producing a 510(k)-ready
    Design History File with full requirement-to-test traceability, IEC 62304 Class C/B
    coverage, FDA AI/ML SaMD statistical validation, HIPAA security tests, and automated
    end-to-end patient safety path verification.
  ready_to_proceed: false  # skill gaps in embedded-ML-validation, clinical-data-science, HIL-bench-automation

  team_lead:
    pattern: hub-and-spoke-with-convergence-gate
    topology: star
    channels: 5

  squads:
    - name: squad-firmware
      task: >
        Implement IEC 62304 Class C TDD for nRF5340 firmware: Rust ECG pipeline property-based
        tests, C BLE stack unit tests, TFLM inference wrapper tests, QEMU integration tests,
        BLE forward-compatibility tests, and HIL bench automation.
      pattern: small-mesh
      topology: mesh
      channels: 3
      briefing_context: |
        You are testing firmware for a Class C medical device (IEC 62304). Every software unit
        must have automated test coverage. The firmware runs on a dual-core nRF5340: Rust/Embassy
        on the application core (ECG processing + TFLM inference) and C/Zephyr on the network core
        (BLE 5.3 communication). Host-based tests run on x86-64 with different FP semantics than
        the ARM Cortex-M33 target -- accept this limitation and document it. QEMU emulation is
        incomplete for BLE peripherals; mock them. The HIL bench is the ground truth for
        integration testing.
      leader:
        agent: squad-leader
        model: opus
        design_phase: full
      workers:
        - name: firmware-rust-tester
          source_agent: testing-expert
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "IEC 62304 Class C + proptest strategy requires deep reasoning"
          archetype: specialist
          skills:
            - name: rust-embedded-testing
            - name: proptest-property-based
            - name: tflm-inference-testing
              shared_with: ml-validation-engineer
          role: "Rust ECG pipeline test lead -- property-based tests, TFLM wrapper tests, Class C coverage"
          briefing_context: |
            Focus on proptest invariants for signal processing (bounded output, BPM range 20-300,
            filter stability). For TFLM, use frozen model weights from Squad-AI/ML and test
            deterministic input/output pairs plus 50ms inference budget on HIL bench. Tag all
            test cases with requirement IDs for traceability matrix.

        - name: firmware-c-tester
          source_agent: independent-contributor
          spawn_type: independent-contributor-sonnet
          model: sonnet
          model_rationale: "Table-driven CppUTest generation is well-scoped; sonnet sufficient"
          archetype: implementer
          skills:
            - name: cpputest-unit-testing
            - name: ble-protocol-testing
              shared_with: e2e-test-engineer
          role: "C BLE stack unit tests, fault injection, protocol forward-compatibility tests"
          briefing_context: |
            Generate table-driven CppUTest tests for every C function in the BLE stack. Include
            fault injection tests for corrupted packets (IEC 60601-1-2 resilience). Test
            forward-compatibility: new firmware must work with deployed relay unit BLE client.

        - name: firmware-integration
          source_agent: testing-expert
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "QEMU mocking strategy and host/target test layer design need deep reasoning"
          archetype: specialist
          skills:
            - name: qemu-emulation-testing
            - name: hil-bench-automation
              shared_with: e2e-test-engineer
          role: "QEMU integration tests, HIL bench automation, cross-core integration, host-vs-target strategy"

    - name: squad-cloud
      task: >
        Implement IEC 62304 Class B TDD for AWS cloud platform: Lambda unit tests (pytest + moto),
        Kinesis ingestion integration tests (Localstack), HIPAA security control tests, GDPR/MDR
        DSAR workflow tests, SageMaker endpoint integration, k6 load tests.
      pattern: supervisor-worker
      topology: hub-and-spoke
      channels: 3
      briefing_context: |
        You are testing a Class B (IEC 62304) cloud platform handling PHI (HIPAA). Risk-based
        unit test scope reduction is permitted: focus unit tests on business logic Lambdas, not
        simple routing/transformation. Integration tests against Localstack are the primary
        coverage mechanism. HIPAA security testing is a compliance obligation -- encryption,
        access control, audit logging, and DSAR workflows must each have dedicated tests. The
        GDPR vs. MDR data retention tension must be resolved: deletion requests remove all
        non-MDR-retained data; MDR-mandated data (10-year post-market surveillance) is preserved.
      leader:
        agent: squad-leader
        model: opus
        design_phase: short-circuit
      workers:
        - name: cloud-lambda-tester
          source_agent: independent-contributor
          spawn_type: independent-contributor-sonnet
          model: sonnet
          model_rationale: "pytest + moto patterns are well-established; sonnet sufficient"
          archetype: implementer
          skills:
            - name: pytest-aws-testing
            - name: localstack-integration
            - name: k6-load-testing
          role: "Lambda unit tests, Kinesis ingestion integration tests, k6 load tests"

        - name: cloud-security-tester
          source_agent: web-bug-hunter
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "HIPAA/GDPR regulatory intersection + security control design requires deep reasoning"
          archetype: specialist
          skills:
            - name: hipaa-security-testing
            - name: gdpr-mdr-retention-testing
              shared_with: dhf-assembler
          role: "HIPAA security control tests, DSAR workflow tests, GDPR/MDR retention logic tests"
          briefing_context: |
            Each HIPAA technical safeguard needs a dedicated test: S3 bucket policy (encryption at
            rest), TLS enforcement (encryption in transit), Cognito role-based access, CloudTrail
            audit logging. DSAR tests must verify complete export AND deletion with MDR exception.
            Document the GDPR/MDR retention tension resolution in test comments.

        - name: cloud-infra-tester
          source_agent: independent-contributor
          spawn_type: independent-contributor-sonnet
          model: sonnet
          model_rationale: "CDK assertion patterns are structured; sonnet sufficient"
          archetype: implementer
          skills:
            - name: aws-cdk-testing
            - name: cognito-auth-testing
            - name: sagemaker-endpoint-integration
          role: "AWS CDK infrastructure tests, Cognito auth flow tests, SageMaker endpoint integration"

    - name: squad-ai-ml
      task: >
        Build AI/ML arrhythmia classification model validation infrastructure: golden model
        snapshot tests, statistical validation suite (MIT-BIH + Cardiax datasets), SageMaker
        Pipelines automation for predetermined change control plan, quantization accuracy
        comparison, and FDA AI/ML SaMD documentation.
      pattern: pair-programming
      topology: pair
      channels: 1
      briefing_context: |
        TDD does not apply to ML model development in a conventional sense. Your job is to build
        a regulatory-defensible statistical validation process, not unit tests for neurons. The
        golden model snapshot tests verify artifact integrity (not generalization). The statistical
        validation suite verifies clinical performance against hard-fail thresholds (VF sensitivity
        >= 99.0%, overall accuracy >= 95.0%). The predetermined change control plan test
        infrastructure (SageMaker Pipelines) automates predicate-model comparison for every new
        model version. All artifacts must be suitable for FDA AI/ML SaMD submission. Work closely
        with firmware-rust-tester on TFLM model artifact handoff and quantization accuracy.
      leader:
        agent: squad-leader
        model: opus
        design_phase: full
      workers:
        - name: ml-validation-engineer
          source_agent: testing-expert
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "FDA AI/ML SaMD + statistical validation pipeline design is reasoning-intensive"
          archetype: specialist
          skills:
            - name: ml-model-validation
            - name: sagemaker-pipelines
            - name: fda-samd-guidance
              shared_with: dhf-assembler
            - name: tflm-inference-testing
              shared_with: firmware-rust-tester
          role: "Golden model tests, statistical validation suite, SageMaker Pipelines, change control plan"

        - name: ml-data-scientist
          source_agent: research-methodology-expert
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "Dataset curation and statistical threshold justification require investigative reasoning"
          archetype: investigator
          skills:
            - name: ecg-dataset-curation
            - name: statistical-threshold-analysis
          role: "ECG dataset curation, annotation QA, threshold definition, clinical significance review"

    - name: squad-vv
      task: >
        Own cross-cutting verification and validation: end-to-end test orchestration (HIL bench
        + BLE + cloud + dashboard), clinical dashboard testing, Sentinel parity regression,
        Design History File assembly, traceability matrix generation, test result archival,
        and quarterly test health review.
      pattern: supervisor-worker-with-cross-squad-liaison
      topology: hub-and-spoke
      channels: 3
      briefing_context: |
        You own the artifacts that no single sub-team can produce alone. The E2E test is the most
        critical: it proves the 5-minute alert SLA by orchestrating ECG signal generator -> nRF5340
        -> BLE -> relay -> cloud -> AI -> dashboard. The DHF traceability matrix must auto-generate
        from test metadata (requirement ID tags in test names). You also own clinical dashboard
        testing (the frontend team's tests) and Sentinel parity regression. Your primary customer
        is Regulatory Affairs -- the DHF package must satisfy their 510(k) submission requirements.
      leader:
        agent: squad-leader
        model: opus
        design_phase: short-circuit
      workers:
        - name: e2e-test-engineer
          source_agent: testing-expert
          spawn_type: independent-contributor-opus
          model: opus
          model_rationale: "Cross-boundary E2E spanning 4 codebases, 3 languages, 2 hardware platforms requires deep reasoning"
          archetype: specialist
          skills:
            - name: e2e-orchestration-python
            - name: hil-bench-automation
              shared_with: firmware-integration
            - name: ble-protocol-testing
              shared_with: firmware-c-tester
          role: "E2E test harness, nightly execution, 5-minute alert SLA verification, PagerDuty alerting"

        - name: dashboard-tester
          source_agent: independent-contributor
          spawn_type: independent-contributor-sonnet
          model: sonnet
          model_rationale: "React Testing Library + Playwright patterns are well-established; sonnet sufficient"
          archetype: implementer
          skills:
            - name: react-testing-library
            - name: playwright-e2e
            - name: axe-core-accessibility
            - name: sentinel-parity-testing
          role: "Clinical dashboard component tests, accessibility tests, clinician workflow E2E, Sentinel parity"

        - name: dhf-assembler
          source_agent: document-maintainer
          spawn_type: independent-contributor-sonnet
          model: sonnet
          model_rationale: "Document assembly from structured metadata; precision-focused but not reasoning-heavy"
          archetype: documenter
          skills:
            - name: traceability-matrix-generation
            - name: coverage-report-aggregation
            - name: regulatory-document-assembly
            - name: gdpr-mdr-retention-testing
              shared_with: cloud-security-tester
            - name: fda-samd-guidance
              shared_with: ml-validation-engineer
          role: "DHF traceability matrix, test result archival, coverage aggregation, V&V report assembly"

  sync_points:
    - name: foundation-alignment
      type: gate
      from: squad-vv
      to: [squad-firmware, squad-cloud, squad-ai-ml]
      artifact: "Software Validation Plan + traceability schema"
      required: true
      initiated_by: dhf-assembler
      validated_by: team-lead
      gate_condition: "All squads confirm unit boundaries and test obligations; Regulatory Affairs approves AI/ML validation strategy"
      minimum_content:
        - "IEC 62304 class assignment per sub-team"
        - "Unit definition per sub-team"
        - "Test obligation per software unit"
        - "Traceability tagging convention with one example per squad"
        - "AI/ML validation strategy approved by Regulatory Affairs"

    - name: model-artifact-handoff
      type: artifact-transfer
      from: squad-ai-ml
      to: squad-firmware
      artifact: "Frozen model artifact (.tflite + .pt) + validation report + deterministic I/O pairs"
      required: true
      initiated_by: ml-validation-engineer
      validated_by: firmware-rust-tester
      minimum_content:
        - "Frozen model weights with version tag"
        - "20 deterministic input/output pairs"
        - "Statistical validation results meeting hard-fail thresholds"
        - "Quantization accuracy comparison (float32 vs. int8)"

    - name: model-cloud-handoff
      type: artifact-transfer
      from: squad-ai-ml
      to: squad-cloud
      artifact: "Cloud-side model artifact (.pt) + SageMaker endpoint configuration"
      required: true
      initiated_by: ml-validation-engineer
      validated_by: cloud-infra-tester
      minimum_content:
        - "PyTorch model artifact with version tag"
        - "SageMaker endpoint configuration"
        - "Expected inference latency and throughput"

    - name: firmware-test-vectors
      type: artifact-transfer
      from: squad-firmware
      to: squad-vv
      artifact: "BLE protocol test vectors for E2E test harness"
      required: true
      initiated_by: firmware-c-tester
      validated_by: e2e-test-engineer
      minimum_content:
        - "Known arrhythmia BLE event payloads (protobuf)"
        - "Expected BLE GATT service/characteristic UUIDs"
        - "Protocol version compatibility matrix"

    - name: coverage-checkpoint
      type: bidirectional-check
      between: [squad-firmware, squad-cloud, squad-ai-ml, squad-vv]
      artifact: "Per-squad coverage reports + test status summary"
      required: false

    - name: integration-validation
      type: gate
      from: squad-vv
      to: [squad-firmware, squad-cloud, squad-ai-ml]
      artifact: "E2E test results + cross-boundary integration results"
      required: true
      initiated_by: e2e-test-engineer
      validated_by: team-lead
      gate_condition: "E2E test demonstrates 5-minute alert path; all cross-boundary tests pass"
      minimum_content:
        - "E2E test passes at least once"
        - "BLE forward-compatibility tests pass"
        - "SageMaker endpoint integration tests pass"
        - "Playwright clinician workflow tests pass"

    - name: dhf-assembly
      type: gate
      from: squad-vv
      to: team-lead
      artifact: "510(k)-ready Design History File V&V package"
      required: true
      initiated_by: dhf-assembler
      validated_by: team-lead
      gate_condition: "Regulatory Affairs confirms DHF is sufficient for 510(k) submission"
      minimum_content:
        - "Complete traceability matrix (requirement -> test case)"
        - "All coverage targets met"
        - "All test results archived with version metadata"
        - "AI/ML validation report complete"
        - "E2E nightly test operational for 7+ consecutive green runs"

  skill_gaps:
    - domain: embedded-ml-validation
      affects: ml-validation-engineer
      source_candidate: "create new -- no existing agent covers TFLM quantization boundary testing"
    - domain: clinical-data-science
      affects: ml-data-scientist
      source_candidate: "accept gap -- represents human clinical data scientists; agent handles automation"
    - domain: iec-62304-compliance
      affects: all squads
      source_candidate: "accept gap -- distributed across squad leaders; dhf-assembler validates at convergence"
    - domain: sentinel-legacy-analysis
      affects: dashboard-tester
      source_candidate: "complexity-reducer agent or accept gap -- work from documentation"
    - domain: cicd-pipeline-configuration
      affects: all squads
      source_candidate: "accept gap -- distributed across squad leaders; each squad configures own pipeline"
```

---

## Part C: Pattern Rationale

This formation splits the work along **sub-team domain boundaries** rather than along the design-vs-implementation axis used in simpler formations (e.g., cloud-infrastructure). The rationale is that TDD for medical device software is fundamentally domain-specific: firmware TDD (property-based tests for signal processing invariants, IEC 62304 Class C coverage mandates) has nothing in common with AI/ML validation (statistical performance thresholds, FDA SaMD predetermined change control plans). Forcing these domains into a single squad would create a mesh where agents have no shared vocabulary. The four-squad structure lets each squad operate with domain-appropriate testing patterns while the V&V squad provides the integrating force.

The critical design choice is the **dedicated V&V squad** rather than distributing V&V responsibilities across the domain squads. In a less regulated context, each squad could own its own validation and produce reports for a document assembler. But in an IEC 62304 + FDA 510(k) context, the Design History File is a first-class deliverable that requires cross-squad artifact aggregation, traceability analysis, and Regulatory Affairs coordination. No domain squad has the mandate or context to own this. The V&V squad also owns the end-to-end test -- the single most important test in the entire system -- which crosses all four domains and requires physical hardware coordination. Without a dedicated squad, this test would be perpetually deprioritized by domain squads focused on their own coverage targets.

The **AI/ML squad uses a pair topology** rather than a mesh or hub-and-spoke because there are only two workers with deeply complementary skills (automation engineer + data scientist). A mesh of two is already a pair, and adding a third agent would be artificial. The pair topology minimizes coordination overhead for a squad whose work is inherently collaborative -- the data scientist defines what to validate while the validation engineer automates how to validate it. The firmware squad uses a mesh because the three agents must debate host-vs-target test strategy, QEMU mocking approaches, and the boundary between Rust and C testing -- these are design conversations, not task assignments. The cloud and V&V squads use hub-and-spoke because their work is well-scoped and can be distributed as independent tasks by the squad leader.

This formation would be over-engineered for any project below the "Enterprise in high-regulation" maturity level. An MVP or V1 project would not need a V&V squad, a DHF assembly pipeline, or a separate AI/ML validation pair. The formation is also specific to the "embedded + security + cloud + ML" intersection -- a purely cloud-native regulated system (e.g., a SaaS EHR) would not need a firmware squad or HIL bench coordination.

### Formation Variants

| Scenario | Variant | Changes from default |
|----------|---------|---------------------|
| Pre-510(k) submission (final 3 months) | Convergence-heavy | Squad-Firmware and Squad-Cloud shift to maintenance mode (fixing test gaps); Squad-V&V doubles down on DHF assembly and E2E stability; Squad-AI/ML focuses exclusively on predetermined change control plan documentation |
| Post-510(k) (year 2, maintenance) | Reduced formation | Drop Squad-AI/ML (model frozen); Squad-V&V absorbs dashboard testing; Squad-Firmware and Squad-Cloud merge into single maintenance squad; 2 squads total |
| No AI/ML component (simpler ICM) | Three-squad | Drop Squad-AI/ML entirely; cloud-infra-tester handles SageMaker removal; V&V squad scope reduced; 3 squads with 9 workers total |
| Single-language firmware (all C, no Rust) | Firmware simplification | firmware-rust-tester replaced with second CppUTest implementer; proptest removed; mesh topology may reduce to hub-and-spoke |
