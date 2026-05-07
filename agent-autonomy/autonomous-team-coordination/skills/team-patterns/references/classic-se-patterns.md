# Classic Software Engineering Team Patterns

Extracted from the comprehensive team patterns catalog. Covers established team organization patterns from software engineering practice.

---

## 1.1 Incident Response / War Room Pattern

**Origin:** Adapted from military Incident Command System (ICS); formalized for software by Google SRE and PagerDuty.

**When to use:** Production outages, security breaches, or any time-critical system failure requiring coordinated resolution under pressure.

**Team size and roles (4-6 core):**
- **Incident Commander (IC):** Leads the response, makes decisions, delegates. Does NOT touch the code. Asks sharp questions, sets priorities, manages resources.
- **Communications Lead (Comms Lead):** Manages information flow to external stakeholders (executives, status pages, customers). Converts technical jargon into business impact. Protects technical team from interruptions.
- **Operations Lead / Technical Responders:** Subject matter experts who investigate and fix the issue. Multiple responders may be pulled in based on the incident's domain.
- **Scribe:** Records key actions, owners, and timestamps in real-time. Maintains the incident timeline for post-incident review.

**Communication topology:** Hub-and-spoke. The IC is the central hub; all communication flows through or is coordinated by the IC. A dedicated channel (Slack/conference call) serves as the information ledger.

**Strengths:**
- Clear chain of command prevents chaos during high-pressure situations
- Separation of concerns (technical vs. communication vs. documentation)
- Transfer of command protocol handles fatigue in long incidents
- Modeled after battle-tested emergency services protocols

**Weaknesses:**
- Requires pre-trained IC personnel; not everyone can perform the role under pressure
- Overhead is excessive for minor incidents
- Single point of failure if the IC is ineffective

**AI agent mapping:** Maps directly to a supervisor-worker pattern. An orchestrator agent acts as IC, delegating diagnostic tasks to specialist agents (log analyzer, metrics checker, dependency tracer). A separate comms agent handles status updates. A scribe agent maintains an immutable event log.

---

## 1.2 Tiger Teams

**Origin:** Military term; popularized by NASA during Apollo 13 (1970). A 1964 paper defined them as "a team of undomesticated and uninhibited technical specialists, selected for their experience, energy, and imagination, and assigned to track down relentlessly every possible source of failure."

**When to use:** High-impact, high-priority problems that have resisted conventional solutions. Projects that are failing or blocked. Opportunities with extremely high potential that require rapid expert response.

**Team size and roles (3-7):**
- Handpicked senior-level experts from different disciplines (engineering, security, operations, etc.)
- A corporate sponsor who provides resources, funding, and organizational authority
- Fully removed from business-as-usual obligations for the duration

**Communication topology:** Mesh. All members communicate freely with each other. Often co-located in a dedicated "war room" space.

**Strengths:**
- Extreme focus and autonomy accelerate problem-solving
- Cross-functional composition breaks through organizational silos
- Operates outside normal constraints and processes
- Disbanded after resolution, so no ongoing organizational overhead

**Weaknesses:**
- Expensive: removes top experts from their regular duties
- Risk of disrupting existing team dynamics when members are pulled away
- Can create resentment among non-selected team members
- Not appropriate for routine or low-priority work

**AI agent mapping:** Spawn a temporary group of specialist agents with elevated tool access and relaxed constraints. Each agent brings domain expertise (security scanner, performance profiler, architecture analyzer). The group operates with a shared scratchpad/blackboard and disbands when the task is resolved.

---

## 1.3 Architecture Review Board (ARB)

**Origin:** Formalized by TOGAF (The Open Group Architecture Framework). Widely adopted in enterprise software governance.

**When to use:** Before build/purchase decisions, before deployment to production, when evaluating new technology adoption, or when ensuring compliance with enterprise architecture standards.

**Team size and roles (4-10, with rotating membership):**
- 4-5 permanent members: senior architects, principal engineers
- Rotating members from Security, Development, Enterprise Architecture, Infrastructure, Operations
- An executive sponsor to ensure organizational authority

**Communication topology:** Star/hub-and-spoke. Project teams present proposals to the board. The board deliberates internally (mesh) and issues decisions.

**Strengths:**
- Ensures architectural consistency and standards across the organization
- Embeds security considerations from the outset
- Risk mitigation through early review
- Knowledge sharing across organizational boundaries

**Weaknesses:**
- Can become a bottleneck if not run efficiently ("approval gate" anti-pattern)
- Risks becoming an "ivory tower" disconnected from delivery realities
- May slow agile delivery if reviews are not embedded into the workflow
- Potential for rubber-stamping if members lack engagement

**AI agent mapping:** A panel of specialist critic agents that review proposed designs. One agent checks for security concerns, another for scalability, another for consistency with existing patterns. A moderator agent synthesizes opinions and issues a verdict. Analogous to the debate/adversarial pattern with a judge.

---

## 1.4 Mob Programming / Ensemble Programming

**Origin:** Coined by Woody Zuill (circa 2012). Evolved from pair programming in Extreme Programming (XP). "Ensemble programming" is the preferred modern term.

**When to use:** Complex problem-solving requiring diverse expertise. Onboarding new team members. Getting a team through the "storming" phase (Tuckman). High-stakes code where quality is paramount.

**Team size and roles (3-5 core, up to 7):**
- **Driver:** Operates the keyboard. Follows the navigator's directions. Minimal autonomous decision-making.
- **Navigator:** Decides what to create. Translates the mob's ideas into instructions for the driver.
- **Mob (remaining members):** Generate ideas, interrogate code quality, spot potential issues.
- **Optional roles:** Automationist (watches for automation opportunities), Nose (calls out code smells).

**Communication topology:** Hub-and-spoke during active coding (navigator is hub). Mesh during discussion phases.

**Rotation:** Every 5-15 minutes (shorter is better). When the timer goes off, the driver becomes a navigator, and a new driver steps in. Everyone cycles through all roles.

**Core rule (Strong-style):** "For an idea to go from your head into the computer, it MUST go through someone else's hands."

**Strengths:**
- Continuous real-time peer review catches bugs within minutes
- Fastest way to get teams through Tuckman's storming phase
- Accelerates knowledge transfer and junior developer growth
- Eliminates knowledge silos and bus factor concerns

**Weaknesses:**
- Appears expensive (N people, 1 keyboard)
- Requires discipline to maintain rotation and engagement
- Can degenerate into "Mob Wars" (anti-pattern) if mutual respect breaks down
- "Loud Driver" anti-pattern: driver proceeds without mob input

**AI agent mapping:** A shared workspace where one agent writes code while others observe and critique. A "navigator" agent provides high-level direction. Rotate which agent is the "driver" (code producer) vs. "reviewer" each iteration. The key principle--ideas must pass through another agent's hands--maps naturally to generator-critic architectures.

---

## 1.5 Pair Programming Patterns

**Origin:** Extreme Programming (XP), formalized by Kent Beck in the late 1990s.

### 1.5.1 Driver-Navigator (Classic)

**When to use:** General-purpose collaborative coding, especially effective with two experts or one expert + one novice.

**Roles:** Driver (keyboard, tactical focus) and Navigator (big picture, edge cases, architecture).

**Communication topology:** Point-to-point bidirectional.

**Key principle:** Navigator avoids tactical thinking; driver avoids strategic thinking. Each complements the other. "5-second rule": wait 5 seconds before correcting the driver.

### 1.5.2 Ping-Pong Pairing

**When to use:** Well-defined tasks implementable via Test-Driven Development (TDD).

**Flow:** Person A writes a failing test. Person B makes it pass. Person B writes a failing test. Person A makes it pass. Refactor together between cycles.

**Communication topology:** Alternating point-to-point. Naturally divides work without needing explicit rotation discipline.

**Strengths:** Enforces TDD. Natural role switching. Clear division of labor.

### 1.5.3 Strong-Style Pairing

**When to use:** Onboarding, initial knowledge transfer, or when one partner is significantly more experienced.

**Core rule:** "For an idea to go from your head into the computer, it MUST go through someone else's hands." If the driver has an idea, they must switch to navigator and direct the other person.

**Strengths:** Forces active learning by doing. Completely engages the observer. Great for knowledge transfer.

**Weaknesses:** Borders on micro-management if overused. Can feel restrictive for experienced developers.

**AI agent mapping:** Two-agent collaboration. Ping-pong maps naturally to a test-writer agent and an implementation agent alternating turns. Strong-style maps to a "brain" agent that cannot directly execute, paired with an "executor" agent that can only act on instructions.

---

## 1.6 Spotify Model (Squads, Tribes, Chapters, Guilds)

**Origin:** Henrik Kniberg and Anders Ivarsson, "Scaling Agile @ Spotify," 2012. Described how Spotify organized at the time; explicitly NOT intended as a generic framework to copy.

**When to use:** Scaling agile practices across a large organization (100+ engineers). Works best when adapted to local context rather than copied literally.

**Structure:**

| Unit | Size | Purpose | Analogy |
|------|------|---------|---------|
| **Squad** | 6-12 | Cross-functional, autonomous team focused on one feature area. Chooses its own agile methodology. | Mini-startup |
| **Tribe** | 40-100 (collection of squads) | Squads working on related product areas. Led by a Tribe Lead. Limited to ~100 people (Dunbar's number). | Department |
| **Chapter** | Varies (within a tribe) | People with the same skill set across squads within a tribe. Led by a Chapter Lead who is also a squad member. | Functional specialty |
| **Guild** | Dozens to hundreds (cross-tribe) | Voluntary community of interest that transcends organizational boundaries. No formal leader; has a Guild Coordinator. | Community of practice |
| **Trio** | 3 | Tribe Lead + Product Lead + Design Lead. Ensures balanced perspective. | Leadership team |
| **Alliance** | Multiple tribes | Formed when tribes must collaborate on large cross-functional goals. | Program |

**Communication topology:** Matrix. Squads operate as mesh internally. Tribes provide vertical alignment. Chapters and guilds provide horizontal alignment across squads and tribes.

**Strengths:**
- High autonomy with alignment
- Reduces top-heavy management
- Guilds enable organic knowledge sharing
- Scales to hundreds of engineers

**Weaknesses:**
- Failed at Spotify itself due to high autonomy without sufficient collaboration guidance
- Overlapping organizational layers (chapters vs. guilds) create confusion
- Not a framework to copy; must be adapted
- "Like trying to transplant a kidney from a total stranger" (Kate Hobler)

**AI agent mapping:** Squads map to agent crews (CrewAI-style) with autonomous mission focus. Tribes map to higher-level orchestrators coordinating related crews. Chapters map to shared tool/capability pools that agents across different crews can access. Guilds map to knowledge bases or shared memory that any agent can query.

---

## 1.7 DevOps Team Topologies

**Origin:** Matthew Skelton and Manuel Pais, *Team Topologies: Organizing Business and Technology Teams for Fast Flow* (2019).

**When to use:** Any organization seeking to optimize software delivery flow. Addresses the shortcomings of models like the Spotify model by providing clearer team boundaries.

**Four fundamental team types:**

### 1.7.1 Stream-Aligned Teams (60-80% of teams)

**Purpose:** Aligned to a single, valuable stream of work (product, service, user journey). Owns work from beginning to end. No hand-offs.

**Size:** 5-9 people, cross-functional (dev, test, ops).

**Communication topology:** Self-contained mesh internally. Minimal external dependencies.

**Strengths:** Fast flow, end-to-end ownership, clear accountability.
**Weaknesses:** Can reinvent wheels without platform support.

### 1.7.2 Enabling Teams (5-15% of teams)

**Purpose:** Specialist teams that help stream-aligned teams overcome obstacles and develop new capabilities. Assistance is temporary. "Servant leaders" of the team types.

**Communication topology:** Facilitating interaction mode. Moves freely across the organization.

**Strengths:** Prevents ivory towers. Upskills other teams.
**Weaknesses:** Must avoid becoming permanent dependencies.

### 1.7.3 Complicated-Subsystem Teams (rare; as needed)

**Purpose:** Handles highly specialized, computationally complex areas (ML models, advanced algorithms, legacy system maintenance). Created only when skills are so specialized they must be pooled.

**Communication topology:** X-as-a-service to stream-aligned teams.

**Strengths:** Reduces cognitive load on stream-aligned teams.
**Weaknesses:** Creates a dependency. Should be avoided unless truly necessary.

### 1.7.4 Platform Teams (15-25% of teams)

**Purpose:** Provides internal services (auth, logging, data storage, CI/CD) that reduce cognitive load of stream-aligned teams. Treats internal services as products.

**Communication topology:** X-as-a-service. Stream-aligned teams consume platform services with minimal interaction.

**Strengths:** Reduces duplication. Accelerates stream-aligned teams.
**Weaknesses:** Must genuinely serve stream-aligned team needs, not become bureaucratic.

**Three interaction modes:** Collaboration (co-creation for a defined period), X-as-a-Service (provider/consumer), Facilitating (support and mentoring).

**AI agent mapping:**
- Stream-aligned = Primary task-execution agents with end-to-end ownership
- Enabling = Utility agents that temporarily augment other agents' capabilities (e.g., a "code review helper" agent)
- Complicated-subsystem = Specialist agents for complex tasks (e.g., ML model training agent, regex generator)
- Platform = Infrastructure agents providing shared services (memory management, tool access, API calls)
