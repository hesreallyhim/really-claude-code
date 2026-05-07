---
Name: "TDD Squad Pre-Spec Planning Doc: Scenario 5 -- Atreus"
Goal: Formulate the factors that will guide the development of the Squad Formation Profiles for the Atreus Implantable Cardiac Monitor Firmware and Cloud Telemetry Platform.
Scenario: 5 (Atreus)
Instructions: Completed document based on tdd.md template, populated for enterprise-in-high-regulation medical device platform.
Date: 2026-02-14
---

# TDD -- Scenario 5: Atreus

## Given:

- A specification with clear AC and functional and non-functional requirements for an implantable cardiac monitor (ICM) and companion cloud telemetry platform, replacing the legacy Sentinel system
- A classification of the project into:
    - **Enterprise in high-regulation**
- A domain area:
    - **Embedded systems + Security-related** (intersection)
- A rough timeline:
    - **One year**
- Additional context:
    - **Legacy migration** (replacing Sentinel platform -- 8 years in production, proprietary radio protocol, on-premise server, no AI classification)
    - **28 engineers across four sub-teams** (Firmware, Cloud/Backend, AI/ML, Frontend) plus QA, Regulatory Affairs, and Clinical Affairs
    - **FDA 510(k) submission deadline: February 2027**
    - **Regulatory surface:** IEC 62304 Class C (firmware), Class B (cloud), FDA 21 CFR 820, HIPAA, GDPR, EU MDR 2017/745, IEC 60601-1-2, FDA AI/ML SaMD guidance

---

## The squads must:

1. **Establish sub-team-specific TDD processes that satisfy IEC 62304 classification requirements while acknowledging that "unit" and "test" mean different things for firmware, cloud, AI/ML, and frontend sub-teams.** IEC 62304 Class C mandates unit testing of every software unit in the firmware. Class B mandates integration testing with risk-based unit test scope reduction for the cloud platform. The AI/ML model is regulated as SaMD and requires statistical validation (sensitivity/specificity/PPV/F1) rather than deterministic unit tests. The frontend has no regulatory mandate but must meet the VP of Engineering's 70% line coverage floor. The squads must produce a unified "Software Validation Plan" that documents how each sub-team's testing approach satisfies its regulatory classification, without forcing a single TDD process onto sub-teams where it does not apply.

2. **Build and maintain a multi-layer test infrastructure that spans four codebases, three languages (C, Rust, Python/TypeScript), two hardware platforms (nRF5340 application core and network core), and a cloud boundary.** This infrastructure must support:
    - Host-based unit tests for firmware (CppUTest for C/BLE, `cargo test` + `proptest` for Rust/ECG pipeline)
    - QEMU-based firmware integration tests with mocked BLE peripherals
    - Hardware-in-the-loop (HIL) tests on the nRF5340 dev kit with ECG signal generator
    - AWS service-mocked unit tests (pytest + moto) and integration tests (Localstack) for cloud Lambdas
    - Statistical model validation suites (SageMaker Pipelines) for the AI/ML arrhythmia classifier
    - Component tests (Jest + React Testing Library) and E2E tests (Playwright) for the clinical dashboard
    - One fully automated end-to-end test crossing the firmware-BLE-relay-cloud-dashboard boundary

3. **Produce a complete, auditable Design History File (DHF) where every design requirement traces to at least one automated test result.** The DHF is the central regulatory deliverable for the FDA 510(k) submission. Test results must be archived with exact tool versions, compiler versions, and test framework versions. The traceability matrix (requirement ID to test case ID) must be generated from test metadata, not maintained manually. Coverage reports must be generated automatically and archived with each build.

4. **Implement and verify HIPAA technical safeguards through dedicated security tests.** Encryption at rest, encryption in transit, role-based access control, audit logging, and data subject access request (DSAR) workflows must each have dedicated automated test coverage. GDPR/MDR data retention tension (right-to-erasure vs. 10-year post-market surveillance retention) must be resolved in code and verified by test.

5. **Validate the AI/ML arrhythmia classification model through a reproducible, automated statistical validation pipeline that satisfies FDA AI/ML SaMD guidance.** This includes:
    - Deterministic "golden model" snapshot tests (frozen weights, known input/output pairs) to detect corruption or inadvertent retraining
    - Statistical performance validation against curated ECG databases (MIT-BIH, Cardiax-annotated) with hard-fail thresholds (VF sensitivity >= 99.0%, overall accuracy >= 95.0%)
    - Predetermined change control plan testing: when a new model version is trained, automated comparison against the predicate model's performance, with regression on any metric blocking deployment
    - Documentation and artifact generation suitable for inclusion in the 510(k) submission

6. **Automate the end-to-end critical patient safety path ("arrhythmia detected on device -> clinician alerted on dashboard within 5 minutes") and run it nightly.** This test crosses all four sub-teams' codebases and requires coordination of the ECG signal generator (HIL bench), BLE sniffer, relay unit, cloud ingestion pipeline, AI classification, and clinical dashboard. No single sub-team owns this test. The squads must collectively build and maintain the test infrastructure, with QA team ownership of the orchestration layer.

7. **Ensure Sentinel-to-Atreus migration parity and regression coverage.** The legacy Sentinel platform's clinical behaviors (event detection, transmission, clinician review workflows) must be catalogued and mapped to Atreus equivalents. Regression tests must verify that Atreus produces clinically equivalent outcomes for the same input data. Parity gaps must be documented and reviewed with Clinical Affairs.

8. **Maintain BLE protocol forward-compatibility and resilience testing.** The BLE relay unit (Raspberry Pi in patients' homes) cannot be reliably updated. The custom GATT profile must be tested for forward-compatibility (new firmware versions must work with deployed relay units). IEC 60601-1-2 EMC resilience requires the BLE stack to handle corrupted packets gracefully -- this must be tested at the firmware level with fault-injection tests.

---

## IN ORDER TO DO THAT, THE SQUADS MUST HAVE:

### Skills

| Category | Required Skills |
|----------|----------------|
| **Firmware languages** | Rust (Embassy async runtime), C (Zephyr RTOS / nRF Connect SDK), ARM Cortex-M33 architecture |
| **Firmware testing** | CppUTest (C unit tests), `cargo test` + `proptest` (Rust property-based tests), QEMU nRF5340 emulation, HIL bench operation |
| **Embedded ML** | TensorFlow Lite for Microcontrollers (TFLM), 8-bit integer quantization, inference profiling on Cortex-M33 |
| **BLE protocol** | BLE 5.3, coded PHY, custom GATT profile design, protobuf serialization, BLE sniffer analysis |
| **Cloud/Backend** | AWS CDK (TypeScript), Lambda, Kinesis Data Streams, S3, DynamoDB, SageMaker, Cognito, CloudWatch, API Gateway |
| **Cloud testing** | pytest, moto (AWS mocking), Localstack, k6 (load testing) |
| **AI/ML** | PyTorch (cloud-side model training), TensorFlow Lite (on-device inference), SageMaker Pipelines, ECG signal processing, arrhythmia classification |
| **AI/ML validation** | Statistical validation methodology (sensitivity, specificity, PPV, F1), dataset curation, model comparison, FDA AI/ML SaMD predetermined change control |
| **Frontend** | React 18, Next.js, WCAG 2.1 AA accessibility |
| **Frontend testing** | Jest, React Testing Library, Playwright, axe-core |
| **Cross-cutting** | Protobuf schema design, CI/CD (GitHub Actions), Python scripting (HIL orchestration, E2E test harness), Docker/containerization |

### Knowledge

| Category | Required Knowledge |
|----------|-------------------|
| **IEC 62304** | Class B and Class C software lifecycle requirements, unit testing mandates, coverage analysis requirements, software unit definition, integration testing, system testing |
| **FDA 21 CFR Part 820** | Design History File structure, design inputs/outputs, verification vs. validation, design reviews, traceability requirements |
| **HIPAA** | Technical safeguards (encryption, access control, audit logging), DSAR workflows, breach notification |
| **GDPR** | Data subject rights, right to erasure, data portability, tension with MDR Article 10(8) retention requirements |
| **EU MDR 2017/745** | Clinical evaluation, post-market surveillance, UDI system, SaMD classification under MDCG 2019-11 |
| **FDA AI/ML SaMD guidance** | Predetermined change control plan, good machine learning practice (GMLP), locked vs. adaptive algorithms |
| **IEC 60601-1-2** | EMC testing implications for BLE protocol resilience |
| **OIML/metrology (reference)** | Not directly applicable but useful for understanding calibration verification patterns from Sentinel legacy |

### Tooling

| Category | Required Tooling |
|----------|-----------------|
| **Firmware dev** | nRF Connect SDK, Zephyr RTOS, Embassy (Rust async for embedded), ARM GCC cross-compiler, nRF5340 DK |
| **Firmware test** | QEMU with nRF5340 support (partial -- GPIO and BLE must be mocked), CppUTest, cargo test, proptest |
| **HIL bench** | nRF5340 development kit, BLE sniffer, ECG signal generator (DAC replaying recorded waveforms), Python orchestration scripts |
| **Cloud dev** | AWS CDK, SAM CLI, Docker |
| **Cloud test** | Localstack, moto, k6 |
| **AI/ML** | SageMaker (training + Pipelines), Jupyter notebooks (exploration), MIT-BIH Arrhythmia Database, Cardiax-annotated ECG dataset |
| **Frontend test** | Playwright (E2E), Jest (unit), axe-core (accessibility) |
| **E2E orchestration** | Custom Python harness coordinating HIL bench + BLE monitor + cloud API polling + dashboard verification |
| **CI/CD** | GitHub Actions (firmware, cloud, frontend), SageMaker Pipelines (AI/ML), self-hosted runners (for HIL bench access) |
| **Regulatory documentation** | Traceability matrix generator (test metadata -> requirement mapping), coverage report archival, version-pinned build manifests |

### Organizational Needs

| Category | Requirement |
|----------|-------------|
| **QA team** | Ownership of the V&V (Verification & Validation) process, end-to-end test orchestration, HIL bench operation, test result archival, quarterly test health reviews |
| **Regulatory Affairs** | Alignment on Software Validation Plan structure, IEC 62304 class interpretations, FDA AI/ML SaMD predetermined change control plan review, 510(k) submission package assembly |
| **Clinical Affairs** | Cardiologist advisory panel for arrhythmia classification ground truth, Sentinel-to-Atreus clinical parity review, clinical evaluation report input |
| **Clinical data scientists** | ECG dataset curation (MIT-BIH + proprietary), annotation quality assurance, statistical validation threshold definition, model performance reporting |
| **Cross-team coordination** | A dedicated integration lead or rotating integration duty across sub-team leads to own the firmware-BLE-cloud-dashboard boundary and the nightly E2E test |
| **VP of Engineering** | Quarterly test health review sponsorship, TDD mandate reconciliation with AI/ML statistical validation reality, coverage floor enforcement |

---

# THE TEAM WILL CONSIST OF:

This is a large-scale, multi-squad formation reflecting the four engineering sub-teams, the cross-cutting QA/regulatory concerns, and the fundamentally different testing philosophies required across the platform.

## Squad 1: Firmware Test Engineering (Squad-Firmware)

**Purpose:** Own TDD for the nRF5340 firmware -- both the Rust ECG signal processing pipeline (application core) and the C BLE communication stack (network core). This squad produces the IEC 62304 Class C unit test coverage, property-based tests for signal processing invariants, TFLM inference wrapper tests with frozen model weights, QEMU-based integration tests, and BLE protocol resilience/forward-compatibility tests.

**Central challenge:** IEC 62304 Class C requires unit testing of every software unit. The firmware has two languages (Rust, C), two cores (application, network), and an on-device ML model. "Unit" must be defined precisely for each: a Rust module, a C function, and a frozen-weights inference checkpoint. The squad must also bridge the gap between host-based tests (fast, x86-64, different FP semantics) and target-based tests (slow, ARM Cortex-M33, real hardware), accepting that no single layer provides complete confidence.

**Coordination:** Produces BLE protocol test vectors consumed by Squad-Cloud for relay-side testing. Produces firmware test coverage reports consumed by Squad-V&V for DHF assembly. Participates in nightly E2E test via HIL bench.

## Squad 2: Cloud and Backend Test Engineering (Squad-Cloud)

**Purpose:** Own TDD for the AWS cloud platform -- the ingestion pipeline (API Gateway -> Kinesis -> Lambda -> DynamoDB + S3), the SageMaker inference endpoint, Cognito authentication, and all HIPAA/GDPR security controls. This squad produces IEC 62304 Class B integration tests, HIPAA security control tests, DSAR workflow tests, and load tests.

**Central challenge:** Class B allows risk-based reduction of unit test scope, but HIPAA mandates security testing as a compliance obligation. The squad must determine which Lambda functions warrant unit tests (business logic) vs. which are adequately covered by integration tests (simple routing/transformation). The GDPR vs. MDR data retention tension must be resolved in code and validated by test: deletion requests must remove all non-MDR-retained data while preserving MDR-mandated post-market surveillance data.

**Coordination:** Consumes BLE protocol test vectors from Squad-Firmware for relay-to-cloud handoff testing. Consumes model artifacts from Squad-AI/ML for SageMaker endpoint integration testing. Produces cloud test coverage reports and HIPAA audit test results consumed by Squad-V&V.

## Squad 3: AI/ML Validation Engineering (Squad-AI/ML)

**Purpose:** Own validation for the arrhythmia classification model -- both on-device (TFLM quantized) and cloud-side (PyTorch). This squad produces the deterministic golden model snapshot tests, the statistical validation suite against curated ECG databases, the predetermined change control plan test infrastructure (SageMaker Pipelines), and the model performance comparison framework.

**Central challenge:** TDD does not apply to ML model development in any conventional sense. You cannot write a failing test, then train a model to pass it -- that is overfitting, not TDD. The squad must translate the VP of Engineering's TDD mandate into a regulatory-defensible statistical validation process: "given this dataset, the model's performance must meet or exceed these thresholds, and any new model version must be compared against the predicate model before deployment." The squad must also bridge the gap between the clinical data scientists (who think in terms of sensitivity/specificity/clinical significance) and the QA team (who think in terms of test cases that pass or fail).

**Coordination:** Produces model artifacts (frozen snapshots, validation reports, performance comparison results) consumed by Squad-Firmware (for TFLM integration) and Squad-Cloud (for SageMaker endpoint). Produces statistical validation documentation consumed by Squad-V&V for FDA AI/ML SaMD submission.

## Squad 4: Verification, Validation, and Integration (Squad-V&V)

**Purpose:** Own the cross-cutting concerns that no single sub-team can own alone: the end-to-end test infrastructure, the Design History File traceability matrix, the test result archival pipeline, the Sentinel-to-Atreus parity regression suite, the clinical dashboard test coverage, and the quarterly test health review process.

**Central challenge:** The most critical test -- the "5-minute alert" end-to-end path from arrhythmia detection to clinician notification -- crosses all four codebases and requires physical hardware (HIL bench, BLE sniffer, ECG signal generator). Automating this test requires coordination across all three other squads and a Python orchestration harness that sequences the signal generator, monitors BLE traffic, polls the cloud API, and verifies the dashboard alert. No single sub-team has the budget or mandate to build this alone. Squad-V&V owns the orchestration and the nightly execution, while the other squads own the individual components.

**Additional responsibilities:** Frontend/clinical dashboard testing (component tests, accessibility tests, E2E clinician workflow tests), Sentinel parity testing (cataloguing Sentinel behaviors, mapping to Atreus equivalents, building regression tests), and DHF assembly (traceability matrix generation from test metadata, coverage report aggregation, version-pinned build manifest production).

**Coordination:** Consumes test artifacts from all three other squads. Produces the integrated V&V report, the traceability matrix, and the 510(k) submission test package. Owns the relationship with Regulatory Affairs and Clinical Affairs.

---

## THE SQUADS:

- **Squad-Firmware** -- see [TDD Enterprise Medical Squad Formation Profile](../tdd-enterprise-medical-profile.md), Squad-Firmware section
- **Squad-Cloud** -- see [TDD Enterprise Medical Squad Formation Profile](../tdd-enterprise-medical-profile.md), Squad-Cloud section
- **Squad-AI/ML** -- see [TDD Enterprise Medical Squad Formation Profile](../tdd-enterprise-medical-profile.md), Squad-AI/ML section
- **Squad-V&V** -- see [TDD Enterprise Medical Squad Formation Profile](../tdd-enterprise-medical-profile.md), Squad-V&V section
