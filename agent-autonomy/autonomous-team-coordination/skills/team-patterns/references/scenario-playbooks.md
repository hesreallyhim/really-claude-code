# Scenario-Specific Team Playbooks

Extracted from the comprehensive team patterns catalog. Each playbook provides a complete team design recommendation for a specific software engineering scenario.

---

## 4.1 Production Incident Debugging

**Best pattern:** Incident Command System + Tiger Team hybrid

**Team structure:**
- Incident Commander (coordinator, non-technical role during the incident)
- Communications Lead (shields technical team, manages stakeholders)
- 2-4 Technical Responders (SREs, domain experts for the affected system)
- Scribe (records timeline)

**Communication topology:** Hub-and-spoke (IC is hub). Dedicated Slack channel + conference call. Decisions in the call, records in Slack.

**Why this works:** Clear roles prevent chaos. The IC ensures parallel investigation doesn't devolve into confusion. The comms lead prevents "tap on the shoulder" interruptions. The scribe creates an artifact for post-incident review.

**AI agent mapping:** Orchestrator agent (IC) dispatches specialist agents: log-analyzer, metrics-checker, dependency-tracer, recent-deployment-reviewer. A comms agent produces human-readable status updates. A scribe agent maintains an immutable timeline. The orchestrator synthesizes findings and proposes remediation steps.

---

## 4.2 Greenfield Application Design

**Best pattern:** Small cross-functional squad + ARB review

**Team structure:**
- 1 Tech Lead / Architect (navigator role)
- 2-4 Senior Engineers (implementers covering different domains: frontend, backend, data)
- 1 Product Owner (requirements and priorities)
- Optional: UX designer, security engineer

**Communication topology:** Mesh (all members communicate freely). ARB provides hub-and-spoke oversight at key milestones.

**Why this works:** Greenfield needs rapid iteration and creative exploration. A small mesh team can explore design space efficiently. ARB check-ins prevent architectural drift without slowing daily work. High dependency between developers in initial sprints is expected and manageable in a small team.

**AI agent mapping:** A planning agent generates architectural proposals. Multiple specialist agents evaluate proposals from different perspectives (scalability, security, cost, developer experience). A synthesis agent converges on a design. Periodic "review board" evaluation by a panel of critic agents.

---

## 4.3 Legacy Codebase Refactoring

**Best pattern:** Strangler Fig + Embedded enabling team

**Team structure:**
- 1-2 Legacy Experts (deep knowledge of existing system)
- 2-3 Refactoring Engineers (implement new components)
- 1 QA/Test Engineer (builds safety net of tests)
- 1 Product Owner (prioritizes based on business impact)

**Communication topology:** Pipeline + mesh. Pipeline for the migration flow (identify -> test -> refactor -> validate -> deploy). Mesh for daily collaboration.

**Why this works:** The Strangler Fig pattern allows incremental replacement, maintaining production stability. Starting with tests as a safety net is essential ("50% of time is spent understanding the code first"). Hotspot analysis (combining complexity + change frequency) identifies highest-ROI refactoring targets. Feature flags enable instant rollback.

**Key principles:**
- Never refactor without automated tests
- Keep refactoring and debugging separate
- Prioritize "hotspots" (high complexity + frequent changes)
- Use progressive delivery (feature flags, canary deployments)

**AI agent mapping:** A code-analysis agent maps the legacy codebase (dependencies, hotspots, complexity). A test-generation agent creates the safety net. A refactoring agent implements changes incrementally. A validation agent runs tests and checks for regressions. A routing agent (strangler fig facade) manages traffic between old and new implementations.

---

## 4.4 Security Audit / Penetration Testing

**Best pattern:** Red Team / Blue Team / Purple Team

**Team structure:**
- **Red Team (Offense, 3-5):** Ethical hackers, social engineers, penetration testers. Simulate adversary TTPs. Led by senior security consultant. Follow MITRE ATT&CK framework.
- **Blue Team (Defense, 4-8):** SOC analysts, security engineers. Monitor, detect, respond. Use SIEM, IDS/IPS, endpoint protection. Ideally unaware that a red team exercise is occurring (for realistic testing).
- **Purple Team (Bridge, 2-3):** Facilitates collaboration between red and blue. Ensures lessons learned are captured. Makes the exercise productive rather than adversarial.

**Communication topology:** Adversarial (red vs. blue) with purple team bridging. Red team operates covertly; blue team operates defensively. Purple team facilitates post-exercise knowledge sharing.

**Why this works:** Adversarial testing reveals vulnerabilities that internal review misses. Blue team's defensive capabilities are stress-tested under realistic conditions. Purple team ensures findings translate into actual security improvements rather than just a report.

**AI agent mapping:** Maps directly to the debate/adversarial AI pattern. Red-team agents attempt to find vulnerabilities (prompt injection, data exfiltration, privilege escalation). Blue-team agents detect and block attacks. A verifier agent (purple team) evaluates whether defenses held and whether attacks were realistic. Critical: research shows that when adversarial agents collude, a verifier agent is essential to block false consensus.

---

## 4.5 Performance Optimization

**Best pattern:** Tiger Team (short-term) or Enabling Team (ongoing)

**Team structure:**
- 1 Performance Engineer (specializes in profiling, benchmarking)
- 1-2 Domain Engineers (know the system's architecture and hotspots)
- 1 Infrastructure/SRE Engineer (knows the deployment environment, hardware, network)
- 1 Data Analyst (identifies patterns in metrics and logs)

**Communication topology:** Mesh (small, tight-knit team). Hub-and-spoke when reporting findings to broader engineering organization.

**Why this works:** Performance optimization requires deep specialization combined with system-wide thinking. The team must establish baselines, profile under realistic workloads, and iterate (profile -> optimize -> measure -> repeat). "Don't just scale -- optimize": many performance issues are architectural, not infrastructural.

**Key approach:**
1. Establish baselines (response time, CPU, memory, DB performance)
2. Profile under realistic workloads using APM tools
3. Identify hotspots through code profiling and continuous profiling
4. Conduct load and stress testing
5. Analyze logs and distributed traces
6. Iterate: profile before AND after each change

**AI agent mapping:** A profiling agent instruments the code and collects metrics. An analysis agent identifies bottlenecks from profiling data. A recommendation agent proposes optimizations. A benchmark agent validates improvements. A regression agent ensures optimizations don't break existing behavior.

---

## 4.6 API Design

**Best pattern:** Design-First embedded team + lightweight ARB review

**Team structure:**
- 1-2 API Designers (may be senior backend engineers)
- 1 Product Manager (consumer needs, use cases)
- 1-2 Consumer-side Representatives (frontend engineers, external partner developers)
- 1 Technical Writer (documentation from day one)
- Optional: Security reviewer

**Communication topology:** Collaborative mesh during design phase. X-as-a-service (API team serves consumers) after stabilization.

**Why this works:** The Design-First approach treats APIs as "first-class citizens." The API contract (OpenAPI document) is agreed upon before implementation, allowing producer and consumer teams to work in parallel. Consistency ("naming conventions, paging, auth mechanisms standard across the board") is what distinguishes a platform from a random collection of endpoints.

**Key principles:**
- Establish design review team early, including non-technical stakeholders
- Embed governance into workflows (CI linting, PR checks), not separate review gates
- Create and maintain an API catalog for discoverability
- Avoid the "approval bottleneck" anti-pattern

**AI agent mapping:** A design agent generates API specifications. Consumer-simulation agents test the API from different client perspectives. A consistency agent checks naming conventions, error formats, and pagination patterns against the organization's API style guide. A documentation agent generates API docs from the spec. A versioning agent manages backward compatibility.

---

## 4.7 Data Pipeline Construction

**Best pattern:** Cross-functional DataOps team with enabling team support

**Team structure:**
- 2-3 Data Engineers (pipeline construction, ETL/ELT, orchestration)
- 1 Data Architect (schema design, overall data flow architecture)
- 1 Data Analyst / Domain Expert (validates business logic, data quality)
- 1 Platform/DevOps Engineer (CI/CD, infrastructure, monitoring)
- Optional: Data Scientist (if pipeline feeds ML models)

**Communication topology:** Mesh internally. Pipeline (the data itself flows through stages). X-as-a-service to downstream consumers.

**Why this works:** Data pipelines require deep collaboration between those who understand the data (analysts, domain experts) and those who build infrastructure (engineers, architects). The DataOps philosophy emphasizes treating data as a product, with CI/CD, automated testing, and orchestration as first-class concerns. The team must balance foundational work (infrastructure, quality) with insight generation (serving business needs).

**Key approach:**
- Choose orchestration tool (Dagster, Airflow, etc.) early
- Implement CI/CD for pipeline code
- Automate data quality validation
- Use ELT in cloud-native environments (cloud warehouses handle transformations at scale)
- Monitor with observability tools

**AI agent mapping:** A schema-design agent creates and validates data models. An extraction agent handles source system integration. A transformation agent applies business logic. A quality agent validates data against rules. An orchestration agent manages scheduling and dependencies. A monitoring agent watches for pipeline failures and data drift.

---

## 4.8 Test Suite Creation from Scratch

**Best pattern:** Integrated quality ownership (no separate QA silo) following the Testing Pyramid

**Team structure:**
- All developers write tests (unit tests as part of TDD)
- 1 QA Lead / Test Architect (defines strategy, pyramid shape, tooling)
- 1-2 Test Automation Engineers (build E2E framework, CI integration)
- 1 Product Owner (defines critical user journeys for E2E tests)

**Communication topology:** Mesh. Quality is a shared responsibility, not a hand-off to a separate team. QA participates in design and grooming sessions.

**Why this works:** The testing pyramid provides a strategic framework: lots of fast unit tests (base), some integration tests (middle), few E2E tests (top). Starting with unit tests via TDD naturally builds a strong foundation. E2E tests are added only when a basic prototype exists, covering critical user journeys. Integrating tests into CI/CD creates a fast feedback pipeline (unit: every commit, integration: every merge, E2E: nightly/pre-release).

**Key principles:**
- Start with TDD for unit tests (naturally builds coverage)
- Add integration tests for component interaction
- Add E2E tests strategically for critical user journeys only
- Integrate into CI/CD with appropriate cadence per level
- Track metrics: coverage, pass/fail rates, execution time, flaky test rates

**AI agent mapping:** A test-planning agent analyzes the codebase and proposes a testing strategy. A unit-test agent generates tests for individual functions/methods. An integration-test agent generates tests for component interactions. A coverage-analysis agent identifies gaps. A flaky-test-detection agent monitors test reliability over time.

---

## 4.9 Documentation Overhaul

**Best pattern:** Docs-as-Code with embedded technical writers

**Team structure:**
- 1-2 Technical Writers (embedded in product teams, not siloed)
- 1 Information Architect (defines structure using Diataxis framework: tutorials, how-to guides, reference, explanation)
- All developers contribute (docs live alongside code)
- 1 Engineering Lead (reviews technical accuracy)
- 1 Product Manager (validates user perspective)

**Communication topology:** Mesh (everyone contributes to docs). Pipeline for the review process (write -> review -> merge -> deploy). Facilitating interaction from writers to developers.

**Why this works:** Docs-as-Code treats documentation with the same rigor as code: version control, pull requests, CI/CD, linting, and automated deployment. Embedding writers in product teams (rather than a separate department) ensures accuracy and shared ownership. The Diataxis framework provides a proven information architecture that helps users find answers fast and helps writers know where new content belongs.

**Key principles:**
- Use the same tools as developers (Git, Markdown, static site generators)
- Implement style guides and automated linting
- Use PR-based review process for all doc changes
- Automate validation and deployment via CI/CD
- Plan for the "documentation debt" phase (engineering grows faster than docs team)

**AI agent mapping:** A content-analysis agent audits existing documentation for gaps, staleness, and inconsistencies. A generation agent drafts documentation from code comments, API specs, and test cases. A style-enforcement agent checks against the style guide. A structure agent organizes content according to the Diataxis framework. A review agent checks technical accuracy against the actual codebase.

---

## 4.10 Code Migration (Language or Framework)

**Best pattern:** Strangler Fig with dedicated migration squad

**Team structure:**
- 1 Migration Architect (defines strategy, manages routing layer, sets boundaries)
- 2-3 Migration Engineers (implement new components in target language/framework)
- 1-2 Legacy Engineers (deep knowledge of source system, ensure behavioral parity)
- 1 QA Engineer (builds and maintains comparison/validation tests)
- 1 DevOps/Platform Engineer (manages dual infrastructure, feature flags, traffic routing)

**Communication topology:** Pipeline (identify module -> build new -> test parity -> route traffic -> retire old). Hub-and-spoke with the migration architect as hub for strategic decisions.

**Why this works:** The Strangler Fig pattern reduces risk by migrating incrementally. A routing/facade layer sits in front of both systems, directing traffic based on feature flags. Both old and new systems run in parallel during migration. Each migrated module delivers value immediately rather than waiting for complete migration. Feature flags enable instant rollback.

**Key principles:**
- Never attempt a "big bang" rewrite
- Place a routing layer in front of the legacy system
- Migrate one module at a time, prioritized by business value and coupling
- Run old and new in parallel with comparison testing
- Ensure clear team ownership (who owns old vs. new vs. routing layer)
- Plan for extended dual-maintenance period

**Anti-patterns to avoid:**
- Migrating everything at once under a "modernization" banner
- Ignoring operational complexity during the transition
- Getting service boundaries wrong (premature decomposition)
- Allowing migration to stall indefinitely (leaving two partial systems)

**AI agent mapping:** A code-analysis agent maps the source system's module boundaries and dependencies. A translation agent converts code from source to target language/framework. A behavioral-parity agent generates tests that verify identical behavior. A routing agent manages traffic distribution between old and new systems. A progress-tracking agent monitors migration completion and identifies stalled modules.
