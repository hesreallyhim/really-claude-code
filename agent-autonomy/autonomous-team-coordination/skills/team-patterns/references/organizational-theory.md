# Organizational Theory Patterns

Extracted from the comprehensive team patterns catalog. Covers foundational organizational theory that constrains and informs team design decisions.

---

## 3.1 Conway's Law

**Statement:** "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations." (Melvin Conway, 1967)

**Implication for teams:** The technical architecture of your system will mirror your team structure, whether you want it to or not. A company with separate frontend and backend teams will inevitably produce a system with a clear frontend-backend split.

**The Inverse Conway Maneuver:** Structure your teams to mirror the architecture you WANT, rather than letting existing communication structures dictate the design. Example: Flo embedded iOS and Android engineers in backend-heavy teams, pushing functionality to the backend and enabling 20-30 releases per day (up from 3-week cycles).

**Relevance to AI agent teams:** Agent team structure will shape the solution architecture. If you create separate "planning" and "execution" agents, the system will produce plans and executions as distinct artifacts. Design your agent team topology to mirror the solution structure you want.

---

## 3.2 Brooks's Law

**Statement:** "Adding manpower to a late software project makes it later." (Fred Brooks, *The Mythical Man-Month*, 1975)

**Three mechanisms:**
1. **Communication overhead:** Grows quadratically with team size (see 3.5)
2. **Ramp-up time:** New members must be trained, consuming existing members' time
3. **Task indivisibility:** Some tasks cannot be meaningfully parallelized ("nine women cannot make a baby in one month")

**A fourth explanation (arXiv:1904.02472):** Group dynamics and social-psychological factors provide additional friction beyond pure coordination costs.

**Relevance to AI agent teams:** Adding more agents to a system does not proportionally increase throughput. Each additional agent increases coordination overhead (context sharing, state synchronization). Most production multi-agent systems use at most 2 levels of hierarchy because deeper hierarchies add latency and token costs faster than they add capability.

---

## 3.3 Tuckman's Stages of Group Development

**Origin:** Bruce Tuckman, 1965. Later added a fifth stage (Adjourning) in the 1970s.

**The stages:**

| Stage | Characteristics | Leadership Style |
|-------|----------------|------------------|
| **Forming** | Polite, anxious, focused on self. Members unsure of purpose and fit. | Directing |
| **Storming** | Conflict and competition. Personality clashes. Performance may decrease. Subgroups form. Most difficult and critical stage. | Coaching |
| **Norming** | Communication improves. Conflicts resolve. Sense of belonging develops. Productivity improves. | Participating |
| **Performing** | True interdependence. High competence and confidence. "Can do" attitude. Problems solved proactively. Not all teams reach this stage. | Delegating |
| **Adjourning** | Goals accomplished. Team disbands. Ceremonial acknowledgment of work. | Supporting |

**Key insights:**
- Progression is NOT linear; teams often regress to earlier stages when membership changes
- Ensemble programming is the fastest known way to move teams from storming to norming
- The storming stage is critical: teams that cannot resolve it never reach performance

**Relevance to AI agent teams:** Agent teams have an analog: initial configuration (forming), discovering conflicts in approach/output format (storming), establishing shared protocols and conventions (norming), and achieving effective collaboration (performing). When agent team composition changes (adding/removing agents), the system may need re-calibration. Temporary regression after composition changes mirrors Tuckman's regression pattern.

---

## 3.4 Ringelmann Effect (Social Loafing)

**Origin:** Max Ringelmann, rope-pulling experiment, 1913. Confirmed by Alan Ingham's blindfolded experiment (participants who THOUGHT they were in a group exerted 20% less effort, even though they were alone).

**Statement:** Individual productivity decreases as group size increases, due to two factors:
1. **Motivation loss (social loafing):** Members rely on co-workers to furnish effort, even when they believe they are contributing at maximum potential
2. **Coordination problems:** Communication and synchronization overhead

**Mitigations:**
- Keep teams small (4-8 optimal)
- Increase identifiability of individual contributions
- Set clear, explicit goals
- Define roles and accountability

**Relevance to AI agent teams:** Agents do not experience motivational loss, but they DO experience coordination overhead. The analog to social loafing in AI systems is redundant computation: multiple agents doing overlapping work without knowing it. Mitigation: clear task boundaries, non-overlapping responsibilities, and explicit output expectations for each agent.

---

## 3.5 Communication Overhead Formula

**Formula:** n x (n-1) / 2, where n = team size

**Origin:** Fred Brooks, *The Mythical Man-Month* (1975).

| Team Size (n) | Communication Channels |
|---|---|
| 3 | 3 |
| 5 | 10 |
| 7 | 21 |
| 9 | 36 |
| 10 | 45 |
| 12 | 66 |
| 15 | 105 |
| 20 | 190 |

**Key thresholds:**
- **Optimal team size:** 4-8 members (Harvard Business School: 4.6 optimal)
- **Dunbar's number:** ~150 for social relationships; ~9 for close working relationships (beyond 9, invisible sub-teams form)
- **Bain & Company:** Each additional member beyond 7 reduces decision effectiveness by ~10%. At 17+, decisions stall.

**Mitigation for large projects:** Create sub-teams of 5-7 with designated leads. Leads communicate with each other (reducing N to the number of leads). Also: reduce per-channel cost through tooling (SCM, automated testing, CI/CD).

**Relevance to AI agent teams:** Agent systems face the same quadratic scaling. With 10 agents in a mesh topology, there are 45 potential communication channels. This is why hierarchical and star topologies (supervisor-worker) are strongly preferred over mesh topologies in production multi-agent systems. A tree topology with sub-teams of 3-5 agents under sub-supervisors is the most scalable architecture.
