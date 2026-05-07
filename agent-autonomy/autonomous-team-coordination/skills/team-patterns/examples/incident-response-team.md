# Example Team Design: Production Incident Response

A complete team design for a production API returning 500 errors after a deployment. This example demonstrates the full output format expected from the team-architect agent.

---

## TEAM DESIGN: API-Outage Response Squad

### Situation Analysis

```
SITUATION ANALYSIS
==================
Task: Diagnose and resolve HTTP 500 errors on the payments API after v2.4.1 deployment
Domain: Backend services, payment processing
Urgency: Critical (production down, revenue impact)
Complexity: Complex-decomposable (multiple possible root causes, but investigation tracks are independent)
Knowledge needs: Distributed (requires log analysis, metrics, deployment history, code review)
Risk tolerance: Zero (payment system, data integrity concerns)
Scale: Single service + 3 downstream dependencies
Duration: One-shot (resolve incident, then disband)
```

### Pattern Selection

**Primary pattern:** Incident Command System (Pattern 1)
**Secondary pattern:** Fan-Out/Fan-In (Pattern 8) for parallel investigation

**Justification:** Critical urgency with zero risk tolerance maps directly to Incident Command per the decision matrix. The IC pattern provides the clear chain of command needed during production outages. Fan-Out/Fan-In is layered on top because the investigation tracks (logs, metrics, deployment diff, dependency check) are independent and can run in parallel, reducing time-to-resolution.

**Communication topology:** Hub-and-spoke (IC as hub) with fan-out for investigation.

### Topology Diagram

```
                    +------------------+
                    | INCIDENT         |
                    | COMMANDER (IC)   |
                    | [project-manager]|
                    +--------+---------+
                             |
           +---------+-------+-------+---------+
           |         |               |         |
     +-----+----+ +--+------+ +-----+----+ +--+-------+
     |LOG       | |METRICS  | |DEPLOY    | |DEPENDENCY|
     |ANALYZER  | |CHECKER  | |REVIEWER  | |TRACER    |
     |[IC-sonnet]| |[IC-sonnet]| |[IC-opus]| |[IC-sonnet]|
     +----------+ +---------+ +----------+ +----------+
```

### Agents

#### Role 1: Incident Commander
- **Type:** existing -- `project-manager`
- **Responsibilities:** Coordinates investigation. Receives findings from all responders. Decides remediation strategy. Does NOT investigate directly. Manages task creation and prioritization.
- **Skills needed:** team-patterns (existing)
- **Model:** opus (complex coordination, high-stakes decisions)
- **Communicates with:** All agents (hub). Sends directives, receives findings.

#### Role 2: Log Analyzer
- **Type:** existing -- `independent-contributor` (sonnet variant)
- **Responsibilities:** Searches application logs for error patterns, stack traces, and anomalies around the deployment timestamp. Reports findings to IC.
- **Skills needed:** None beyond base capabilities
- **Model:** sonnet (pattern matching in logs, high throughput)
- **Communicates with:** IC only

#### Role 3: Metrics Checker
- **Type:** existing -- `independent-contributor` (sonnet variant)
- **Responsibilities:** Examines monitoring dashboards, error rates, latency percentiles, CPU/memory around deployment. Identifies when errors started and their correlation with system metrics.
- **Skills needed:** None beyond base capabilities
- **Model:** sonnet (data analysis, pattern recognition)
- **Communicates with:** IC only

#### Role 4: Deployment Reviewer
- **Type:** existing -- `independent-contributor` (opus variant)
- **Responsibilities:** Reviews the v2.4.1 deployment diff, identifies risky changes (database migrations, API contract changes, dependency upgrades). Assesses rollback safety.
- **Skills needed:** None beyond base capabilities
- **Model:** opus (code review of potentially complex changes requires deep reasoning)
- **Communicates with:** IC only

#### Role 5: Dependency Tracer (optional, spawn if needed)
- **Type:** existing -- `independent-contributor` (sonnet variant)
- **Responsibilities:** Checks health of downstream dependencies (database, message queue, third-party payment gateway). Rules out external causes.
- **Skills needed:** None beyond base capabilities
- **Model:** sonnet (API health checks, straightforward investigation)
- **Communicates with:** IC only

### Task Dependency Graph

```
  Task 1: Create incident channel + brief team  -->  Owner: IC
       |
       +---> Task 2: Search logs for 500 errors  -->  Owner: Log Analyzer (parallel)
       +---> Task 3: Check metrics around deploy  -->  Owner: Metrics Checker (parallel)
       +---> Task 4: Review v2.4.1 diff           -->  Owner: Deploy Reviewer (parallel)
       +---> Task 5: Check dependency health       -->  Owner: Dependency Tracer (parallel)
       |
  Task 6: Synthesize findings, decide remediation -->  Owner: IC (blocked by: 2,3,4,5)
       |
  Task 7: Execute fix or rollback                 -->  Owner: Deploy Reviewer (blocked by: 6)
       |
  Task 8: Verify resolution, close incident       -->  Owner: IC (blocked by: 7)
```

### Agent Count Justification

**Total agents: 4 (5 if dependency tracer is spawned)**

Communication channels: 4(4-1)/2 = 6 in full mesh, but hub-and-spoke reduces effective channels to 4 (one per spoke). Well within the optimal range of 4-8 agents (Harvard: 4.6 optimal).

The IC pattern intentionally keeps the team small. Each investigator has a clear, non-overlapping scope. Adding more agents would increase coordination overhead without proportional benefit (Brooks's Law). The dependency tracer is optional and only spawned if initial investigation suggests an external cause.

### Capability Gap Assessment

**No gaps.** All roles can be filled by existing agents:
- `project-manager` as IC
- `independent-contributor` (sonnet) for investigation roles
- `independent-contributor` (opus) for code review

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| IC bottleneck (all info flows through one agent) | IC focuses solely on coordination, never investigates directly. Clear task structure reduces back-and-forth. |
| Investigation scope creep | IC sets time-box for each investigation track (e.g., 10 minutes). If no findings, escalate. |
| Rollback not safe (data migration in v2.4.1) | Deploy Reviewer explicitly assesses rollback safety as part of Task 4. IC does not approve rollback without this assessment. |
| False positive resolution | Task 8 includes verification: monitor error rates for 15 minutes after fix before closing incident. |

### Execution Readiness

**READY.** All agents and skills exist. Can execute immediately with `TeamCreate` and task spawning.
