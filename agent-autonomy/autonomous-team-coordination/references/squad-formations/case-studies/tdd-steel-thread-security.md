---
Name: "TDD Squad Pre-Spec Planning Doc: Veridian (Steel Thread / Security / One Month)"
Goal: Formulate the factors that will guide the development of the Squad Formation Profile for a TDD team building a zero-trust service mesh authentication broker as a steel thread.
Source scenario: tdd-scenarios.md, Scenario 2 (Veridian)
Date: 2026-02-14
---

# TDD -- Veridian: Zero-Trust Service Mesh Authentication Broker

## Given:

- A specification with clear AC and functional and non-functional requirements for a Kubernetes operator that mediates mTLS certificate issuance and rotation between microservices, backed by HashiCorp Vault PKI.
- A classification of the project as: **Steel Thread**
- A domain area: **Security-related**
  - Certificate lifecycle management (issuance, rotation, expiry)
  - mTLS enforcement between microservices
  - SOC 2 Type II audit trail requirements (CC6.1, CC6.3)
  - Zero-trust identity model scoped to individual service identities
  - Cryptographic correctness as a non-negotiable property
- A rough timeline: **One month**
- Context: **Greenfield** -- new Kubernetes operator, new CRD (`ServiceIdentity`), new Vault PKI integration. Replaces namespace-level Istio RBAC defaults.

## The squads must:

1. **Implement the golden-path certificate lifecycle as a fully test-driven state machine.** The steel-thread scope is exactly one flow: service registration -> certificate issuance -> mTLS handshake -> certificate rotation without downtime. Every state transition in this flow must have a failing test written before the production code. No test may be written for behavior outside the golden path (revocation, multi-cluster federation, non-Kubernetes workloads) -- this is a discipline requirement, not a gap.

2. **Produce a layered test suite that satisfies three audiences simultaneously.** The tests must (a) give the development team fast inner-loop feedback via `go test` unit tests with fake Vault clients and fake clocks; (b) give the platform team integration confidence via `envtest` tests against a fake Kubernetes API server with real etcd semantics; and (c) give the CISO and the Fortune 500 customer's security reviewers a demonstrable end-to-end proof that the golden path works in the staging EKS cluster.

3. **Resolve the fake-clock vs. real-time-wait tradeoff for certificate rotation testing and document the decision.** The zero-downtime rotation behavior is a time-dependent state machine. The squads must choose between a fake clock (fast, deterministic, but does not exercise real timer behavior) and real-time waits (realistic but slow and potentially flaky), implement the chosen approach, and produce a written rationale that can be referenced by future engineers expanding the test suite.

4. **Produce a "scope fence" document as a first-class deliverable.** This document enumerates every behavior that is explicitly NOT tested in the steel thread, with a rationale for each exclusion and a forward reference to when each excluded behavior should be addressed. The scope fence is the team's contract with themselves, the CISO, and the customer's security reviewers. It must be committed to the repository and reviewed as critically as any code artifact.

5. **Produce SOC 2-aligned audit log test coverage for the golden path.** Because Stratum holds an active SOC 2 Type II certification, every certificate lifecycle event (registration, issuance, rotation, expiry) must emit audit log entries that map to CC6.1 (logical access controls) and CC6.3 (role-based access). The test suite must verify that these log entries are produced with the correct structure and content. This is not optional scope creep -- it is a compliance obligation that applies even to a steel thread.

6. **Maintain strict scope discipline under psychological pressure.** Security-minded engineers will feel compelled to test error paths (expired certs, revoked certs, clock skew, race conditions). The squads must resist this urge and channel it into the scope fence document. Every out-of-scope behavior that someone wants to test gets documented, not implemented. The one-month timeline does not permit both golden-path rigor and error-path breadth.

## IN ORDER TO DO THAT, THE SQUADS MUST HAVE:

### Skills

| Skill | Why |
|-------|-----|
| Go 1.22+ | The operator and all tests are written in Go. Table-driven tests, subtests, test helpers, and `go test` conventions are foundational. |
| controller-runtime / Kubebuilder | The operator is built with controller-runtime. Reconciler patterns, CRD code generation, and `envtest` integration are required. |
| HashiCorp Vault PKI secrets engine | Certificate issuance and rotation are mediated by Vault. The Go client library (`hashicorp/vault/api`) and PKI mount configuration must be understood. |
| `envtest` (controller-runtime test framework) | Integration tests run against a fake API server with real etcd. Setting up `envtest`, installing CRDs, and managing test lifecycle are required. |
| Kubernetes CRD design | The `ServiceIdentity` CRD is the operator's primary interface. Schema design, status subresource patterns, and controller watches must be correct. |
| mTLS / X.509 certificate mechanics | The golden path involves certificate issuance, SAN matching, and TLS handshake verification. Misunderstanding certificate semantics leads to false-positive tests. |
| Go test mocking patterns | Fake Vault clients, fake clocks, and interface-based dependency injection are required to isolate the state machine for unit testing. |

### Knowledge

| Knowledge | Why |
|-----------|-----|
| SOC 2 CC6.1 and CC6.3 controls | Audit log structure must map to these specific controls. Without understanding what the auditor expects, the team cannot write correct log assertions. |
| Zero-trust architecture principles | The broker replaces namespace-level Istio defaults with per-service identity. The team must understand why this matters to write meaningful test assertions (e.g., asserting that a cert SAN contains the specific service identity, not a namespace wildcard). |
| Certificate lifecycle state machines | Registration -> issuance -> active -> approaching-expiry -> rotation -> old-cert-drain -> old-cert-delete. The team must model this explicitly to write tests against it. |
| Steel-thread methodology | The team must understand that a steel thread proves a single end-to-end path and is not a partial implementation of the full system. This shapes every scoping decision. |

### Tooling

| Tool | Why |
|------|-----|
| `go test` + table-driven test patterns | The primary test runner. The existing team already uses this convention. |
| `envtest` (sigs.k8s.io/controller-runtime/pkg/envtest) | Required for integration tests against the fake API server. |
| Staging EKS cluster (AWS EKS 1.29) | The end-to-end test deploys two test pods and verifies the mTLS handshake in a real Kubernetes environment. |
| HashiCorp Vault 1.15 (staging instance) | The end-to-end test must interact with a real Vault PKI secrets engine, not a mock. |
| GitHub Actions CI | The existing nightly integration suite runs on GitHub Actions. Unit and envtest tests must integrate into this pipeline. |
| Helm | The operator is deployed via Helm charts. Test pod deployment for the E2E test also uses Helm. |

### Organizational Needs

| Need | Why |
|------|-----|
| Access to Vault staging instance with PKI secrets engine configured | The end-to-end test and some integration tests require a real Vault endpoint. DevOps must provision and configure the PKI mount before the E2E test can be written. |
| CISO alignment on scope fence boundaries | The scope fence document is the team's contract with leadership. The CISO must agree that the excluded behaviors (revocation, multi-cluster, non-K8s) are acceptable exclusions for the steel thread, before the team commits to the one-month timeline. |
| Dedicated staging EKS namespace | The E2E test deploys test pods. This must not interfere with other staging workloads. A dedicated namespace with RBAC isolation is required. |
| Agreement on the fake-clock decision | The team lead, the platform team, and ideally the CISO must agree on the tradeoff between fake-clock and real-time-wait testing for certificate rotation. This decision affects test reliability and execution speed permanently. |

# THE TEAM WILL CONSIST OF:

Two squads organized around the natural divergence between **building the operator and its test suite** (golden-path TDD implementation) and **building the testing infrastructure, scope documentation, and compliance artifacts** (testing scaffolding and scope governance).

### Squad-Implement: Golden-Path TDD

This squad owns the core development loop: write a failing test, write the minimal production code to pass it, refactor, repeat. Their scope is the `ServiceIdentity` CRD, the Kubernetes operator reconciler, the Vault PKI client integration, and the certificate lifecycle state machine. They produce unit tests (fake Vault, fake clock), `envtest` integration tests, and the production Go code. They are explicitly forbidden from writing tests for out-of-scope behaviors -- when they identify an edge case that falls outside the golden path, they file it in a shared backlog that Squad-Scaffold converts into scope-fence entries.

**Topology:** Hub-and-spoke. The squad leader assigns TDD cycles (one failing test at a time) and reviews each green-to-refactor transition. Workers implement in parallel only when working on independent state transitions (e.g., one worker on issuance, another on rotation).

### Squad-Scaffold: Test Infrastructure and Scope Governance

This squad owns everything that enables and constrains the TDD process. They set up the `envtest` harness, configure the staging Vault PKI mount, write the E2E test framework (test pod deployment, TLS handshake verification), author the scope fence document, and implement the SOC 2 audit log assertions. They are the team's scope police: when Squad-Implement surfaces an out-of-scope edge case, Squad-Scaffold documents it in the scope fence with a rationale and a forward plan. They also own the fake-clock implementation (or the real-time-wait harness, depending on the team's decision) as a shared test utility.

**Topology:** Mesh. The work is varied (infrastructure setup, documentation, compliance, E2E framework) and requires frequent coordination between workers. No single worker is blocked on another for extended periods, but they need to share context about decisions (e.g., the fake-clock choice affects both the test utility and the scope fence rationale).

## THE SQUADS:

- **Squad-Implement (Golden-Path TDD):** See [tdd-steel-thread-security-profile.md](../tdd-steel-thread-security-profile.md), Squad-Implement
- **Squad-Scaffold (Test Infrastructure and Scope Governance):** See [tdd-steel-thread-security-profile.md](../tdd-steel-thread-security-profile.md), Squad-Scaffold
