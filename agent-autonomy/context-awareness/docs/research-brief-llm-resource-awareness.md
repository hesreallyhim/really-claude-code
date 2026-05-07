# Research Brief: LLM Self-Awareness of Resource Constraints

**Phase 2 Background Investigation**
**Date**: 2026-03-28
**Research Lead**: Claude (Opus 4.6) with human direction

---

## 1. Executive Summary

- **Budget-aware prompting works, but with caveats.** Multiple empirical studies (TALE, BudgetThinker, BATS, Agent Contracts) demonstrate that providing LLMs with token or tool-call budgets can reduce resource consumption by 40-90% with minimal quality degradation (typically <5%). However, LLMs exhibit "token elasticity" -- when budgets are set too tight, models ignore constraints entirely and may consume *more* tokens than with no budget at all.

- **Continuous budget feedback outperforms one-shot budget injection.** BudgetThinker (2025) found that merely stating a budget constraint in the initial prompt is insufficient; models need periodic reminders of remaining budget as they generate responses. BATS (Google/UCSB/NYU, 2025) confirmed this with tool-call budgets, showing that a lightweight "Budget Tracker" plug-in providing continuous resource awareness improved performance across all budget levels.

- **Adaptive computation is a rapidly maturing field.** The "Reasoning on a Budget" survey (July 2025) catalogs dozens of approaches for matching reasoning effort to problem complexity. Anthropic's own adaptive thinking (Opus 4.6, March 2026) operationalizes this at the product level. The evidence strongly supports that fixed reasoning effort wastes resources -- models overthink simple tasks and underthink hard ones.

- **Context rot is real and universal.** Chroma's 2025 study of 18 frontier models confirmed that *every* model degrades with increasing context length, often well before hitting window limits. This validates the core premise of context-aware resource management: monitoring and managing context consumption is not optional for long-running agent sessions.

- **The specific intersection we're exploring -- giving an LLM agent real-time feedback about its own context window consumption in agentic coding workflows -- has NOT been directly studied.** The closest work is BATS (tool-call budgets for information-seeking agents) and Agent Contracts (formal resource governance for coding agents). No published work provides an LLM with a percentage-based context utilization signal and measures behavioral adaptation in coding workflows.

---

## 2. Search Strategy

### Sources searched
- **Academic databases**: arXiv, Semantic Scholar (via OpenAlex API), ACL Anthology, OpenReview
- **Technical blogs**: Anthropic engineering blog, LangChain blog, Chroma Research
- **Industry reports**: OpenRouter State of AI, Gartner forecasts
- **Community discussions**: Hacker News threads on context rot, Emergent Mind topic pages

### Search terms used
- "LLM context window resource management", "token-budget-aware LLM reasoning"
- "adaptive computation language models", "test-time compute scaling"
- "agentic AI resource allocation", "budget-aware agent"
- "meta-cognition large language models", "LLM self-awareness"
- "SWE-bench efficiency", "agent trajectory reduction"
- "context rot", "lost in the middle", "thinking tokens reasoning effort"
- "LLM ignore budget constraint", "token elasticity"
- "autonomous self-regulation AI agents risks"

### Literature search tool
OpenAlex API queries for the above terms, filtered to 2022-2026. Results were mostly tangential (general LLM surveys) with a few direct hits (TALE, meta-cognition papers).

---

## 3. Findings by Angle

### Angle A: Prior Work on LLM Resource-Aware Behavior

#### Key Papers

**TALE: Token-Budget-Aware LLM Reasoning** (Han et al., Dec 2024; ACL 2025 Findings)
[arXiv:2412.18547](https://arxiv.org/abs/2412.18547)

The foundational paper in budget-aware LLM prompting. TALE injects a token budget into the reasoning prompt and achieves 67% token reduction with <3% accuracy loss on math reasoning tasks. Two variants:
- **TALE-EP** (Estimation & Prompting): Zero-shot budget estimation, no training needed. Achieved 84.46% accuracy on GSM8K while reducing tokens from 318 to 77.
- **TALE-PT** (Post-Training): Internalizes budget awareness via SFT/DPO.

Critical discovery -- **"Token Elasticity"**: When budgets are set too low (e.g., 10 tokens for a problem needing 50), LLMs ignore the constraint entirely and produce *more* tokens than with a reasonable budget. There is a "sweet spot" for each problem complexity. This is directly relevant to our plugin: overly aggressive warnings could backfire.

**BudgetThinker: Empowering Budget-Aware LLM Reasoning with Control Tokens** (Wen et al., Aug 2025)
[arXiv:2508.17196](https://arxiv.org/abs/2508.17196)

Inserts special control tokens periodically during inference to continuously inform the model of its remaining token budget. Key finding: **merely stating a budget in the initial prompt is insufficient** -- models need ongoing reminders. Two-stage training: SFT for budget familiarity, then curriculum RL with length-aware rewards. Improved accuracy by 4.9% over baselines across all tested budgets.

**This directly validates our plugin's approach of injecting context awareness signals on every tool call rather than just in the system prompt.**

**BATS: Budget-Aware Tool-Use Enables Effective Agent Scaling** (Google/UCSB/NYU, Nov 2025)
[arXiv:2511.17006](https://arxiv.org/abs/2511.17006)

The closest published work to our research question, applied to information-seeking agents. Key findings:
- Standard ReAct agents plateau and cannot utilize additional budget beyond a certain point.
- A "Budget Tracker" providing continuous budget awareness at the prompt level enables agents to leverage larger budgets effectively.
- Budget-aware agents achieved **comparable accuracy using 40.4% fewer search calls and 31.3% lower overall cost**.
- The authors prioritize tool-call budgets over token budgets, arguing they are more "relevant, consistent, and practicable" as a constraint on agent capability.
- Provides **the first systematic study on budget-constrained agents**, showing budget-aware methods push the cost-performance Pareto frontier.

**Agent Contracts: A Formal Framework for Resource-Bounded Autonomous AI Systems** (Ye & Tan, Jan 2026; COINE/AAMAS 2026)
[arXiv:2601.08815](https://arxiv.org/abs/2601.08815)

Formalizes resource-bounded agent execution. Empirical validation on coding tasks (LiveCodeBench):
- **CONTRACTED** agents (50K token budget, 3 max iterations, dynamic status updates) vs **UNCONTRACTED** (no limits, 6 max iterations).
- Results: 90% token reduction, 525x lower variance, with only 7.1 percentage points of quality loss (not statistically significant, p=0.13).
- Zero conservation violations in multi-agent delegation scenarios.
- **"Governance value increases with task complexity"**: medium-difficulty problems showed 92% token savings vs 76% for easy problems.
- Draws explicitly on Simon's bounded rationality: agents with limited resources must satisfice rather than maximize.

**SelfBudgeter: Adaptive Token Allocation for Efficient LLM Reasoning** (May 2025)
[arXiv:2505.11274](https://arxiv.org/abs/2505.11274)

Trains models to predict their own required token budgets based on task complexity using GRPO-based training.

#### Context Engineering as Resource Management

**Anthropic Engineering Blog: Effective Context Engineering for AI Agents** (2025)
[anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Frames context as a finite resource with diminishing returns. Key guidance: "Find the smallest set of high-signal tokens that maximize desired outcomes." Recommends compaction (summarizing at context limits), structured note-taking (external memory), and sub-agent architectures (isolated context per task).

**LangChain: Context Management for Deep Agents** (2025)
[blog.langchain.com](https://blog.langchain.com/context-management-for-deepagents/)

The Deep Agents SDK implements automatic context management: truncates older tool calls when context crosses **85% of the model's available window**, falls back to LLM-generated summarization when truncation is insufficient. This aligns with our plugin's threshold-based approach.

---

### Angle B: Adaptive Computation and Reasoning Effort

#### Scaling Test-Time Compute

**"Scaling LLM Test-Time Compute Optimally"** (Snell et al., Aug 2024)
[arXiv:2408.03314](https://arxiv.org/abs/2408.03314)

Landmark paper showing that compute-optimal strategies can improve test-time compute efficiency by 4x over best-of-N baselines. A smaller model with optimal test-time compute can outperform a 14x larger model on problems with non-trivial baseline success rates.

**"The Art of Scaling Test-Time Compute"** (Dec 2025)
[arXiv:2512.02008](https://arxiv.org/abs/2512.02008)

First large-scale empirical study: 30B+ tokens generated across 8 open-source LLMs (7B-235B parameters), 4 reasoning datasets. Key findings:
- No single test-time scaling strategy universally dominates.
- Reasoning models form "short-horizon" and "long-horizon" categories with distinct performance profiles.
- Optimal TTS performance scales monotonically with compute budget within a strategy.

**"Reasoning on a Budget" Survey** (Alomrani et al., July 2025)
[arXiv:2507.02076](https://arxiv.org/abs/2507.02076)

Comprehensive survey of adaptive test-time compute (TTC). Introduces two-tiered taxonomy:
- **L1 controllability**: Methods operating under fixed compute budgets (e.g., Claude's thinking budget parameter, OpenAI's reasoning effort setting).
- **L2 adaptiveness**: Methods that dynamically scale inference based on input difficulty.

Benchmarks proprietary models and reveals **systemic inefficiencies**: underthinking on hard problems, overthinking on simple ones, limited sensitivity to task complexity. Models frequently waste resources by overthinking "1+1=?" while failing to allocate enough compute for genuinely hard problems.

#### Adaptive Thinking in Production

**Anthropic: Claude Opus 4.6 Adaptive Thinking** (March 2026)
[platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)

Replaces binary reasoning toggles with four effort levels (low/medium/high/max). Adaptive thinking lets the model decide when and how deeply to reason. "Reliably drives better performance than extended thinking with a fixed budget_tokens." Early production testing (Resolve AI blog) found that adaptive thinking "eliminated the need for manually calibrating reasoning depth."

**Concise Chain-of-Thought (CCoT)** (Renze & Guven, Jan 2024)
[arXiv:2401.05618](https://arxiv.org/abs/2401.05618)

Simply instructing an LLM to "think step-by-step" AND "be concise" reduces output tokens by ~48.7% without significant performance loss for GPT-4. However, **GPT-3.5 showed a 27.69% performance penalty on math tasks** -- indicating that less capable models suffer more from reasoning compression. This is relevant for task-type-dependent effort allocation.

#### Quality Degradation by Task Type

**"The Danger of Overthinking: Examining the Reasoning-Action Dilemma"** (Feb 2025)
[arXiv:2502.08235](https://arxiv.org/abs/2502.08235)

Identifies three harmful patterns in agentic overthinking:
- **Analysis Paralysis**: Excessive planning with minimal environmental progress.
- **Rogue Actions**: Error-driven multi-action attempts breaking sequential constraints.
- **Premature Disengagement**: Terminating based on internal predictions rather than environmental feedback.

Extended reasoning can *degrade* performance through redundant reasoning loops or erroneous self-corrections. This is not exclusive to complex problems -- both simple and complex questions can suffer from excessive thinking tokens.

**"Stop Overthinking" Survey** (March 2025)
[GitHub: Awesome-Efficient-Reasoning-LLMs](https://github.com/Eclipsess/Awesome-Efficient-Reasoning-LLMs)

Categorizes efficient reasoning approaches into: (1) model-based (optimizing reasoning models into concise variants), (2) output-based (dynamically reducing reasoning steps during inference), and (3) input-based (enhancing efficiency based on input properties like difficulty).

---

### Angle C: Measurement and Operationalization

#### Efficiency Metrics for Agentic Settings

**SWE-Effi: Re-Evaluating Software AI Agent System Effectiveness Under Resource Constraints** (Sep 2025)
[arXiv:2509.09853](https://arxiv.org/abs/2509.09853)

The most directly relevant benchmark for coding agent efficiency. Introduces effectiveness metrics combining accuracy and resource consumption:
- **EuITB** (Effectiveness under Inference Time Budget): AUC of resolve rate vs. normalized inference time.
- **Token consumption breakdown**: A typical SWE-bench Verified trajectory contains 48.4K tokens across 40 steps, but accumulated input reaches 1.0M tokens due to context resubmission.
- **"Fail Expensively" pattern**: When agents fail, they consume 4x+ more tokens and time than successful attempts. OpenHands with Llama-3.3-70B: 238.9s on failure vs 79s on success.
- **"Token Snowball" effect**: Agent trajectories grow exponentially as context accumulates.

**AgentDiet: Trajectory Reduction** (Xiao et al., Sep 2025; FSE 2026)
[arXiv:2509.23586](https://arxiv.org/abs/2509.23586)

Identifies three categories of waste in agent trajectories: useless information, redundant information, and expired information. Reduces input tokens by 39.9-59.7% while maintaining performance (-1.0% to +2.0% change). **Challenges the assumption that there is a tradeoff between token efficiency and performance** -- reducing low-quality context can actually prevent performance degradation. Notes that current products (Claude Code, Cursor) apply compaction "sparingly, only when the context window is full."

**TheAgentCompany Benchmark** (Dec 2024)
[arXiv:2412.14161](https://arxiv.org/abs/2412.14161)

Defines cost as: `Cost = (Prompt tokens x Prompt cost) + (Completion tokens x Completion cost)`. Introduces realistic factors including environment setup issues, unlike SWE-bench's idealized scenarios.

#### Context Utilization Patterns

**Context Rot: How Increasing Input Tokens Impacts LLM Performance** (Chroma, July 2025)
[research.trychroma.com/context-rot](https://research.trychroma.com/context-rot)

Tested 18 frontier models with controlled experiments. Key findings:
- **Every model degrades** with increasing context length. Not some. All.
- Degradation is non-uniform and model-specific (Claude models "decay the slowest overall").
- Performance drops 20-50% from 10K to 100K tokens even on simple retrieval tasks.
- Context rot is NOT about hitting the limit -- a 200K-window model can degrade significantly at 50K tokens.
- Adding full conversation history (~113K tokens) dropped accuracy 30% compared to a focused 300-token version.

**"Lost in the Middle"** (Liu et al., 2023; TACL 2024)
[arXiv:2307.03172](https://arxiv.org/abs/2307.03172)

Foundational study showing 30%+ accuracy drops when relevant information is in the middle of context. U-shaped performance curve (primacy and recency bias). Cross-model consistency across GPT-3.5, GPT-4, Claude 1.3, and others. Instruction fine-tuning does not fix the bias.

#### Resource-Specific Metrics

No standardized metric suite exists for "resource-aware agent behavior" specifically. The closest are:
- **Tokens per resolved issue** (SWE-Effi)
- **Tool calls per task** (BATS)
- **Burn rate** (our plugin's invention, as far as we can determine)
- **Effectiveness AUC** (SWE-Effi: cumulative success vs. cumulative resource consumption)
- **Outcome efficiency** ("Reasoning on a Budget": proportion of tokens contributing to correctness)

---

### Angle D: Contradictions, Counterevidence, and Gaps

#### Evidence That Budget Signals Can Hurt

**Token Elasticity (TALE, 2024)**: When budgets are too tight, LLMs paradoxically consume *more* tokens. The model ignores unrealistic constraints and produces verbose output. This is a real risk for our plugin: if context awareness messages create a sense of urgency that the model perceives as an unreasonably tight constraint, it could trigger the opposite of the desired behavior.

**Overthinking Induced by Self-Monitoring**: "Revisiting Overthinking in Long Chain-of-Thought from the Perspective of Self-Doubt" (Peng et al., 2025) suggests that self-monitoring mechanisms can become counterproductive. If a model is constantly told it's running low on resources, it may spend additional tokens reasoning about how to conserve resources rather than completing the task -- a metacognitive overhead tax.

**Salesforce's Directive Limit**: Salesforce's CTO noted that LLMs start omitting instructions when given more than ~8 directives. Adding budget awareness signals to an already-complex system prompt may crowd out other important instructions, leading to degraded instruction following on the primary task.

**Analysis Paralysis in Agents**: Research on agentic overthinking (arXiv:2502.08235) identified that excessive self-monitoring can cause agents to spend time planning rather than acting. Budget awareness could exacerbate this if the model interprets resource pressure as a reason to plan more carefully rather than act more efficiently.

#### LLMs Ignoring Resource Feedback

**Limited Metacognitive Reliability**: The Ackerman et al. (Sep 2025, arXiv:2509.21545) study found that frontier LLMs show "increasingly strong evidence" of metacognitive abilities but these are "limited in resolution, emerge in context-dependent manners, and seem to be qualitatively different from those of humans." Models may not reliably respond to resource signals in the way a human would respond to a fuel gauge.

**Instruction Adherence at Scale**: System prompts compete with user instructions and retrieved context. As context fills, earlier system prompt instructions (including resource warnings) may be effectively forgotten or deprioritized -- the very phenomenon our plugin aims to mitigate. This creates a paradox: the resource warnings are most needed when context is fullest, but that is also when they are most likely to be ignored.

**Post-training effects on metacognition**: Ma et al. (EMNLP 2025) found that LLMs have intrinsic metacognitive signals detectable in internal activations, but **extracting and utilizing these signals effectively requires specialized frameworks**. Prompting alone may not engage the right metacognitive circuits.

#### Arguments Against Autonomous Self-Regulation

**"Fully Autonomous AI Agents Should Not be Developed"** (Feb 2025, arXiv:2502.02649): While not about resource management specifically, the paper argues that risks increase with autonomy level. An agent that modifies its own thinking effort is a form of self-regulation that raises questions about predictability and oversight. The counterargument: simple threshold-based rules (our adaptive mode) are deterministic and predictable, not open-ended self-modification.

**Trust Paradox**: From our own plugin's hypothesis document -- "Should the model that's running low on context be the one deciding to reduce its own thinking depth? There's a paradox: the degrading model may make worse decisions about when to degrade itself." This is acknowledged in the broader literature as a challenge for any self-regulating system.

#### What Has NOT Been Studied

1. **Real-time context window utilization feedback in coding agents**: No published study gives an LLM coder a percentage-based context meter and measures behavioral adaptation. BATS is the closest analog but targets information-seeking (search/browse) tasks, not code generation/editing.

2. **Feedback granularity comparison**: No study compares different granularities of resource feedback (percentage only vs. burn rate vs. remaining projections vs. all three). BATS uses tool-call counts; TALE uses token budgets; BudgetThinker uses remaining-tokens. Nobody has compared these signal types head-to-head.

3. **Impact on task triage decisions**: No published work examines whether budget signals improve an agent's decision about what to start, defer, or delegate. This is entirely unstudied.

4. **Context compaction interaction**: No study examines how budget-aware behavior interacts with automatic context compaction (like Anthropic's new feature in Opus 4.6). Does the agent's awareness of upcoming compaction change its behavior? Does compaction reset undermine the budget signal's value?

5. **Thinking token eviction and burn rate**: The interaction between thinking token eviction (tokens consumed then discarded between turns) and context utilization metrics has not been formally studied. This is a measurement challenge specific to our plugin.

6. **Long-session behavioral drift under resource pressure**: While "context rot" studies measure accuracy degradation, none measure whether models change their behavioral patterns (tool selection, verbosity, delegation decisions) as context pressure increases -- with or without explicit budget signals.

7. **Cross-task quality degradation under effort reduction**: While CCoT shows math tasks suffer more from reasoning compression in less capable models, there is no systematic study of which coding subtasks (debugging, refactoring, test writing, architecture) degrade most when thinking effort is reduced.

---

## 4. Evidence Quality Assessment

| Angle | Evidence Strength | Type | Confidence |
|-------|-------------------|------|------------|
| Budget-aware prompting reduces tokens | **Strong** | Empirical (multiple papers, multiple models) | High |
| Continuous budget signals > one-shot | **Moderate** | Empirical (2 papers: BudgetThinker, BATS) | Medium-High |
| Token elasticity (too-tight budgets backfire) | **Moderate** | Empirical (1 paper, TALE, but well-documented) | Medium-High |
| Adaptive thinking improves efficiency | **Strong** | Empirical + Product deployment | High |
| Context rot is universal | **Strong** | Empirical (18 models, Chroma study) | High |
| Lost-in-the-middle effect | **Strong** | Empirical (multiple replications) | High |
| Budget signals improve task triage | **None** | No studies found | Unknown |
| Feedback granularity comparison | **None** | No studies found | Unknown |
| Budget awareness in coding workflows | **Weak** | One partial analog (Agent Contracts on LiveCodeBench) | Low |
| Overthinking harms performance | **Moderate-Strong** | Empirical (multiple papers, surveys) | Medium-High |
| Self-monitoring can be counterproductive | **Moderate** | Empirical + Theoretical | Medium |
| Fail-expensively pattern | **Strong** | Empirical (SWE-Effi, multiple agents) | High |

**Overall assessment**: The evidence strongly supports that (a) LLMs can respond to budget signals, (b) continuous signals work better than one-shot, (c) context degrades with length, and (d) adaptive computation improves efficiency. However, the specific application to coding agents with real-time context window feedback is **unstudied territory**. The closest analogs (BATS, Agent Contracts) are encouraging but not directly transferable.

---

## 5. Key Takeaways for the Context Awareness Plugin

### What the evidence supports

1. **The core approach is sound.** Providing real-time resource feedback to LLMs is empirically validated to improve resource efficiency (BATS: 31.3% cost reduction, TALE: 67% token reduction, Agent Contracts: 90% token reduction). The plugin's approach of injecting context awareness on every tool call aligns with BudgetThinker's finding that continuous feedback outperforms one-shot prompts.

2. **The burn rate metric is novel and valuable.** No published work computes a running "burn rate" (%/tool call). SWE-Effi computes cost per resolved issue; BATS tracks remaining tool-call budget; TALE estimates per-problem token budgets. A live burn rate with remaining-call projections is a unique contribution that could be valuable for both the LLM and human operators.

3. **Adaptive effort mode is well-motivated.** The "Reasoning on a Budget" survey and Anthropic's own adaptive thinking feature confirm that matching reasoning effort to task complexity improves efficiency. The plugin's threshold-based approach (medium at 50%, low at 70%) is a simple but defensible heuristic. The evidence suggests this should work for routine operations but may need manual override for complex reasoning tasks.

4. **Compaction interaction is important and unstudied.** Anthropic's Deep Agents trigger summarization at 85% context usage. LangChain's Deep Agents SDK does the same. Our plugin operates in the space before compaction fires, making it complementary. But the interaction between budget-aware behavior and compaction is unexplored.

### What the evidence warns against

1. **Beware token elasticity.** If messages are too alarmist at high context utilization, the model may ignore them or react counterproductively. The evidence suggests that budgets should feel "reasonable" rather than "tight." Consider framing: "You have approximately 25 tool calls remaining at current rate" is more actionable than "WARNING: 80% of context consumed."

2. **Metacognitive overhead is real.** Every token spent on resource awareness instructions is a token not spent on the task. Keep budget signals concise. The Salesforce finding about LLMs degrading after ~8 directives suggests the budget message should be brief and integrated, not a separate lengthy instruction.

3. **Don't assume reliable self-regulation.** LLM metacognition is "limited in resolution" and "context-dependent." Threshold-based rules (adaptive mode) are safer than relying on the model to independently assess and respond to resource pressure. The "trust paradox" noted in our own hypothesis document is a real concern.

4. **Monitor for analysis paralysis.** If the model starts producing longer planning-oriented responses in response to budget pressure (instead of acting more efficiently), the budget signals may be net negative.

### Design recommendations from the literature

1. **Prefer tool-call budgets over token budgets** for the agent-facing signal (per BATS). Humans and LLMs understand "you have 25 tool calls left" more intuitively than "you have 52,000 tokens left."

2. **Implement futility detection** (per SWE-Effi). The "fail expensively" pattern shows agents waste 4x resources on tasks they cannot solve. Budget awareness could help trigger earlier abandonment of unproductive paths.

3. **Consider a "contract" approach** (per Agent Contracts). Define acceptable quality thresholds within resource budgets rather than just monitoring and warning. This is more ambitious but shows stronger results.

4. **Use differential feedback granularity by phase**: Minimal signals early in the session (when resources are abundant), progressively more detailed signals as context pressure increases. This matches the "burn rate increases nonlinearly" observation from context rot research.

---

## 6. Knowledge Gaps

The following questions remain open and would benefit from empirical experimentation, roughly in priority order for the context-awareness plugin project:

### High Priority (directly affects plugin design)

1. **Does our specific feedback format (percentage + burn rate + remaining projections) actually change Claude's behavior?** No published work tests this exact signal combination. We need controlled A/B testing: sessions with and without context awareness, measuring tool call efficiency, task completion, and output quality.

2. **What is the optimal feedback granularity?** Should we show just percentage? Percentage + burn rate? Full projections? The literature suggests more information is better (BATS, BudgetThinker), but the Salesforce finding and metacognitive overhead concern suggest diminishing returns. This needs empirical testing.

3. **Does adaptive effort mode actually save context, or just money?** Our hypothesis document correctly notes the ambiguity: thinking tokens are evicted between turns, so the context savings may be indirect (shorter non-thinking output) rather than direct. This needs the transient-vs-persistent experiment outlined in the hypothesis doc.

4. **How does compaction reset interact with budget awareness?** When Claude Code compacts from 90% to 30-40%, does the agent effectively get a "fresh start"? Does the pre-compaction budget awareness behavior persist or reset? This has implications for whether we should adjust messaging post-compaction.

### Medium Priority (informs future development)

5. **Which coding subtasks degrade most under reduced thinking effort?** Anecdotally, simple file edits don't need deep reasoning while architectural decisions do. But we have no data on where the crossover points are for coding-specific tasks.

6. **Does budget awareness improve task triage?** Can Claude make better decisions about what to start vs. defer vs. delegate to a sub-agent when it knows its remaining capacity? This is entirely unstudied.

7. **What is the "token elasticity" threshold for context window signals?** At what point does "you're running low on context" trigger counterproductive behavior? TALE found this for reasoning token budgets but no one has studied it for context window utilization signals.

### Lower Priority (academic contribution)

8. **Cross-model comparison**: Do different LLMs respond differently to context awareness signals? BATS tested only ReAct-style agents. Agent Contracts tested only GPT-4o. How does Claude specifically respond vs. other frontier models?

9. **Long-session behavioral drift quantification**: How do tool selection patterns, response verbosity, and delegation decisions change over the course of a long coding session -- and does budget awareness produce measurably different drift patterns?

10. **Formal efficiency metric for context-aware coding agents**: A standardized "task completion per context-token" or "effectiveness under context budget" metric for coding agents does not exist. Our burn rate is a step toward one.

---

## Sources

### Core Papers (directly relevant)

- [TALE: Token-Budget-Aware LLM Reasoning](https://arxiv.org/abs/2412.18547) -- Han et al., 2024 (ACL 2025)
- [BudgetThinker: Budget-Aware LLM Reasoning with Control Tokens](https://arxiv.org/abs/2508.17196) -- Wen et al., 2025
- [BATS: Budget-Aware Tool-Use Enables Effective Agent Scaling](https://arxiv.org/abs/2511.17006) -- Google/UCSB/NYU, 2025
- [Agent Contracts: Resource-Bounded Autonomous AI Systems](https://arxiv.org/abs/2601.08815) -- Ye & Tan, 2026 (AAMAS)
- [SelfBudgeter: Adaptive Token Allocation](https://arxiv.org/abs/2505.11274) -- 2025
- [SWE-Effi: Re-Evaluating Agent Effectiveness Under Resource Constraints](https://arxiv.org/abs/2509.09853) -- 2025
- [AgentDiet: Trajectory Reduction for LLM Agents](https://arxiv.org/abs/2509.23586) -- Xiao et al., 2025 (FSE 2026)
- [Reasoning on a Budget: Survey of Adaptive TTC](https://arxiv.org/abs/2507.02076) -- Alomrani et al., 2025
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot) -- Chroma, 2025

### Adaptive Computation

- [Scaling LLM Test-Time Compute Optimally](https://arxiv.org/abs/2408.03314) -- Snell et al., 2024
- [The Art of Scaling Test-Time Compute](https://arxiv.org/abs/2512.02008) -- Dec 2025
- [Concise Chain-of-Thought Prompting](https://arxiv.org/abs/2401.05618) -- Renze & Guven, 2024
- [The Danger of Overthinking: Reasoning-Action Dilemma](https://arxiv.org/abs/2502.08235) -- Feb 2025
- [Stop Overthinking: Survey on Efficient Reasoning](https://github.com/Eclipsess/Awesome-Efficient-Reasoning-LLMs) -- March 2025

### Metacognition and Self-Awareness

- [LLMs Have Intrinsic Meta-Cognition, but Need a Good Lens](https://arxiv.org/abs/2506.08410) -- Ma et al., EMNLP 2025
- [Evidence for Limited Metacognition in LLMs](https://arxiv.org/abs/2509.21545) -- Ackerman et al., 2025
- [Metacognitive Prompting Improves Understanding](https://aclanthology.org/2024.naacl-long.106.pdf) -- NAACL 2024
- [Metacognition and Uncertainty Communication](https://journals.sagepub.com/doi/10.1177/09637214251391158) -- Steyvers & Peters, 2025

### Context Engineering and Management

- [Lost in the Middle: How LLMs Use Long Contexts](https://arxiv.org/abs/2307.03172) -- Liu et al., TACL 2024
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) -- Anthropic, 2025
- [Context Management for Deep Agents](https://blog.langchain.com/context-management-for-deepagents/) -- LangChain, 2025
- [Claude Opus 4.6: Adaptive Thinking and Context Compaction](https://www.anthropic.com/news/claude-opus-4-6) -- Anthropic, March 2026

### Safety and Autonomy

- [Fully Autonomous AI Agents Should Not be Developed](https://arxiv.org/abs/2502.02649) -- Feb 2025
- [Agent Behavioral Contracts: Formal Specification and Runtime Enforcement](https://arxiv.org/abs/2602.22302) -- Bhardwaj, Feb 2026

### Benchmarks and Metrics

- [TheAgentCompany: Benchmarking LLM Agents](https://arxiv.org/abs/2412.14161) -- Dec 2024
- [Controlling Multi-agent LLM System Budget with RL](https://arxiv.org/abs/2511.02755) -- Nov 2025
- [Claude Adaptive Thinking Docs](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)
- [Claude Effort Level Docs](https://platform.claude.com/docs/en/build-with-claude/effort)
