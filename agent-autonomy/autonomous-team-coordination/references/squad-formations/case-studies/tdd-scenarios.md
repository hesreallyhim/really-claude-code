---
name: TDD Squad Scenario Profiles
description: >
  Five richly detailed project scenarios for TDD squad formation planning,
  generated using the scenario-architect skill. Each scenario occupies a
  distinct region of the maturity x domain x timeline parameter space and
  captures the realistic tensions that make test-driven development non-trivial.
generated_with: scenario-architect
coverage:
  maturity_levels: [Prototype, Steel Thread, MVP, V1, Enterprise in high-regulation]
  domain_areas: [Consumer tech, Network reliance, Embedded systems, Security-related]
  timelines: [One week, One month, One quarter, One year]
  contexts: [greenfield, greenfield, greenfield, legacy migration, legacy migration]
date: 2026-02-14
---

# TDD Project Scenario Profiles

Five scenarios designed for systematic coverage of the TDD parametric space defined in the [TDD Pre-Spec Planning Doc](tdd.md). Each scenario is constructed using the scenario-architect skill's core principles:

- **Specificity over generality** -- every scenario names real technologies, real regulations, and plausible organizational structures.
- **Realism through tension** -- every scenario contains at least one central conflict that makes TDD adoption non-obvious.
- **Coverage through systematic variation** -- the five scenarios collectively span 5 maturity levels, all 4 domain areas, 4 timelines, and a mix of greenfield and legacy contexts.
- **Intersection method** -- several scenarios sit at the intersection of two unusual conditions (e.g., high-regulation + embedded systems, or prototype + security).

---

## Coverage Matrix

| # | Project | Maturity | Domain | Timeline | Context |
|---|---------|----------|--------|----------|---------|
| 1 | Frostbite | Prototype | Consumer tech | One week | Greenfield |
| 2 | Veridian | Steel Thread | Security-related | One month | Greenfield |
| 3 | Tideline | MVP | Network reliance | One quarter | Greenfield |
| 4 | Oxbow | V1 | Embedded systems | One quarter | Legacy migration |
| 5 | Atreus | Enterprise in high-regulation | Embedded systems + Security-related | One year | Legacy migration |

---

## Scenario 1: Frostbite -- On-Device AR Try-On for a Streetwear Drop

### Project Description

Frostbite is a throwaway augmented-reality prototype that lets users point their phone camera at their feet and see how a limited-edition sneaker collab looks on them before it drops. The prototype only needs to support one shoe model (the "Glacier IV"), one camera angle (top-down foot shot), and two skin-tone-adaptive lighting presets. It will be shown at a private buyer preview event in seven days and discarded immediately afterward. The output is a mobile web page served from a single static host -- no backend, no accounts, no persistence.

### Parameter Classification

| Axis | Value |
|------|-------|
| **Maturity** | Prototype |
| **Domain** | Consumer tech |
| **Timeline** | One week |

### Organizational Context

**Company:** VSSL Collective, a 14-person streetwear brand based in Los Angeles that contracts all its tech work to a two-person creative-technology studio called Liminal Labs. Liminal's principals are a creative technologist (strong on Three.js, WebXR, and shaders) and a product designer (strong on UI, weak on engineering). Neither has formal testing experience. VSSL's creative director saw a competitor demo real-time AR try-on at a trade show and demanded "something like that but cooler" for the upcoming Glacier IV preview event on February 21. Budget: a flat $8,000 project fee. There is no staging environment, no CI, and no existing test infrastructure.

**Why now:** The Glacier IV drop is a make-or-break moment for VSSL's DTC pivot. If the buyer preview generates social media buzz, VSSL secures a distribution deal with a major retailer. If the AR prototype crashes on-camera in front of buyers, it damages the brand's reputation for craftsmanship.

### Regulatory / Compliance Factors

None directly applicable. However, VSSL's creative director has verbally mandated that the AR overlay "must not look weird on dark skin," which is an implicit fairness and inclusivity constraint without a formal compliance framework behind it. This creates a testing obligation that has no associated process or acceptance criteria.

### Technical Environment and Constraints

- **Platform:** Mobile Safari and Chrome on iOS 16+ and Android 13+. No app store deployment -- served as a PWA from a Cloudflare Pages static site.
- **AR framework:** WebXR Device API with fallback to `getUserMedia` + MediaPipe hand/foot landmark detection.
- **3D assets:** A single glTF model of the Glacier IV provided by VSSL's 3D artist, delivered as a 12MB file that needs to be optimized down to < 3MB for mobile.
- **Languages:** TypeScript, GLSL shaders, HTML/CSS.
- **Infrastructure:** GitHub repo, no CI pipeline, manual deployment via `wrangler pages deploy`.
- **Devices available for testing:** One iPhone 15 Pro, one Pixel 7, and the Chrome DevTools device emulator.

### Central Tension

**TDD feels like an unaffordable luxury for a seven-day throwaway prototype, but the project's highest risk -- AR rendering that looks wrong on diverse skin tones -- is exactly the kind of problem that benefits from automated regression testing.** The creative technologist's instinct is to "just eyeball it" in real-time on the two test devices, but the skin-tone-adaptive lighting involves shader math that is easy to break when tweaking parameters. Without tests, every change to the lighting model requires manually re-checking both devices under multiple lighting conditions. With tests, a snapshot-based visual regression suite could catch regressions in seconds. But building that suite takes time the team does not believe it has.

A secondary tension: the foot-detection model has non-deterministic inference timing. Testing anything that depends on ML model output requires either mocking the model (which defeats the purpose of testing the pipeline) or accepting flaky tests (which undermines trust in the suite). The team has no experience with either approach.

### What "Success" Looks Like for TDD

At the **Prototype** maturity level, TDD success is minimal and targeted:

1. **A single test file** containing 3-5 unit tests for the skin-tone-adaptive lighting shader math, verifying that the two lighting presets produce expected RGB output ranges for input skin-tone samples spanning the Fitzpatrick scale. These tests run in Node.js using the shader math extracted into a pure TypeScript function (not the actual GLSL).
2. **One visual snapshot test** that renders the Glacier IV model under each lighting preset against a reference image, with a perceptual diff threshold, run via Playwright against a headless Chromium instance.
3. **Zero infrastructure overhead** -- tests run via `npx vitest` with no CI pipeline. The creative technologist runs them manually before deploying.

Success is NOT a comprehensive test suite. Success is that the two highest-risk behaviors (lighting correctness across skin tones, visual regression of the AR overlay) have any automated verification at all, and that the team experiences the feedback loop of "change shader param, run test, see it catch a regression" at least once during the week.

---

## Scenario 2: Veridian -- Zero-Trust Service Mesh Authentication Broker

### Project Description

Veridian is a steel-thread implementation of a service mesh authentication broker that mediates mTLS certificate issuance and rotation between microservices in a Kubernetes cluster. The steel thread must prove that a single "golden path" works end-to-end: a new service registers with the broker, receives a short-lived client certificate signed by an intermediate CA, uses that certificate to authenticate to one other service, and the certificate is rotated before expiry without downtime. The broker is implemented as a Kubernetes operator with a custom CRD (`ServiceIdentity`), backed by a HashiCorp Vault PKI secrets engine for certificate generation. The steel thread does not need to handle revocation, multi-cluster federation, or non-Kubernetes workloads.

### Parameter Classification

| Axis | Value |
|------|-------|
| **Maturity** | Steel Thread |
| **Domain** | Security-related |
| **Timeline** | One month |

### Organizational Context

**Company:** Stratum Systems, a 120-person B2B SaaS company (Series C, $40M raised) that sells a supply-chain visibility platform to mid-market manufacturers. Stratum's platform runs on AWS EKS across two regions. The platform team (8 engineers) has been using Istio's built-in mTLS for service-to-service auth, but the CISO mandated a move to an in-house identity broker after an incident where a compromised pod was able to impersonate another service due to overly broad Istio RBAC policies. The platform team lead pushed for a steel-thread approach after a previous attempt to build the full broker in one quarter failed -- the team got lost in the complexity of revocation lists and multi-cluster federation and delivered nothing.

**Why now:** Stratum's largest customer (a Fortune 500 manufacturer) is conducting a vendor security review in 60 days. The CISO needs to demonstrate that service-to-service authentication is cryptographically scoped to individual service identities, not namespace-level Istio defaults. The steel thread must be running in a staging cluster and demo-able before the review.

### Regulatory / Compliance Factors

- **SOC 2 Type II:** Stratum holds an active SOC 2 certification. The auditor (a Big 4 firm) has specifically flagged "service-to-service authentication granularity" as an area of concern in the last review cycle. Any new authentication mechanism must produce audit logs that map to SOC 2 CC6.1 (logical access controls) and CC6.3 (role-based access).
- **Customer contractual SLA:** The Fortune 500 customer's MSA requires 99.95% uptime for API endpoints. Certificate rotation must be zero-downtime, and a bug in the rotation logic could cause cascading authentication failures across the mesh.

### Technical Environment and Constraints

- **Platform:** AWS EKS 1.29, Kubernetes 1.29, Linux (Amazon Linux 2023 nodes).
- **Language:** Go 1.22 for the operator; Helm charts for deployment; Rego for OPA-based admission policies.
- **Certificate infrastructure:** HashiCorp Vault 1.15 (self-hosted on EKS), PKI secrets engine, AppRole auth.
- **Existing test infrastructure:** The platform team uses `go test` with table-driven tests, `envtest` (controller-runtime's test framework) for operator testing against a fake API server, and a nightly integration suite that runs against a dedicated EKS staging cluster via GitHub Actions.
- **Constraints:** The operator must be written in Go using controller-runtime (not Metacontroller or shell-operator) per team convention. Vault interactions must go through the official Go client library, not HTTP calls.

### Central Tension

**The security domain demands exhaustive edge-case coverage (expired certs, revoked certs, clock skew, race conditions during rotation), but the steel-thread mandate demands ruthless scope limitation.** The team must write tests that prove the golden path works while actively resisting the urge to test error paths that are explicitly out of scope. This is psychologically difficult for security-minded engineers: every untested error path feels like a vulnerability left open. The team lead must enforce a "test what we're building, not what we wish we were building" discipline.

A deeper technical tension: the most critical behavior -- zero-downtime certificate rotation -- involves a time-dependent state machine (cert issued -> cert approaching expiry -> new cert issued -> old cert drained -> old cert deleted). Testing this in `envtest` requires either a fake clock (which means the test doesn't exercise real timer behavior) or real-time waits (which makes the test suite unacceptably slow). The team must decide which compromise to accept and document why.

### What "Success" Looks Like for TDD

At the **Steel Thread** maturity level, TDD success means the golden path is fully tested at every layer, but only the golden path:

1. **Unit tests** for the core certificate lifecycle state machine: registration, issuance, rotation trigger, rotation execution, old-cert cleanup. These use a fake Vault client and a fake clock, testing the state transitions in isolation. Target: 100% branch coverage of the state machine, 0% coverage of error/revocation paths (explicitly out of scope).
2. **`envtest` integration tests** for the Kubernetes operator: a `ServiceIdentity` CR is created, the operator reconciles it, a Secret containing the client cert appears in the correct namespace, and the cert's Subject Alternative Name matches the service identity. These tests run against a fake API server with a real (but in-memory) etcd.
3. **One end-to-end test** in the staging cluster: two test pods are deployed, one configured as a client and one as a server. The client authenticates to the server using the broker-issued cert. The test verifies the TLS handshake succeeds and the server extracts the correct service identity from the client cert.
4. **A "scope fence" document** checked into the repo listing the behaviors that are explicitly NOT tested in this steel thread (revocation, multi-cluster, non-K8s workloads) with a rationale for each exclusion. This document is the team's contract with themselves and with the CISO.

Success is NOT a comprehensive security test suite. Success is that the single golden path is tested with enough rigor that the team can demo it to the Fortune 500 customer's security reviewers and say, with confidence: "This specific flow is proven correct. Here is the test evidence. Here is the explicit list of what is not yet covered and our plan to cover it."

---

## Scenario 3: Tideline -- Offline-First Field Data Collection for Marine Biologists

### Project Description

Tideline is an MVP mobile application for marine biology field researchers who collect specimen observation data (species identification, GPS coordinates, water temperature, salinity, photographs, and free-text notes) while working on boats, intertidal zones, and remote coastlines where cellular connectivity is absent for hours or days at a time. The app must function fully offline, sync data to a cloud backend when connectivity is restored, and handle sync conflicts gracefully when multiple researchers collect overlapping observations. The MVP targets iOS and Android via React Native, with a Supabase backend (PostgreSQL + real-time subscriptions + storage buckets for photos). The MVP must support 10-20 concurrent researchers across 3 active research expeditions.

### Parameter Classification

| Axis | Value |
|------|-------|
| **Maturity** | MVP |
| **Domain** | Network reliance |
| **Timeline** | One quarter |

### Organizational Context

**Company:** The Pelagic Data Cooperative (PDC), a nonprofit research consortium funded by a three-year NSF grant (Award #2345678). PDC has no in-house engineering staff. The app is being built by a 4-person contract development team from a civic-tech consultancy called Meridian Digital. The team consists of a tech lead (strong React Native, weak on testing), two mid-level React Native developers, and a part-time backend developer who also supports two other Meridian clients. PDC's principal investigator, Dr. Rina Kamali, is the product owner and has written a detailed specification based on two decades of field experience and acute frustration with the existing workflow (paper data sheets, manual GPS logging, Excel spreadsheets emailed between researchers, and frequent data loss).

**Why now:** The NSF grant's Year 2 deliverable requires a "functional data collection prototype deployed to at least two field teams" by September 2026. PDC's previous attempt to build this tool (a Django web app by a single freelancer in 2024) failed because it assumed constant connectivity and was unusable in the field. Dr. Kamali specifically required offline-first architecture in the new RFP and selected Meridian partly because they claimed experience with offline sync. (In reality, Meridian has built one offline-capable app before, using a different stack.)

### Regulatory / Compliance Factors

- **NSF Data Management Plan (DMP):** The grant requires all collected data to be deposited in a FAIR-compliant public repository (BCO-DMO) within 12 months of collection. This means data integrity is not just a UX concern -- corrupted or lost observations represent a compliance failure that could jeopardize future funding.
- **Endangered Species Act (ESA) Section 7:** Some observations may involve ESA-listed species. GPS coordinates of endangered species sightings must not be publicly exposed at fine resolution (must be degraded to 10km grid cells in public datasets). The app must track which observations contain ESA-sensitive data, and the sync pipeline must enforce coordinate degradation before public export.
- **Institutional Review Board (IRB):** Not applicable (non-human subjects research), but PDC's institutional policy requires that field data be attributable to the collecting researcher for provenance tracking.

### Technical Environment and Constraints

- **Frontend:** React Native 0.74 with Expo, targeting iOS 17+ and Android 14+. Offline storage via WatermelonDB (SQLite-backed, with sync primitives).
- **Backend:** Supabase (hosted) -- PostgreSQL 15, Supabase Auth, Supabase Storage for photos, Supabase Realtime for sync notifications.
- **Sync architecture:** WatermelonDB's push/pull sync protocol against a custom Supabase Edge Function that handles conflict resolution. Conflict strategy: last-write-wins for scalar fields, append-only for photographs and notes.
- **Devices:** Researchers use a mix of personal iPhones (mostly iPhone 12-15), one lab-owned iPad Air, and two Samsung Galaxy A54s purchased for the project. Devices may be exposed to salt spray, direct sunlight, and wet hands.
- **Connectivity profile:** Zero connectivity for 4-8 hours during boat transits. Intermittent 3G/LTE at coastal research stations. Reliable WiFi only at the shore-based lab. Sync windows are unpredictable and sometimes brief (5-10 minutes at a waypoint).
- **Testing infrastructure:** Meridian uses Jest + React Native Testing Library for unit/component tests, Detox for E2E tests on iOS/Android simulators, and a staging Supabase project. No device farm -- E2E tests run on simulators only.

### Central Tension

**The offline-sync behavior that makes this app valuable is also the behavior that is hardest to test deterministically.** Sync conflicts depend on the order and timing of operations across multiple devices and a remote database, which means the most important tests are inherently non-deterministic unless the sync layer is heavily mocked -- but heavily mocking the sync layer means the tests don't actually verify the behavior that matters most.

Specifically: WatermelonDB's sync protocol is a black box with documented but complex semantics. The team can test their conflict resolution Edge Function in isolation (given these two versions of a record, which one wins?), but they cannot easily test the full round-trip (device A writes offline, device B writes offline, both sync, conflict is resolved correctly on both devices) without either (a) running two simulators simultaneously against a shared Supabase instance, which Detox does not natively support, or (b) building a custom integration test harness that simulates the sync protocol at the HTTP level.

A secondary tension: Dr. Kamali's specification is extremely detailed about the data model and field workflows but says nothing about sync behavior, because she has never used an offline-first app. The team must write acceptance tests for behavior the product owner does not know how to specify.

### What "Success" Looks Like for TDD

At the **MVP** maturity level, TDD success means the core user flows are covered and the highest-risk behavior (offline sync) has explicit test coverage, even if that coverage requires architectural compromises:

1. **Unit tests for the data model and validation layer:** Every observation field has validation rules (GPS coordinates within valid range, salinity within plausible bounds, species ID from a controlled vocabulary). These are pure functions, trivially testable. Target: 100% coverage of validation logic.
2. **Unit tests for the conflict resolution Edge Function:** Given two conflicting versions of a record, the function returns the correct winner. Tested with a matrix of conflict scenarios (same field modified, different fields modified, one side deleted, photo added on both sides). Target: all identified conflict scenarios covered.
3. **Component tests for the offline data entry forms:** Using React Native Testing Library, verify that forms render correctly, validate input, and persist to WatermelonDB. These tests use WatermelonDB's in-memory adapter (no SQLite on disk).
4. **A custom sync integration test harness** that simulates two "devices" as separate WatermelonDB instances syncing against the same Supabase staging project. This harness does NOT use Detox or simulators -- it runs in Node.js, instantiating WatermelonDB with the LokiJS adapter and calling the sync Edge Function over HTTP. It tests the five critical sync scenarios: clean merge, scalar conflict, photo conflict, delete-vs-update conflict, and sync after 8 hours of offline accumulation (500+ records).
5. **One Detox E2E test** for the primary happy path: launch app, create observation, fill all fields, save, verify observation appears in the list. This test runs on a single iOS simulator and does not test sync.

Success is that the team can release the MVP to Dr. Kamali's field teams with confidence that (a) data entered offline will not be lost, (b) sync conflicts will be resolved according to a documented, tested policy, and (c) new features can be added during Year 3 without breaking the sync pipeline, because the sync integration harness serves as a regression safety net.

---

## Scenario 4: Oxbow -- Firmware Migration for Legacy Industrial Flow Meters

### Project Description

Oxbow is a firmware migration project for the Meridian FM-400, an electromagnetic flow meter used in municipal water treatment plants and chemical processing facilities. The FM-400 has been in production since 2011 and runs a bare-metal C firmware (approximately 35,000 lines of C89) on a Renesas RX631 microcontroller. The firmware has never had automated tests -- it was developed by a single engineer who retired in 2022 and has been maintained since then via "change it and pray" by two junior firmware engineers who inherited the codebase. The project's goal is to migrate the FM-400 firmware to a new hardware platform (Renesas RX671, with 2x RAM and a hardware floating-point unit) while simultaneously introducing a test harness that allows the existing signal-processing algorithms to be validated on the host machine before being cross-compiled for the target. The migration must maintain bit-for-bit measurement accuracy with the existing FM-400 -- any deviation in flow calculation output for the same sensor input is a certification failure.

### Parameter Classification

| Axis | Value |
|------|-------|
| **Maturity** | V1 |
| **Domain** | Embedded systems |
| **Timeline** | One quarter |

### Organizational Context

**Company:** Meridian Instrumentation, a 200-person industrial instrumentation manufacturer headquartered in Baton Rouge, Louisiana. Meridian sells flow meters, level sensors, and pressure transmitters to water utilities, chemical plants, and oil refineries across North America. The FM-400 is Meridian's best-selling product (approximately 8,000 units in the field). The firmware team is 5 people total: a firmware architect (15 years at Meridian, did not write the original FM-400 code but has maintained other products), two mid-level firmware engineers (the ones who inherited the FM-400), one test engineer (focused on hardware-in-the-loop testing, no software test automation experience), and a new hire fresh from an embedded systems master's program who has used Unity (the C test framework, not the game engine) and Ceedling in academic projects.

**Why now:** The Renesas RX631 is approaching end-of-life. Renesas has guaranteed availability through 2028 but has signaled that the RX631 will not receive new silicon revisions. The RX671 is the recommended migration path. Simultaneously, Meridian's VP of Engineering has mandated that all firmware for new products and major revisions must have automated test coverage, after a costly field recall in 2025 caused by a firmware bug in a different product line (a pressure transmitter that reported negative gauge pressure under specific temperature conditions -- a bug that would have been trivially caught by a unit test).

### Regulatory / Compliance Factors

- **OIML R 49 (International Organization of Legal Metrology):** The FM-400 is a custody-transfer-grade flow meter. Its measurement accuracy is certified under OIML R 49, which requires that the meter's maximum permissible error (MPE) not exceed +/- 0.5% of the actual flow rate in the normal operating range. The migrated firmware must pass the same type-approval tests as the original. If the firmware produces different numerical outputs for the same sensor inputs, the OIML certification is invalid, and every FM-400 unit on the new hardware must be individually re-calibrated -- a cost of approximately $400 per unit.
- **IEC 61508 (Functional Safety):** The FM-400 is not SIL-rated itself, but several customers integrate it into SIL-2 safety instrumented systems. Meridian's documentation must demonstrate that the firmware migration did not alter the meter's safety-relevant behavior. The firmware architect has interpreted this as requiring traceability from requirements to test cases.
- **NIST Handbook 44:** For US water utility customers, the FM-400 must comply with NIST HB 44 specifications for water meters, which overlap with but are not identical to OIML R 49.

### Technical Environment and Constraints

- **Target hardware:** Renesas RX671 (RXv3 core, 240 MHz, 1 MB flash, 384 KB RAM, hardware FPU).
- **Outgoing hardware:** Renesas RX631 (RXv2 core, 100 MHz, 512 KB flash, 128 KB RAM, no hardware FPU -- all floating-point is software-emulated).
- **Language:** C89 (the existing codebase), with a plan to adopt C11 for new modules on the RX671. The test harness runs on the host (x86-64 Linux) using Unity (ThrowTheSwitch.org) and CMock.
- **Build system:** A legacy Makefile that invokes the Renesas CC-RX compiler. The team is migrating to CMake with a cross-compilation toolchain file for CC-RX and a native toolchain for host-based tests.
- **Critical constraint -- floating-point semantics:** The RX631 uses software floating-point emulation; the RX671 has a hardware FPU (IEEE 754 compliant). The signal-processing algorithms use `float` extensively. Bit-for-bit identical output is not guaranteed when moving from software to hardware FPU due to differences in intermediate rounding. The team must characterize these differences and either (a) force the RX671 to use software FP for the measurement pipeline (sacrificing performance), or (b) demonstrate that the differences are within the OIML MPE tolerance and update the certification documentation.
- **Existing test infrastructure:** Hardware-in-the-loop (HIL) test bench with a reference flow rig, controlled by a LabVIEW automation script. No host-based automated tests. The HIL bench can run a full calibration sweep in approximately 4 hours.

### Central Tension

**The most valuable thing TDD could do -- verify bit-for-bit numerical equivalence of the signal processing pipeline on the new hardware -- is precisely the thing TDD cannot guarantee, because the floating-point semantics have changed.** Host-based unit tests run on x86-64 with IEEE 754 double-precision intermediate values, but the target runs on an RX671 with single-precision hardware FPU that may round intermediates differently. A test that passes on the host does not prove the firmware will produce identical output on the target.

This creates a layered testing problem:
- **Layer 1 (host-based unit tests):** Can verify algorithmic correctness in isolation but cannot verify numerical identity with the target hardware.
- **Layer 2 (target-based tests via debugger/JTAG):** Can verify numerical output on the actual hardware but are slow and require the HIL bench.
- **Layer 3 (HIL integration tests):** Can verify end-to-end measurement accuracy but take 4 hours per sweep and cannot be run by individual developers.

The team must decide how to distribute test effort across these layers and accept that no single layer provides complete confidence. This is a TDD maturity challenge: the new hire wants to write pure unit tests; the firmware architect wants HIL tests; the test engineer wants to automate the HIL bench. The correct answer involves all three, but the team has never coordinated a multi-layer test strategy before.

### What "Success" Looks Like for TDD

At the **V1** maturity level, TDD success means a structured, multi-layer test strategy that provides measurable confidence in the migration's correctness:

1. **Host-based unit tests (Unity/CMock) for all signal-processing functions:** The team extracts the 12 core signal-processing functions from the monolithic firmware into a hardware-abstraction-layer (HAL)-independent library. Each function gets table-driven tests with sensor input vectors captured from the HIL bench. Tests verify output within a defined epsilon (not bit-exact), where epsilon is derived from the OIML MPE tolerance. Target: all 12 functions covered, with at least 50 input vectors per function spanning the full operating range.
2. **A "golden reference" test:** The existing RX631 firmware runs the 50-vector suite on the actual RX631 hardware via JTAG, capturing outputs to a CSV file. The RX671 firmware runs the same suite on the RX671 hardware. A comparison script verifies that every output pair is within the OIML MPE tolerance. This test runs on the HIL bench and is automated via a Python script that replaces the LabVIEW manual process.
3. **Build system integration:** `cmake --build . --target test` runs the host-based Unity tests in under 30 seconds. CI (GitHub Actions with a self-hosted runner) runs them on every push. The golden-reference test runs nightly on the HIL bench and posts results to a shared dashboard.
4. **Traceability matrix:** A markdown document mapping each OIML R 49 clause to one or more test cases, satisfying the IEC 61508 traceability requirement. This document is generated from test metadata (Unity test names include requirement IDs).
5. **Developer workflow change:** Developers write a failing host-based test before modifying any signal-processing function. The test is reviewed in the PR alongside the code change. This is the team's first experience with TDD as a workflow, not just as a testing technique.

Success is that the firmware migration passes OIML type-approval testing on the first attempt, that the automated test suite catches at least one floating-point discrepancy during development (proving its value), and that the team adopts the host-based-test-first workflow as a permanent practice for future firmware development.

---

## Scenario 5: Atreus -- Implantable Cardiac Monitor Firmware and Cloud Telemetry Platform

### Project Description

Atreus is the development of a next-generation implantable cardiac monitor (ICM) and its companion cloud telemetry platform. The ICM is a subcutaneous device the size of a USB flash drive, implanted in the chest wall, that continuously records single-lead electrocardiogram (ECG) data and transmits detected arrhythmia events to a cloud platform via a bedside relay unit using Bluetooth Low Energy (BLE). The cloud platform receives event transmissions, runs a secondary AI-based arrhythmia classification model, alerts the patient's cardiologist via the clinical dashboard, and archives all data for regulatory-mandated retention. Atreus is a full-platform development effort: new device firmware (ARM Cortex-M33, written in C and Rust), new BLE communication protocol, new cloud ingestion pipeline (AWS), new classification model (TensorFlow Lite for Microcontrollers on-device, PyTorch cloud-side), and new clinical dashboard (React). The project replaces an existing legacy ICM platform (the "Sentinel" system) that has been on the market for 8 years and uses a proprietary radio protocol, an on-premise server, and no AI classification.

### Parameter Classification

| Axis | Value |
|------|-------|
| **Maturity** | Enterprise in high-regulation |
| **Domain** | Embedded systems + Security-related (intersection) |
| **Timeline** | One year |

### Organizational Context

**Company:** Cardiax Medical, a 600-person medical device company headquartered in Minneapolis, Minnesota, with manufacturing in Galway, Ireland. Cardiax's annual revenue is approximately $180M, primarily from the Sentinel ICM and associated monitoring services. The company has a strong clinical reputation but is perceived as technologically behind competitors (Abbott, Medtronic, Boston Scientific) who have already shipped AI-enabled ICMs with cloud platforms. Cardiax's board authorized the Atreus program 18 months ago with a $12M budget and a hard deadline: FDA 510(k) submission by February 2027.

**Team:** The Atreus program has 28 engineers organized into four sub-teams: Firmware (8 engineers, including 2 who are new to Rust), Cloud/Backend (7 engineers), AI/ML (4 engineers + 2 clinical data scientists), and Frontend/Clinical Dashboard (5 engineers). There is also a dedicated Quality Assurance team (4 people) that owns the verification and validation (V&V) process, a Regulatory Affairs specialist, and a Clinical Affairs manager who coordinates with cardiologists serving as clinical advisors. The VP of Engineering, who joined from a big-tech background 2 years ago, has mandated TDD across all sub-teams. The firmware team has a strong testing culture (inherited from the Sentinel codebase, which has 60% line coverage with CppUTest). The cloud team has moderate coverage with pytest. The AI/ML team has never written automated tests -- they validate models via Jupyter notebooks and manual evaluation on held-out datasets. The frontend team uses React Testing Library but coverage is patchy.

**Why now:** Abbott's Confirm Rx and Medtronic's LINQ II have captured significant market share with AI-enabled monitoring and cloud-based clinician workflows. Cardiax's Sentinel platform requires clinicians to review every transmitted event manually, which is unsustainable as the installed base grows. Three major health system customers have indicated they will not renew Sentinel monitoring contracts if Cardiax does not ship a cloud-connected, AI-assisted platform by 2027. The legacy Sentinel on-premise server runs Windows Server 2012 R2 and is approaching end of extended support.

### Regulatory / Compliance Factors

This scenario sits at the intersection of the most demanding regulatory environments:

- **FDA 21 CFR Part 820 (Quality System Regulation):** Requires a documented design history file (DHF) with design inputs, design outputs, verification, validation, and design reviews. Software must follow IEC 62304 (see below). All test results must be traceable to design requirements and archived as part of the DHF.
- **IEC 62304 (Medical Device Software Lifecycle):** The ICM firmware is classified as Class C software (could contribute to a hazardous situation resulting in death or serious injury). Class C requires unit testing of every software unit, integration testing, and system testing, with documented coverage analysis. The cloud platform is Class B (could contribute to non-serious injury -- a delayed arrhythmia alert). Class B requires integration testing and system testing but allows risk-based reduction of unit testing scope.
- **IEC 60601-1-2 (Electromagnetic Compatibility):** Not directly a software concern, but the BLE communication protocol must be tested for robustness under EMC conditions, which affects the firmware test strategy (the protocol must handle corrupted packets gracefully).
- **HIPAA (Health Insurance Portability and Accountability Act):** All patient ECG data in the cloud platform is protected health information (PHI). The cloud architecture must implement technical safeguards (encryption at rest and in transit, access controls, audit logging). Security testing is a HIPAA obligation, not just a best practice.
- **GDPR (General Data Protection Regulation):** Cardiax sells in the EU. The cloud platform must support data subject access requests (DSARs), right to erasure (with exceptions for medical device data retention requirements under MDR), and data portability. GDPR and the EU MDR (Medical Device Regulation) create a tension: GDPR says patients can request data deletion, but MDR Article 10(8) requires manufacturers to retain post-market surveillance data for at least 10 years after the last device is placed on the market.
- **EU MDR 2017/745 (Medical Device Regulation):** Requires clinical evaluation, post-market surveillance, and a Unique Device Identification (UDI) system. The AI classification model is regulated as a Software as a Medical Device (SaMD) under MDCG 2019-11, requiring a separate clinical evaluation and potentially a clinical investigation if the predicate device comparison is insufficient.
- **FDA AI/ML SaMD guidance (2021 action plan):** The FDA expects a "predetermined change control plan" for AI/ML-based SaMD, documenting how the model will be updated post-market and what testing will be performed for each update. This means the test infrastructure for the AI model must be designed for ongoing use, not just pre-submission validation.

### Technical Environment and Constraints

- **Device firmware:** ARM Cortex-M33 (Nordic nRF5340 SoC), dual-core (application core + network core). Application core firmware in Rust (using Embassy async runtime) for the ECG signal processing pipeline and event detection. Network core firmware in C (Nordic's nRF Connect SDK / Zephyr RTOS) for BLE communication. Total firmware size target: < 256 KB flash, < 64 KB RAM. Battery life target: 3 years on a 120 mAh battery.
- **On-device ML:** TensorFlow Lite for Microcontrollers (TFLM), running a quantized 8-bit integer CNN for arrhythmia detection on the application core. Model size: < 30 KB. Inference time budget: < 50ms per heartbeat classification.
- **BLE protocol:** Custom GATT profile over BLE 5.3 with coded PHY for range. Events are transmitted as compressed protobuf messages. The bedside relay unit is a dedicated Raspberry Pi 4 running a Python BLE client.
- **Cloud platform:** AWS -- API Gateway, Lambda, Kinesis Data Streams for ingestion, S3 for raw ECG storage, DynamoDB for event metadata, SageMaker for cloud-side model inference, Cognito for clinician auth, CloudWatch for monitoring. Infrastructure as code via AWS CDK (TypeScript).
- **Clinical dashboard:** React 18 with Next.js, hosted on AWS Amplify. Clinician-facing; must support WCAG 2.1 AA accessibility.
- **Test infrastructure (current):**
  - Firmware: CppUTest for the C BLE stack, `cargo test` for Rust application core, QEMU-based emulation for integration tests (nRF5340 support is incomplete in QEMU -- GPIO and BLE peripherals must be mocked).
  - Cloud: pytest + moto (AWS service mocking) for Lambda unit tests, Localstack for integration tests, k6 for load testing.
  - Frontend: Jest + React Testing Library for component tests, Playwright for E2E tests against a staging environment.
  - AI/ML: No automated tests. Model evaluation is done via notebooks comparing predictions to cardiologist-annotated ECG databases (MIT-BIH, PhysioNet).
  - Hardware-in-the-loop: A custom test bench with an nRF5340 development kit, a BLE sniffer, and an ECG signal generator (a DAC replaying recorded ECG waveforms). Currently operated manually by the QA team.
- **Constraints:**
  - The BLE relay unit (Raspberry Pi) runs in patients' homes and cannot be reliably updated. The BLE protocol must be forward-compatible.
  - The on-device ML model cannot be updated without a firmware update, which requires an in-clinic visit. Model updates are expected no more than once per year.
  - All test results that contribute to the DHF must be reproducible and archived with the exact tool versions, compiler versions, and test framework versions used.

### Central Tension

**TDD is not optional -- IEC 62304 Class C mandates it -- but the definition of "unit" and the meaning of "test" vary so dramatically across the four sub-teams that a single TDD process cannot be applied uniformly.** The firmware team's "unit" is a C function or a Rust module. The cloud team's "unit" is a Lambda function. The AI/ML team's "unit" is... what? A single neuron? A layer? The whole model? The AI/ML team's notion of "testing" is statistical (precision/recall on a test dataset), not deterministic (given this input, expect this output). Forcing the AI/ML team into deterministic unit tests is either meaningless (testing that the model returns a float) or requires freezing the model weights and testing specific input/output pairs, which doesn't validate the model's generalization ability.

The regulatory framework intensifies this tension: IEC 62304 was written for deterministic software. Its requirement for "unit testing of every software unit" does not map cleanly onto ML model validation. The regulatory affairs specialist has advised that the FDA will accept a "software validation plan" that includes statistical performance testing (sensitivity/specificity on a curated dataset) in lieu of traditional unit tests for the ML components, but this plan must be documented and defended in the 510(k) submission. The VP of Engineering's blanket "TDD across all sub-teams" mandate must be reconciled with this regulatory reality.

A second tension spans the firmware-cloud boundary: the most critical end-to-end behavior (a detected arrhythmia on the device triggers an alert on the clinician's dashboard within 5 minutes of the relay unit connecting to the internet) crosses four codebases, three programming languages, two hardware platforms, and a network boundary. No single team owns this test. The QA team nominally owns end-to-end testing but has no automated infrastructure for it -- they currently perform this test manually by replaying an ECG waveform, waiting for the device to detect it, watching the relay unit transmit, and checking the dashboard. Automating this requires coordination across all four sub-teams and a significant investment in test infrastructure that no single sub-team has the budget or mandate to build alone.

### What "Success" Looks Like for TDD

At the **Enterprise in high-regulation** maturity level, TDD success is defined by the regulatory framework and measured by the ability to submit a credible 510(k) with a complete design history file:

1. **Firmware (Class C -- full unit test coverage required):**
   - Every Rust module in the ECG signal processing pipeline has property-based tests (using `proptest`) that verify signal processing invariants (e.g., filter output is bounded, heartbeat detection never reports a rate outside 20-300 BPM).
   - Every C function in the BLE stack has CppUTest unit tests with table-driven input vectors.
   - The TFLM inference wrapper has deterministic tests with frozen model weights and known input/output pairs, plus a performance test verifying inference completes within the 50ms budget on the actual nRF5340 hardware (via the HIL bench).
   - Integration tests run on QEMU with mocked BLE peripherals, verifying the full firmware pipeline from ECG input to BLE event transmission.
   - Target: IEC 62304 Class C unit coverage requirements met; coverage report generated automatically and archived with each build.

2. **Cloud platform (Class B -- integration testing required, risk-based unit testing):**
   - All Lambda functions have pytest unit tests with moto-mocked AWS services.
   - The ingestion pipeline (Kinesis -> Lambda -> DynamoDB + S3) has integration tests running against Localstack.
   - HIPAA security controls have dedicated tests: encryption at rest (S3 bucket policy test), encryption in transit (TLS enforcement test), access control (Cognito role-based access test), audit logging (CloudTrail event test).
   - A DSAR (Data Subject Access Request) workflow test verifies that a patient data export request produces a complete, correct export and that a deletion request removes all non-MDR-retained data.
   - Target: integration test coverage of all data paths; unit test coverage of business logic; security tests for all HIPAA technical safeguards.

3. **AI/ML model (SaMD -- statistical validation, not unit tests):**
   - A frozen "golden" model snapshot has deterministic input/output tests (20 curated ECG segments with known classifications). These tests verify that the model artifact has not been corrupted or inadvertently retrained, not that the model generalizes well.
   - A statistical validation suite runs the model against the MIT-BIH Arrhythmia Database and a proprietary Cardiax-annotated dataset, reporting sensitivity, specificity, positive predictive value, and F1 score per arrhythmia class. The suite has hard-fail thresholds: sensitivity for ventricular fibrillation must be >= 99.0%, and overall accuracy must be >= 95.0%.
   - The predetermined change control plan test suite: when a new model version is trained, the full statistical validation suite runs automatically (via SageMaker Pipelines), and the results are compared against the predicate model's performance. Regression on any metric beyond a defined threshold blocks deployment.
   - Target: a documented, automated, reproducible model validation process that satisfies FDA AI/ML SaMD guidance and produces artifacts suitable for inclusion in the 510(k) submission.

4. **Clinical dashboard (not classified, but patient-facing):**
   - Component tests for all clinician-facing views (event list, ECG strip viewer, alert queue).
   - Accessibility tests (axe-core) for WCAG 2.1 AA compliance on all pages.
   - E2E tests (Playwright) for the three critical clinician workflows: review alert, view ECG strip, dismiss or escalate event.
   - Target: sufficient coverage to prevent clinician-facing regressions; no regulatory mandate for specific coverage levels, but the VP of Engineering has set a 70% line coverage floor.

5. **End-to-end (cross-team):**
   - One fully automated end-to-end test: ECG signal generator replays a known arrhythmia waveform -> nRF5340 dev kit detects arrhythmia -> BLE transmission to relay unit -> cloud ingestion -> AI classification -> clinician dashboard alert. This test runs on the HIL bench nightly, orchestrated by a Python script that coordinates the signal generator, monitors BLE traffic, and polls the cloud API.
   - Target: the "5-minute alert" SLA is verified automatically every night, and any regression triggers a PagerDuty alert to the QA team.

6. **Process and documentation:**
   - Every test case ID traces to a design requirement ID in the DHF requirements matrix.
   - Test results are archived as CI artifacts (firmware: GitHub Actions; cloud: GitHub Actions; AI/ML: SageMaker Pipelines) with exact tool and compiler version metadata.
   - A quarterly "test health" review compares coverage trends, flaky test rates, and test execution times across all four sub-teams, presented to the VP of Engineering.

Success is NOT that every line of code has a test. Success is that the 510(k) submission package contains a complete, defensible verification and validation report where every design requirement traces to at least one automated test result, the AI/ML model has a documented and reproducible validation process that the FDA reviewer can follow, and the end-to-end patient safety path (arrhythmia detected -> clinician alerted) is verified automatically every day.
