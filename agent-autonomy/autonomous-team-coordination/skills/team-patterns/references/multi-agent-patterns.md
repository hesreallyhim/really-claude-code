# Multi-Agent AI Patterns

Extracted from the comprehensive team patterns catalog. Covers coordination and orchestration patterns specifically designed for multi-agent AI systems.

---

## 2.1 Supervisor-Worker (Hierarchical Orchestration)

**Origin:** Classic distributed systems pattern; adapted for AI agents by AutoGen, LangGraph, CrewAI, and cloud providers (Azure, Google ADK).

**When to use:** Open-ended tasks where the full scope is not known upfront. Tasks requiring dynamic delegation and coordination. Enterprise workflows with multiple specialized sub-teams.

**Roles:**
- **Supervisor/Orchestrator:** Receives the high-level goal, decomposes it, delegates to workers, monitors progress, synthesizes results
- **Workers:** Specialized agents that execute assigned sub-tasks

**Communication topology:** Tree (hierarchical). Supervisor at root, workers as leaves. Can be multi-level (supervisor -> sub-supervisors -> workers), though most production systems use at most two levels due to latency/token overhead.

**Strengths:**
- Clear delegation and oversight
- Dynamic task allocation based on intermediate results
- Supervisor can spawn additional agents or redirect work
- Natural fit for complex, multi-step workflows

**Weaknesses:**
- Each hierarchy level adds latency and token cost
- Single point of failure at the supervisor
- Over-centralization can bottleneck throughput

**Frameworks:** LangGraph (agent supervisor tutorial), CrewAI (role-based crews), Azure Architecture Center (Scheduler-Agent-Supervisor pattern), Google ADK.

---

## 2.2 Sequential Pipeline

**Origin:** Classic data processing pattern (Unix pipes); adapted for agent chains by LangChain, LangGraph, Google ADK.

**When to use:** Tasks with clear, ordered stages. Document processing (extract -> transform -> validate -> store). Content generation (research -> outline -> draft -> edit).

**Roles:** Chain of specialized agents, each processing the output of the previous agent.

**Communication topology:** Linear pipeline. Each agent receives input from and passes output to the next agent in sequence.

**Strengths:**
- Simple, deterministic, easy to debug
- Each stage is independently testable
- Clear data flow

**Weaknesses:**
- No parallelism; total latency is the sum of all stages
- Failure in one stage blocks the entire pipeline
- Rigid; cannot adapt to unexpected intermediate results

**Implementation:** Google ADK's `SequentialAgent` primitive. LangGraph's linear graph. Each agent writes to shared `session.state` using `output_key`.

---

## 2.3 Fan-Out / Fan-In (Parallel)

**Origin:** MapReduce (Google, 2004); adapted for agent orchestration.

**When to use:** Tasks that can be decomposed into independent subtasks that run in parallel. Code review (security scanner + style checker + complexity analyzer in parallel, then a summarizer consolidates).

**Roles:**
- **Dispatcher:** Splits the task into independent subtasks
- **Parallel Workers:** Execute subtasks concurrently
- **Aggregator:** Consolidates results from all workers

**Communication topology:** Fan-out from dispatcher to workers; fan-in from workers to aggregator. Star topology during execution.

**Strengths:**
- Dramatic latency reduction for parallelizable tasks
- Natural fit for review, analysis, and search tasks
- Easy to scale by adding more workers

**Weaknesses:**
- Workers must be truly independent (no shared mutable state during execution)
- Aggregation can be complex if outputs are heterogeneous
- Higher total compute cost than sequential

**Implementation:** Google ADK's `ParallelAgent`. Azure Durable Functions fan-out/fan-in pattern. LangGraph's parallel branches.

---

## 2.4 Debate / Adversarial Pattern

**Origin:** AI safety research on multi-agent debate (MAD). Inspired by adversarial processes in law (prosecution vs. defense) and philosophy (dialectic method).

**When to use:** High-stakes decisions where output quality matters more than speed. Architecture decisions, code review, verification tasks. AI safety: ensuring robust reasoning by forcing agents to defend and attack positions.

**Roles:**
- **Debaters (2+):** Agents assigned distinct roles (e.g., "affirmative" and "negative," "angel" and "devil"). Each independently generates and defends arguments.
- **Judge/Moderator:** Evaluates rounds, adjudicates persistent disagreements, selects the best answer.

**Communication topology:** Structured mesh between debaters. Hub-and-spoke with judge as hub for final decisions.

**Strengths:**
- Significantly improves output quality for high-stakes decisions
- Can reduce model toxicity when jailbroken models debate with aligned models
- Forces consideration of multiple perspectives
- "Generator-Critic" variant is simpler: one agent creates, one validates against hard-coded criteria

**Weaknesses:**
- Expensive (2x+ compute per round)
- Convergence not guaranteed; agents may never agree
- Collusion risk: adversarial agents can form false majority consensus, making the system LESS safe (research from December 2024)
- Mitigation: a verifier agent checking outputs against trusted guidelines completely blocked collusion in tested scenarios

**Key research:** "Combating Adversarial Attacks with Multi-Agent Debate" (arXiv:2401.05998). "Many-to-One Adversarial Consensus" (arXiv:2512.03097). AGENTBREEDER framework for evolutionary multi-agent safety.

---

## 2.5 Voting-Based Ensemble (Majority Consensus)

**Origin:** Classical ensemble methods in machine learning (bagging, boosting); adapted for LLM agents. Social choice theory (Condorcet, Borda count).

**When to use:** When accuracy is critical and independent agents can solve the same problem. Reasoning tasks benefit most from voting; knowledge/factual tasks benefit most from consensus.

**Roles:**
- **N independent solver agents:** Each independently produces an answer
- **Aggregator:** Tallies votes or applies a decision protocol

**Decision protocol types (Kaesberg et al., 2025):**
- **Voting-based:** Simple, Ranked, Cumulative, Approval
- **Consensus-based:** Majority, Supermajority, Unanimity

**Communication topology:** Star (agents report independently to aggregator) for voting. Mesh (peer-to-peer deliberation) for consensus.

**Key research findings:**
- Voting protocols improve performance by 13.2% in reasoning tasks
- Consensus protocols improve performance by 2.8% in knowledge tasks
- Most performance gains of multi-agent debate stem from majority voting, not the debate process itself (martingale property)
- If each of 5 agents has 80% accuracy, majority voting yields significantly higher overall accuracy (Condorcet Jury Theorem)
- New methods: All-Agents Drafting (AAD) improves performance by 3.3%; Collective Improvement (CI) improves by 7.4%

**Strengths:**
- Simple majority voting is "surprisingly strong" as a baseline
- Parallelizable; all agents can run concurrently
- Well-understood theoretical foundations from social choice theory

**Weaknesses:**
- More agents = higher latency and cost
- No agent interaction in pure voting (no error correction between agents)
- Assumes agent diversity; if all agents make the same errors, voting doesn't help

**Frameworks:** Swarms (MajorityVoting module with multi-loop consensus building), AutoGen (scriptable voting workflows).

---

## 2.6 Reflection / Self-Critique Pattern

**Origin:** Reflexion (Shinn et al., 2023). Identified by Andrew Ng as one of four key agentic AI design patterns.

**When to use:** Any task where iterative refinement improves quality. Coding, writing, strategic planning. When initial outputs consistently have errors that can be caught by critique.

**Variants:**

### Basic Reflection (Generator-Critic)
- **Generator agent:** Produces initial output
- **Critic agent:** Reviews output against criteria, provides feedback
- Loop continues for N iterations or until quality threshold is met

### Reflexion (Single-Agent Self-Reflection)
- Agent explicitly critiques each response, grounded in external data
- Uses metrics: success state, current trajectory, persistent memory
- GPT-4 accuracy improved from 78.6% to 97.1% with unredacted reflection

### Multi-Agent Reflection
- One agent generates, another critiques, together they refine
- "AI agents testing AI agents" outperforms single-model self-correction
- Production implementations increasingly rely on external verification systems

**Communication topology:** Bidirectional loop (generator <-> critic). Can be single-agent (self-reflection) or multi-agent.

**Strengths:**
- 9.0-18.5 percentage point improvement in problem-solving performance
- Natural fit for coding tasks (write -> test -> fix cycle)
- Can be layered onto any other pattern

**Weaknesses:**
- Intrinsic self-correction has significant limitations: LLMs generate plausible but internally coherent errors
- Susceptible to "non-optimal local minima" (Reflexion)
- Limited long-term memory (sliding window bounded by token limit)
- Adds latency per iteration

---

## 2.7 Tree of Thoughts (ToT) and Language Agent Tree Search (LATS)

**Origin:** Tree of Thoughts (Yao et al., 2023). LATS (Zhou et al., 2023) unifies ToT with Reflexion and Monte Carlo Tree Search.

**When to use:** Complex tasks requiring exploration of multiple reasoning paths. Coding, interactive QA, web navigation, mathematical reasoning. When response quality matters more than speed.

**LATS process:**
1. **Select:** Pick best next actions based on aggregate rewards
2. **Expand and simulate:** Select top 5 potential actions, execute in parallel
3. **Reflect + Evaluate:** Observe outcomes, score decisions using both environmental and LLM feedback
4. **Backpropagate:** Update scores of root trajectories

**Communication topology:** Tree (search tree where each node is a partial solution). Agents can backtrack to previous nodes and explore alternative branches.

**Strengths:**
- Unifies reasoning, acting, and planning in a single framework
- Self-reflection dramatically improves performance over pure tree search
- Outperforms ReAct, Reflexion, and standalone ToT on multiple benchmarks

**Weaknesses:**
- Significantly more computational resources and time than single-agent methods
- Not appropriate for low-latency applications
- Tested primarily on relatively simple benchmarks; less proven on complex multi-tool scenarios

---

## 2.8 Blackboard Architecture

**Origin:** 1980s AI research; originally proposed as a decentralized problem-solving approach imitating experts working around a shared blackboard.

**When to use:** Complex, unstructured problems requiring incremental solution building. Medical diagnosis, signal interpretation, multi-source intelligence analysis. When agents need both shared and private workspace.

**Components (bMAS variant, arXiv July 2025):**
- **Blackboard:** Multifunctional shared space with public and private sections. Public: dialogues and knowledge visible to all agents. Private: space for particular agents to debate or self-reflect.
- **Agent Group:** Agents with various functions (planning, reasoning, criticizing, tool use)
- **Control Unit:** Takes query + current blackboard state, selects suitable agents for the next round

**Communication topology:** Star + shared memory. Agents do not communicate directly with each other; they read from and write to the blackboard. The control unit orchestrates agent selection.

**Strengths:**
- Highly effective for complex, unstructured problems
- Dynamic adaptation: control unit selects appropriate agents per round
- Private blackboard sections allow focused sub-deliberation
- Agents can contribute asynchronously and incrementally

**Weaknesses:**
- Complex to implement (shared state management)
- Control unit is a potential bottleneck
- Race conditions possible with concurrent blackboard access
- Hard to debug (implicit communication via shared state)

**Modern implementations:** GitHub `agent-blackboard` (multi-agent coordination for software engineering with 9 specialized agents). Medium article by Denis Petelin on combining MCP with the blackboard pattern.

---

## 2.9 Mixture of Experts (MoE) Applied to Agents

**Origin:** Machine learning (Jacobs et al., 1991). Popularized at scale by DeepSeek-V3 (671B parameters, 37B active per forward pass).

**When to use:** When different sub-problems require fundamentally different expertise. When you want efficiency (not all experts active simultaneously).

**Roles:**
- **Router/Gating Network:** Determines which expert(s) to activate for a given input
- **Expert Agents:** Specialized in different domains
- **Aggregator:** Combines outputs from activated experts

**Communication topology:** Star (router -> selected experts -> aggregator). Only a subset of experts is active at any time.

**Strengths:**
- Computational efficiency: only relevant experts are activated
- Natural specialization without cross-contamination
- Scales to very large numbers of experts

**Weaknesses:**
- Router quality is critical; poor routing = wrong experts
- Training/calibrating the router is non-trivial
- Load balancing across experts can be challenging

**AI agent mapping:** A dispatch agent examines the incoming task and routes to the appropriate specialist agent(s). Only relevant specialists are activated, keeping costs low. The dispatch agent combines results. This is essentially what CrewAI's crew orchestration does at a higher level.

---

## 2.10 Chain-of-Thought Decomposition Across Agents

**Origin:** Chain-of-thought prompting (Wei et al., 2022). Extended to multi-agent systems where different agents handle different reasoning steps.

**When to use:** Complex tasks requiring step-by-step reasoning where each step benefits from different specialization.

**Roles:**
- **Decomposer:** Breaks the task into reasoning steps
- **Step-Specialist Agents:** Each handles one step of the reasoning chain
- **Synthesizer:** Combines step outputs into a final answer

**Communication topology:** Linear pipeline (each step feeds into the next).

**Strengths:**
- Makes reasoning transparent and debuggable
- Each agent can be optimized for its specific reasoning step
- Natural fit for tasks that humans solve step-by-step

**Weaknesses:**
- Requires accurate decomposition upfront
- Errors in early steps cascade through the chain
- Sequential dependency limits parallelism

---

## 2.11 Role-Based Crew Pattern (CrewAI)

**Origin:** CrewAI framework (2024). Inspired by real-world organizational structures.

**When to use:** Content pipelines, report generation, structured team workflows where roles are well-defined.

**Structure:**
- **Crew:** A team of agents with defined roles, tasks, and collaboration protocols
- **Flows:** Deterministic, event-driven task orchestration layered above crews
- Each agent has a role (Researcher, Developer, Editor), a set of tools, and a backstory

**Communication topology:** Configurable: sequential, hierarchical, or collaborative within a crew. Flows provide higher-level orchestration across crews.

**Strengths:**
- Low learning curve
- Role-based design is intuitive for anyone familiar with human team structures
- Scales through horizontal agent replication and task parallelization

**Weaknesses:**
- Opinionated design becomes constraining for complex orchestration
- Custom orchestration patterns are difficult or impossible
- Many teams report hitting the wall 6-12 months in, requiring rewrites to LangGraph

---

## 2.12 Graph-Based Orchestration (LangGraph)

**Origin:** LangChain / LangGraph (2024). Treats agent interactions as nodes in a directed graph.

**When to use:** Complex decision-making pipelines with conditional logic, branching workflows, and dynamic adaptation. Mission-critical production systems requiring state management, compliance, and debuggability.

**Structure:**
- **Nodes:** Agent actions or decision points
- **Edges:** Transitions between nodes (can be conditional)
- **State:** Typed, persistent state machine with checkpointing

**Communication topology:** Arbitrary directed graph. Supports cycles (loops), branches, parallel paths, and conditional routing.

**Strengths:**
- Maximum control and flexibility
- Production-grade state management with checkpointing
- Traceable and debuggable flows
- Supports any orchestration pattern (sequential, parallel, hierarchical, cyclic)

**Weaknesses:**
- Steepest learning curve among major frameworks
- More code required for simple use cases
- Graph definition can become complex for large systems
