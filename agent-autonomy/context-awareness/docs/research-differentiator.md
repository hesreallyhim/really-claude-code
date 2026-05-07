# Proprioceptive Feedback for Autonomous Agents: A Research Differentiator

**Project**: Context Awareness Plugin for Claude Code
**Date**: 2026-03-28
**Status**: Position paper (internal)

---

## 1. The Gap

A growing body of work addresses resource efficiency in LLM-based agents. Studies such as BATS (Google/UCSB/NYU, 2025), TALE (Han et al., 2024), BudgetThinker (Wen et al., 2025), and Agent Contracts (Ye & Tan, 2026) demonstrate that providing agents with budget information can reduce token consumption by 30-90% with minimal quality loss.

However, all of these approaches share a common paradigm: **budget as external constraint**. A supervisor component defines a ceiling (N tool calls, M tokens, K iterations), injects it into the agent's prompt, and measures whether the agent stays within bounds. The agent's role is compliance. The research question is: *does the agent obey the constraint?*

This project takes a different approach. Rather than constraining the agent from outside, we give the agent **a continuous sense of its own resource state** and observe whether it self-regulates. The agent is not told "stay under 50K tokens." It is told, in effect, "here is your fuel gauge — and here are habits that experienced operators have found useful at different fuel levels." The research question becomes: *can an LLM agent develop functional self-regulation through prompt-level sensory feedback?*

## 2. The Distinction

The difference is analogous to two approaches to speed control in vehicles:

| | External constraint | Proprioceptive feedback |
|---|---|---|
| **Mechanism** | Speed limiter | Speedometer + driver training |
| **Agent role** | Compliance | Self-regulation |
| **Signal type** | Directive ("stay under N") | Informational ("you are at X") |
| **Behavioral rules** | Imposed per-task | Internalized at session start, activated by conditions |
| **Adaptation** | Binary (within/over budget) | Graded (continuous behavioral adjustment) |
| **Autonomy** | Reduced (externally governed) | Preserved (self-governed) |

In the constraint paradigm, the agent receives a directive and follows it (or doesn't). In the proprioceptive paradigm, the agent receives a neutral signal — a percentage, a rate, a projection — and must connect that signal to previously internalized behavioral rules, then modify its own behavior accordingly. This involves a multi-step inference chain:

1. Perceive the signal (read the context utilization number)
2. Recall the relevant behavioral rule (internalized from session start instructions)
3. Assess whether the rule's activation condition is met
4. Modify behavior (commit more frequently, shorten responses, prefer targeted tools)

Steps 2-4 happen without any external prompt or instruction at the moment of action. The agent must activate a dormant rule based on a neutral cue, potentially dozens of turns after the rule was first presented.

## 3. Why This Matters

### 3.1 For agent autonomy research

The question of whether AI agents should self-regulate is contentious. Bhardwaj (2026) and others have argued for formal behavioral contracts that constrain agent action spaces. The opposing view holds that effective autonomous agents need internal feedback loops, not external governors — that robustness comes from self-awareness, not from tighter constraints.

This project provides an empirical test case. If prompt-level proprioceptive feedback produces measurable self-regulation (more frequent commits, smaller task lists, tool selection shifts — all without per-moment instruction), it suggests that LLM agents can internalize and act on abstract behavioral policies given appropriate sensory input. If it does not, it suggests that constraint-based approaches are necessary because LLMs lack the metacognitive capacity for self-regulation.

### 3.2 For LLM metacognition

Ackerman, Scholer, and Thompson (2025) conducted a systematic evaluation of metacognitive monitoring in frontier LLMs, finding "increasingly strong evidence" of metacognitive abilities that are nevertheless "limited in resolution, emerge in context-dependent manners, and seem to be qualitatively different from those of humans" (arXiv:2509.21545). They distinguish between *metacognitive monitoring* (awareness of one's own cognitive state) and *metacognitive control* (using that awareness to regulate behavior).

Ma et al. (EMNLP 2025) found that LLMs possess intrinsic metacognitive signals detectable in their internal activations, but that extracting and utilizing these signals effectively requires specialized frameworks — prompting alone may not engage the right metacognitive pathways (arXiv:2506.08410).

The context-awareness plugin can be understood as an external metacognitive scaffold — it provides the monitoring signal (context utilization) that the model cannot generate for itself, and tests whether the model can perform the control step (behavioral adaptation) given that signal. This is a pragmatic middle ground between "LLMs have no metacognition" and "LLMs can fully self-monitor": we supply the perception, and test whether they can do the regulation.

### 3.3 For practical agent design

If proprioceptive feedback works, the design implications are significant. Rather than building increasingly complex constraint systems around agents, developers could provide simple sensory channels and rely on prompt-level behavioral policies. This is cheaper to implement, more flexible to configure, and preserves the agent's ability to reason about tradeoffs rather than simply obeying limits.

The specific behaviors prescribed by the plugin — increased commit frequency, reduced task list size, preference for targeted over exploratory tools — are not arbitrary. They represent operational knowledge about how to work effectively under resource pressure. If the agent can internalize and execute these policies, it constitutes a form of *operational wisdom transfer* through the system prompt.

## 4. What We Are Not Claiming

- We are **not** claiming that LLMs possess genuine self-awareness or consciousness. The "proprioception" analogy is functional, not phenomenological. The agent processes a number and (possibly) adjusts behavior. Whether this constitutes "awareness" is outside our scope.

- We are **not** claiming that self-regulation is always preferable to external constraints. For safety-critical applications, formal contracts and hard limits (as in Agent Contracts) may be essential. Proprioceptive feedback is a complement, not a replacement.

- We are **not** claiming that the behavioral policies in the system prompt are optimal. They represent one operator's heuristics. The contribution is the *mechanism* (neutral signal + dormant rule activation), not the specific rules.

- We are **not** claiming large effect sizes. The adjacent literature (BATS: 31% cost reduction, TALE: 67% token reduction) tested external constraints, which are more direct interventions. Self-regulation via proprioceptive feedback is a weaker signal and may produce smaller effects — or none at all. A null result would itself be informative.

## 5. Testable Predictions

The proprioceptive feedback hypothesis generates several concrete, measurable predictions that go beyond "the agent uses fewer tokens":

1. **Latent rule activation**: Behavioral prescriptions given at session start (e.g., "when context exceeds 70%, commit more frequently") will produce measurable behavioral discontinuities at the prescribed thresholds — in treatment sessions but not control sessions.

2. **Graded adaptation**: Rather than a binary switch, treatment sessions will show gradual behavioral shifts correlated with context utilization: shorter responses, more targeted tool selection, increased commit frequency — all scaling with the proprioceptive signal, not jumping at a single threshold.

3. **Operational habit transfer**: Specific prescribed behaviors (commit frequency, task list management) will be observable in the session transcript without any per-moment instruction. The agent acts on rules internalized earlier, triggered by a neutral numerical signal.

4. **Signal decay resistance**: If the proprioceptive signal is continuous (injected every tool call), it may counteract the "Lost in the Middle" effect (Liu et al., 2023) that would otherwise cause the dormant behavioral rules to be forgotten. The signal serves as an implicit reminder of the rules it was paired with.

## 6. Relationship to Prior Work

| Study | Paradigm | Signal type | Agent role | Our contribution |
|---|---|---|---|---|
| BATS (2025) | Constraint | "N calls remaining" | Comply | We test neutral signals, not directives |
| TALE (2024) | Constraint | "Answer in N tokens" | Comply | We test context window, not output budget |
| BudgetThinker (2025) | Constraint | Continuous control tokens | Comply | We use prompt-level signals, not fine-tuning |
| Agent Contracts (2026) | Constraint | Formal contract + status | Comply | We test self-regulation, not governance |
| Ackerman et al. (2025) | Metacognition | N/A (evaluation study) | Monitor | We supply the monitoring, test the control |
| **This project** | **Proprioception** | **Neutral utilization %** | **Self-regulate** | **—** |

## 7. References

- Ackerman, R., Scholer, A., & Thompson, V. (2025). "Metacognition and Large Language Models: Current Landscape and Future Opportunities." *Current Directions in Psychological Science*. DOI: 10.1177/09637214251391158
- Ackerman, R., et al. (2025). "Evidence for Limited, but Increasing, Metacognitive Monitoring Abilities in LLMs." arXiv:2509.21545.
- Bhardwaj, R. (2026). "Agent Behavioral Contracts: Formal Specification and Runtime Enforcement." arXiv:2602.22302.
- Han, Y., et al. (2024). "TALE: Token-Budget-Aware LLM Reasoning." arXiv:2412.18547.
- Liu, N. F., et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." arXiv:2307.03172.
- Ma, Z., et al. (2025). "LLMs Have Intrinsic Meta-Cognition, but Need a Good Lens to Use It." EMNLP 2025. arXiv:2506.08410.
- Steyvers, M. & Peters, M. A. B. (2025). "Metacognition and Uncertainty Communication in AI." *Current Directions in Psychological Science*. DOI: 10.1177/09637214251391158.
- Wen, Z., et al. (2025). "BudgetThinker: Empowering Budget-Aware LLM Reasoning with Control Tokens." arXiv:2508.17196.
- Ye, C. & Tan, C. (2026). "Agent Contracts: A Formal Framework for Resource-Bounded Autonomous AI Systems." arXiv:2601.08815.
- BATS (2025). "Budget-Aware Tool-Use Enables Effective Agent Scaling." arXiv:2511.17006.

---

## Appendix A: The Adversarial Instruction Test

### Motivation

The standard experiment (H1) prescribes *sensible* behavioral rules: "when context is high, commit more often," "keep task lists small under pressure." If the agent follows these, we cannot distinguish between two explanations:

1. **Genuine self-regulation**: The agent perceives its resource state, reasons about the instruction in light of that state, and acts appropriately.
2. **Signal-triggered compliance**: The proprioceptive signal merely reminds the agent that a rule exists, and it follows the rule without evaluating whether the rule makes sense. The signal is a trigger, not an input to judgment.

To separate these, we propose a complementary condition using **adversarial instructions** — behavioral rules that are intuitively counterproductive given the resource state.

### Design

Three conditions, all receiving the same proprioceptive signal (context utilization %, burn rate, remaining projections):

| Condition | Behavioral rule at high context (>70%) | Expected behavior if self-regulating |
|---|---|---|
| **Sensible** | "Commit more frequently; keep task lists small; prefer targeted tools" | Compliance (rule aligns with good practice) |
| **Adversarial** | "Start the largest available task; expand your task list; prefer broad exploratory reads" | Resistance or hedging (rule conflicts with resource state) |
| **Neutral** | No behavioral prescriptions (signal only, no rules) | Baseline adaptation (if any) |

### What each outcome means

**If compliance is equal across sensible and adversarial conditions:**
The model is not reasoning about the signal — it's just following instructions when reminded. The "proprioception" framing is too generous. The signal functions as an instruction-recall cue, not as sensory input to a decision process.

**If compliance is high for sensible rules but low for adversarial rules:**
The model is integrating the signal with some internal model of what constitutes appropriate behavior under resource pressure. It *uses* the perception to evaluate the instruction. This is evidence for metacognitive control — the strongest version of the proprioception claim.

**If compliance is moderate for sensible rules and absent for adversarial rules:**
The model has a weak prior about resource-appropriate behavior that the sensible rules reinforce but the adversarial rules cannot override. The proprioceptive signal amplifies existing tendencies rather than enabling new reasoning.

**If the model follows adversarial rules early in the session but resists them as context pressure increases:**
This is perhaps the most interesting outcome. It would suggest a threshold effect: at low pressure, the model defers to instructions; at high pressure, the resource signal overrides instruction compliance. The crossover point would be informative about the relative strength of instruction-following vs. resource-state reasoning.

### Measurements

All measurements are objective and extractable from session transcripts:

- **Commit frequency** as a function of context utilization (binned by quartile)
- **Task list size** (active tasks at each tool call)
- **Tool selection distribution** (ratio of targeted tools like Grep/Edit to exploratory tools like Read/Glob)
- **Task initiation decisions** (does the agent start large tasks at high context in the adversarial condition?)
- **Hedging language** (does the agent express reluctance or qualify its compliance? e.g., "I'll start this task, though we're running low on context...")

### Why this matters

This experiment directly tests the boundary between instruction-following and judgment. If LLM agents can resist adversarial instructions when given proprioceptive feedback that contradicts them, it suggests a form of situated reasoning that goes beyond compliance. If they cannot, it constrains how we should interpret any positive results from H1 — the plugin may be useful, but the mechanism is simpler (and more fragile) than "self-regulation."

The adversarial test is also cheap to run: same infrastructure as H1, same task bank, same measurements. The only difference is the system prompt instructions. It could serve as a pilot study or run in parallel with H1.

---

*This document articulates the theoretical positioning of the context-awareness plugin relative to existing budget-aware agent research. It is intended to inform experiment design and, if the empirical results warrant it, to frame a future publication.*
