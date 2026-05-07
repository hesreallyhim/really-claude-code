# Example Team Design: Greenfield Full-Stack Application

A complete team design for building a new SaaS application from scratch. Demonstrates the Squad + ARB pattern composition with mesh topology.

---

## TEAM DESIGN: Greenfield SaaS Build Squad

### Situation Analysis

```
SITUATION ANALYSIS
==================
Task: Design and build a new project management SaaS with real-time collaboration features
Domain: Full-stack web development (React frontend, Node.js backend, PostgreSQL, WebSockets)
Urgency: Normal (planned work, 3-month timeline)
Complexity: Complex-decomposable (frontend, backend, data layer, real-time are separable)
Knowledge needs: Distributed (frontend, backend, database, real-time/WebSocket expertise needed)
Risk tolerance: Moderate (new product, can iterate; but architecture decisions are hard to reverse)
Scale: ~15 modules across 4 layers
Duration: Multi-phase (architecture -> MVP -> iteration)
```

### Pattern Selection

**Primary pattern:** Cross-functional Squad (see Scenario 4.2)
**Secondary pattern:** Architecture Review Board (Pattern 3) at key milestones
**Overlay:** Reflection/Self-Critique (Pattern 12) on all architectural decisions

**Justification:** Normal urgency with distributed knowledge maps to Cross-functional Squad per the decision matrix. Moderate risk tolerance with complex-decomposable architecture calls for periodic ARB checkpoints to prevent architectural drift without slowing daily work. Reflection loops catch design issues early.

**Communication topology:** Mesh (squad members communicate freely) + periodic Star (ARB reviews at milestones).

### Topology Diagram

```
  Daily Work: Mesh                      Milestones: Star (ARB)
  =====================                 =====================

  +----------+------+----------+              +----------+
  | Architect +------+ Frontend |              | Architect|
  +-----+----+      +-----+---+              +----+-----+
        |  \          /    |                       |
        |   \        /     |            +----------+----------+
        |    \      /      |            |          |          |
  +-----+----+\  /  +-----+---+   +----+---+ +---+----+ +---+----+
  | Backend   | \/   |  Reviewer|   |Security| |Scalab. | |Consist.|
  +-----+----+ /\   +----------+   |Critic  | |Critic  | |Critic  |
        |     /  \                  +--------+ +--------+ +--------+
        |    /    \
  +-----+--+      +------+
  | Data    +------+ DevOps|
  +---------+      +-------+
```

### Agents

#### Role 1: Architect (Team Lead)
- **Type:** existing -- `solid-architect`
- **Responsibilities:** Defines system architecture, API contracts, module boundaries. Makes technology decisions. Leads ARB reviews. Ensures architectural consistency.
- **Skills needed:** team-patterns (existing)
- **Model:** opus (architectural decisions require deep reasoning about trade-offs)
- **Communicates with:** All squad members (mesh). Presents to ARB.

#### Role 2: Frontend Implementer
- **Type:** existing -- `independent-contributor`
- **Responsibilities:** Builds React frontend components, implements real-time collaboration UI, WebSocket client integration. Follows API contracts defined by Architect.
- **Skills needed:** None beyond base capabilities
- **Model:** sonnet (implementation work, high throughput)
- **Communicates with:** Architect (API contracts), Backend Implementer (integration), Reviewer

#### Role 3: Backend Implementer
- **Type:** existing -- `independent-contributor`
- **Responsibilities:** Builds Node.js API endpoints, WebSocket server, authentication, business logic. Implements API contracts.
- **Skills needed:** None beyond base capabilities
- **Model:** sonnet (implementation work)
- **Communicates with:** Architect, Frontend Implementer, Data Engineer, Reviewer

#### Role 4: Data Engineer
- **Type:** existing -- `independent-contributor`
- **Responsibilities:** Designs PostgreSQL schema, writes migrations, implements data access layer, optimizes queries, handles real-time data sync logic.
- **Skills needed:** None beyond base capabilities
- **Model:** sonnet (database design, query optimization)
- **Communicates with:** Architect, Backend Implementer, Reviewer

#### Role 5: Code Reviewer / Quality Gate
- **Type:** existing -- `critical-code-reviewer`
- **Responsibilities:** Reviews all code before merge. Checks for security vulnerabilities, performance issues, consistency with architecture. Acts as the reflection loop.
- **Skills needed:** None beyond base capabilities
- **Model:** opus (deep code review requires strong reasoning)
- **Communicates with:** All implementers (reviews their work), Architect (flags architectural concerns)

#### Role 6 (ARB only): Security Critic
- **Type:** existing -- `web-bug-hunter` (activated only during ARB reviews)
- **Responsibilities:** Reviews architecture and code for security vulnerabilities. Evaluates auth design, data handling, input validation.
- **Model:** sonnet (security-focused analysis)
- **Communicates with:** Architect (during ARB review only)

### Task Dependency Graph

```
  Phase 1: Architecture
  Task 1: Define system architecture + API contracts   -->  Owner: Architect
  Task 2: ARB Review #1 (architecture)                 -->  Owner: ARB panel (blocked by: 1)

  Phase 2: Foundation
  Task 3: Set up project scaffolding + CI/CD           -->  Owner: Backend Impl (blocked by: 2)
  Task 4: Design database schema + migrations          -->  Owner: Data Engineer (blocked by: 2)
  Task 5: Implement auth system                        -->  Owner: Backend Impl (blocked by: 3)

  Phase 3: Core Features (parallel)
  Task 6: Build API endpoints (CRUD)                   -->  Owner: Backend Impl (blocked by: 5)
  Task 7: Build frontend components                    -->  Owner: Frontend Impl (blocked by: 3)
  Task 8: Implement WebSocket server                   -->  Owner: Backend Impl (parallel with: 7)
  Task 9: Implement real-time collaboration UI         -->  Owner: Frontend Impl (blocked by: 8)

  Phase 4: Integration + Review
  Task 10: Integration testing                         -->  Owner: Reviewer (blocked by: 6,7,9)
  Task 11: ARB Review #2 (pre-launch)                  -->  Owner: ARB panel (blocked by: 10)
```

### Agent Count Justification

**Total agents: 5 daily + 1 activated for ARB reviews = 6 max**

Daily mesh channels: 5(5-1)/2 = 10 channels. Manageable for a mesh topology (well under the 21-channel limit for 7 agents).

ARB reviews activate 1 additional agent temporarily, bringing total to 6. This is still within the optimal range. The squad pattern intentionally keeps the team small for greenfield work where rapid iteration matters more than parallelism.

### Capability Gap Assessment

**No critical gaps.** Minor notes:
- No dedicated DevOps/infrastructure agent exists. The Backend Implementer handles CI/CD setup as part of scaffolding. For a more complex deployment (Kubernetes, multi-region), a dedicated DevOps agent would be needed.
- No dedicated frontend testing agent. The Reviewer covers this, but a `testing-expert` could be added if E2E test coverage becomes a priority.

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Over-engineering (greenfield temptation) | Architect enforces "build the simplest thing that works" principle. ARB Review #1 specifically checks for unnecessary complexity. |
| Architectural drift between implementers | API contracts are defined upfront (Task 1). Reviewer catches deviations. Architect is available for clarification in mesh. |
| ARB bottleneck slowing delivery | ARB reviews are scheduled at 2 fixed milestones only, not on every change. Daily work is unblocked. |
| Real-time features adding unexpected complexity | WebSocket work is a separate track (Tasks 8-9) that can be descoped to Phase 2 if needed. |

### Execution Readiness

**READY.** All agents exist. Architect uses `solid-architect`, implementers use `independent-contributor`, reviewer uses `critical-code-reviewer`, security critic uses `web-bug-hunter`.
