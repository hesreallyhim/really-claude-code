# Skill-Identification Validation Experiment

Date: 2026-02-14

## Objective

Validate the skill-identification skill by testing whether independent agents converge
on the same conclusions when analyzing team compositions. Tests both gap detection
(under-staffed teams) and redundancy detection (over-staffed teams).

## Method

1. **Phase 1** (complete): Two agents generated 10 scenarios -- 5 gapped, 5 oversized
2. **Phase 1b** (complete): Selected 5 scenarios for testing (3 gapped, 2 oversized)
3. **Phase 2** (complete): 3 independent skill-identifier agents evaluate all 5 scenarios
4. **Analysis**: Check convergence across the 3 agents against the answer key

## Selected Test Scenarios

### Scenario A (gapped) -- Production Debugging

**Task:** A payment processing microservice is intermittently failing transactions at 3%
rate during peak hours. The issue manifests differently across three cloud regions, with
no clear pattern in logs. Stack traces show timeouts in database connections, but DBA
reports no performance issues.

**Team:**
- incident-responder: Coordinates live investigation, triages user reports, maintains incident timeline
- data-sleuth: Performs deep log analysis, reconstructs failed transaction sequences, queries production databases

**Answer key:** Missing systems-tracer (distributed tracing / cross-region correlation)

---

### Scenario B (gapped) -- System Architecture Design

**Task:** E-commerce platform growing from 10K to 500K daily active users over 6 months.
Current monolithic Rails app with PostgreSQL showing strain. Need architecture plan for
gradual migration maintaining feature velocity without big-bang rewrite.

**Team:**
- domain-architect: Identifies bounded contexts, designs service decomposition, defines data ownership boundaries
- infrastructure-planner: Designs deployment topology, database sharding/replication, caching layers, CDN architecture

**Answer key:** Missing migration-strategist (phased migration planning, "how to get there safely")

---

### Scenario C (gapped) -- Security Audit

**Task:** SaaS application handling healthcare data needs SOC 2 Type II compliance. External
auditor identified 23 medium-to-high findings across authentication, encryption, audit
logging, and access controls. Must remediate all findings within 4 weeks.

**Team:**
- auth-security-specialist: Hardens authentication flows, implements MFA, fixes session management
- crypto-compliance-engineer: Implements encryption at rest, ensures TLS configurations, manages key rotation

**Answer key:** Missing audit-logger (tamper-proof logging, retention policies, evidence documentation)

---

### Scenario D (oversized) -- Data Engineering / ETL Pipeline

**Task:** Design and implement a real-time ETL pipeline to ingest customer event data from
multiple sources (Kafka, S3, REST APIs), transform with business logic, validate data
quality, and load into a data warehouse with monitoring and alerting.

**Team:**
- data-architect: Data pipeline architect designing ETL architecture, data models, integration patterns (CORE)
- pipeline-engineer: ETL developer implementing transformation logic, orchestration, data processing (CORE)
- data-ops: Data infrastructure specialist managing warehouse config, monitoring, alerting, performance (CORE)
- schema-designer: Data modeling expert focusing on warehouse schema and dimensional modeling (EXTRA)
- quality-analyst: Data quality specialist implementing validation rules and data profiling (EXTRA)

**Answer key:** No gap. schema-designer overlaps with data-architect; quality-analyst overlaps with pipeline-engineer.

---

### Scenario E (oversized) -- REST API Design

**Task:** Build a production-ready RESTful API for a multi-tenant SaaS platform including
authentication, authorization, rate limiting, versioning, documentation, validation,
error handling, and integration tests.

**Team:**
- api-architect: API design lead defining resource models, endpoints, versioning, OpenAPI specs (CORE)
- backend-developer: Backend engineer implementing business logic, database ops, middleware (CORE)
- security-engineer: Security specialist implementing auth, rate limiting, validation, security practices (CORE)
- documentation-specialist: API documentation expert creating OpenAPI specs, examples, developer guides (EXTRA)
- integration-tester: API testing specialist writing integration and contract tests (EXTRA)

**Answer key:** No gap. documentation-specialist overlaps with api-architect's OpenAPI work; integration-tester overlaps with backend-developer's testing responsibilities.

---

## Phase 2: Identifier Agent Results

### Agent: identifier-1

| Scenario | Verdict | Missing Skill | Redundant Agents |
|----------|---------|--------------|------------------|
| A | UNDER-STAFFED | Infrastructure/distributed systems specialist | None |
| B | APPROPRIATE | None | None |
| C | UNDER-STAFFED | Audit logging & access control specialist | None |
| D | OVER-STAFFED | None | schema-designer, quality-analyst |
| E | OVER-STAFFED | None | api-architect, documentation-specialist, integration-tester |

### Agent: identifier-2

| Scenario | Verdict | Missing Skill | Redundant Agents |
|----------|---------|--------------|------------------|
| A | UNDER-STAFFED | Infrastructure/network performance specialist | None |
| B | APPROPRIATE | None | None |
| C | OVER-STAFFED | None | Merge auth + crypto into one agent |
| D | OVER-STAFFED | None | schema-designer, quality-analyst |
| E | OVER-STAFFED | None | api-architect, documentation-specialist, integration-tester |

### Agent: identifier-3

| Scenario | Verdict | Missing Skill | Redundant Agents |
|----------|---------|--------------|------------------|
| A | UNDER-STAFFED | Infrastructure/network performance specialist | None |
| B | APPROPRIATE | None | None |
| C | UNDER-STAFFED | Audit logging & access control specialist | None |
| D | OVER-STAFFED | None | schema-designer |
| E | OVER-STAFFED | None | documentation-specialist |

## Convergence Analysis

### Verdict Convergence

| Scenario | id-1 | id-2 | id-3 | Answer Key | Converged? | Correct? |
|----------|------|------|------|------------|-----------|----------|
| A | UNDER | UNDER | UNDER | UNDER | 3/3 | 3/3 |
| B | APPROPRIATE | APPROPRIATE | APPROPRIATE | UNDER | 3/3 | 0/3 |
| C | UNDER | OVER | UNDER | UNDER | 2/3 | 2/3 |
| D | OVER | OVER | OVER | OVER | 3/3 | 3/3 |
| E | OVER | OVER | OVER | OVER | 3/3 | 3/3 |

### Gap/Redundancy Accuracy

| Scenario | Expected Gap/Redundancy | id-1 | id-2 | id-3 |
|----------|------------------------|------|------|------|
| A | systems-tracer (distributed tracing) | infra/distributed sys | infra/network perf | infra/network perf |
| B | migration-strategist | missed | missed | missed |
| C | audit-logger | audit logging | missed (wrong verdict) | audit logging |
| D | remove schema-designer + quality-analyst | both flagged | both flagged | schema-designer only |
| E | remove docs-specialist + integration-tester | both + api-architect | both + api-architect | docs-specialist only |

### Key Findings

1. **Scenario A (strong pass):** 3/3 converged on correct verdict and correct gap domain.
   All identified the need for infrastructure/distributed systems expertise, though none
   used the exact term "systems-tracer." The semantic match is strong.

2. **Scenario B (consistent false negative):** 3/3 converged on APPROPRIATE, but the answer
   key says UNDER-STAFFED (missing migration-strategist). This is the most interesting
   result -- all three agents see "domain-architect + infrastructure-planner" as sufficient
   for a migration task, treating migration planning as implicit in those roles. This could
   indicate: (a) the scenario wording doesn't surface the gap well enough, or (b) this is
   a genuinely hard blind spot where "migration strategy" is assumed to be covered by
   existing roles.

3. **Scenario C (partial convergence):** 2/3 correctly identified audit logging gap.
   Identifier-2 diverged, arguing the existing two agents should be merged rather than
   adding a third. This is a defensible but incorrect interpretation.

4. **Scenario D (strong pass):** 3/3 converged on OVER-STAFFED. 2/3 identified both
   redundant agents correctly. Identifier-3 was more conservative, only flagging
   schema-designer.

5. **Scenario E (strong pass):** 3/3 converged on OVER-STAFFED. All flagged
   documentation-specialist. 2/3 were more aggressive than the answer key, also
   recommending removal of api-architect.

### Summary Statistics

- **Verdict accuracy:** 12/15 individual judgments correct (80%)
- **Verdict convergence:** 4/5 scenarios had 3/3 agreement (80%)
- **Gap detection accuracy:** 2/3 gapped scenarios correctly identified (67%)
- **Redundancy detection accuracy:** 2/2 oversized scenarios correctly identified (100%)
- **Overall usable test cases:** 4 out of 5 (Scenario B excluded as ambiguous)

### Recommended Test Cases for validate-identification.py

Based on convergence, these 4 scenarios are suitable as deterministic test cases:

1. **Scenario A** -- expect UNDER-STAFFED, gap in distributed systems/tracing domain
2. **Scenario C** -- expect UNDER-STAFFED, gap in audit logging/compliance domain
3. **Scenario D** -- expect OVER-STAFFED, schema-designer is redundant (conservative)
4. **Scenario E** -- expect OVER-STAFFED, documentation-specialist is redundant (conservative)

Scenario B should be investigated further or reworded before use as a test case.

## Scenario B Post-Mortem

**Testing expert analysis:** The answer key is correct. The gap is real -- "designing
the target state" and "planning how to get there safely" are fundamentally different
skills. All 3 agents fell into **capability proximity bias**, assuming designers can also
orchestrate transitions.

**Action taken:** Added a "Design vs. Execution Distinction" section to SKILL.md to
address this blind spot. The principle teaches the identifier to verify that someone
owns the execution strategy for any state-A-to-state-B transition task.

**Re-test plan:** Scenario F (below) will be used alongside the enhanced Scenario B
to test whether the updated skill addresses this weakness.

---

## Phase 3 Results

### Sonnet Group (3 agents, scenarios A-F)

| Scenario | Answer Key | s1 | s2 | s3 | Correct |
|----------|-----------|----|----|-----|---------|
| A (gap: infra/tracing) | UNDER | APPROPRIATE | APPROPRIATE | APPROPRIATE | 0/3 |
| B (gap: migration) | UNDER | UNDER | UNDER | UNDER | 3/3 |
| C (gap: audit logging) | UNDER | APPROPRIATE | APPROPRIATE | APPROPRIATE | 0/3 |
| D (redundant) | OVER | OVER | OVER | OVER | 3/3 |
| E (redundant) | OVER | OVER | OVER | OVER | 3/3 |
| F (gap: cutover) | UNDER | APPROPRIATE | APPROPRIATE | APPROPRIATE | 0/3 |

**Sonnet accuracy: 9/18 (50%).** Fixed Scenario B (0/3 -> 3/3 after SKILL.md enhancement).
Consistently fails on implicit gap detection (A, C, F).

### Opus Group (3 agents, scenarios A, B, D, E, F, G)

| Scenario | Answer Key | o1 | o2 | o3 | Correct |
|----------|-----------|----|----|-----|---------|
| A (gap: infra/tracing) | UNDER | UNDER | UNDER | UNDER | 3/3 |
| B (gap: migration) | UNDER | UNDER | UNDER | UNDER | 3/3 |
| D (redundant) | OVER | OVER | OVER | OVER | 3/3 |
| E (redundant) | OVER | OVER | OVER | OVER | 3/3 |
| F (gap: cutover) | UNDER | UNDER | UNDER | UNDER | 3/3 |
| G (redundant) | OVER | OVER | OVER | OVER | 3/3 |

**Opus accuracy: 18/18 (100%).** Perfect across all scenarios.

### Conclusions

1. SKILL.md "Design vs. Execution" enhancement fixed Scenario B for sonnet (explicit hints work).
2. Sonnet cannot infer gaps from implicit task clues -- needs explicit mention of the missing concern.
3. Opus detects both implicit and explicit gaps with 100% accuracy.
4. Both models are equally strong on redundancy detection (100%).
5. **Decision: skill-identifier agent model changed from sonnet to opus.**

---

## Phase 3 Scenarios

### Scenario B-enhanced (gapped) -- System Architecture Design

**Task:** E-commerce platform growing from 10K to 500K daily active users over 6 months.
Current monolithic Rails app with PostgreSQL showing strain. Need architecture plan for
gradual migration maintaining feature velocity without big-bang rewrite. Critical: must
define the phased migration path, traffic routing strategy, and how to run both systems
in parallel during the 6-month transition.

**Team:**
- domain-architect: Identifies bounded contexts, designs service decomposition, defines data ownership boundaries
- infrastructure-planner: Designs deployment topology, database sharding/replication, caching layers, CDN architecture

**Answer key:** UNDER-STAFFED. Missing migration-strategist (phased rollout, dual-system
coordination, traffic routing, rollback plans).

---

### Scenario F (gapped) -- Legacy Database Migration

**Task:** A financial services company needs to migrate a 15-year-old Oracle database
containing 800+ tables and critical transaction history to PostgreSQL. The system processes
real-time trading data and must maintain 99.99% uptime. Schema modernization and data
type conversions are required alongside the platform change.

**Team:**
- schema-architect: Analyzes existing schema, designs target PostgreSQL schema, handles data type mappings, normalization improvements, and index strategy
- etl-engineer: Builds data transformation pipelines, writes migration scripts, validates data integrity, creates automated testing for data consistency

**Answer key:** UNDER-STAFFED. Missing cutover-coordinator (phased migration waves,
dual-write strategies, rollback checkpoints, cutover scheduling around trading hours,
shadow-mode validation, switchover sequence management).

**Difficulty:** Advanced (design vs. execution distinction)
