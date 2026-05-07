# Hypothesis: Autonomous Thinking Effort Control

## Date: 2026-03-28

## Premise

Claude's `effortLevel` setting (low/medium/high) directly affects how much
context budget each turn consumes. If Claude could autonomously adjust this
setting, it could extend session longevity by downshifting thinking effort
as context pressure increases.

## Observations

### Baseline: effort = high

| Metric | Value | Turn |
|--------|-------|------|
| Burn rate | ~1.00%/tool | early session |
| Remaining | ~66 tool calls | at 34% used |

### After switch: effort = low

| Metric | Value | Turn |
|--------|-------|------|
| Burn rate | ~0.83%/tool | transitional (blended avg) |
| Remaining | ~78 tool calls | at 35% used |
| Burn rate | ~0.71%/tool | settling |
| Remaining | ~91 tool calls | at 35% used |

### Trend

The burn rate dropped from ~1.00 to ~0.71 %/tool after switching from high
to low effort — a ~29% reduction. The projected remaining tool calls increased
from ~66 to ~91 (~38% improvement). Note: these are blended session averages,
so the true per-tool cost at low effort is likely even lower than 0.71 (the
average still includes the earlier high-effort tool calls).

### Continued: effort switched back to high (mid-session, via Claude edit)

Claude edited `settings.json` to set `effortLevel` back to `"high"` mid-turn.

| Metric | Value | Turn |
|--------|-------|------|
| Burn rate | ~0.53%/tool | continued settling (blended) |
| Remaining | ~115 tool calls | at 39% used |
| Burn rate | ~0.53%/tool | next turn |
| Remaining | ~114 tool calls | at 40% used |

The rate continued to drop even after switching back to high, likely because
the blended average still reflects the many low-effort tool calls. Need more
turns at high effort to see the average climb back up.

**Key observation**: Claude can edit `settings.json` mid-session and the change
appears to take effect. This confirms the mechanism is viable for autonomous
control.

## Effort Mode Design (decided 2026-03-28)

Three modes, stored as `effort_mode` in the per-session tracking file:

| Mode | Value | Behavior |
|------|-------|----------|
| Off | `"off"` | No autonomous adjustment. Default. |
| Adaptive | `"adaptive"` | Auto-downshift effort based on context thresholds (e.g., medium at 60%, low at 80%). |
| Plan Mode | `"planMode"` | High effort for planning/reasoning, low for execution. Borrows the familiar `planMode` concept from Claude Code. |

Toggled via `/autonomous-mode` slash command (cycles off → adaptive → planMode → off).

## Critical Finding: Thinking Tokens and Context Eviction

From the Anthropic API docs (noted 2026-03-28):

> Previous thinking blocks are automatically stripped from the context window
> calculation by the Claude API and are not part of the conversation history
> that the model "sees" for subsequent turns, preserving token capacity for
> actual conversation content.

This means:

1. **Thinking tokens spike during the current turn** but are **evicted before
   the next turn**. They do NOT accumulate in the context window.
2. **Thinking tokens still cost money and count toward rate limits.**
3. **The context window is primarily consumed by**: user messages, tool
   call inputs/outputs, and non-thinking assistant output.

### Implications for the burn rate data

The ~29% burn rate reduction we observed when switching from high to low
effort could be caused by:

- **(a) Transient measurement**: The statusline may sample `used_percentage`
  while current-turn thinking is still counted, capturing a momentary spike
  that would be evicted before the next turn.
- **(b) Indirect effect**: Higher thinking effort may produce longer, more
  detailed non-thinking responses, which DO persist in context. Lower effort
  → terser output → less persistent context consumption.
- **(c) Measurement artifact**: The blended average smooths over multiple
  effects, making it hard to isolate the cause.

### What this changes

- **Adaptive mode still has value**, but the primary benefit may be **cost
  and rate limit savings** rather than context space savings.
- **The indirect effect (b) is likely real** — lower effort tends to produce
  shorter reasoning and more concise output, which genuinely saves context.
- **We should not overstate** the context-saving benefit until we can
  isolate the persistent vs transient components.
- **A useful experiment**: compare the `used_percentage` at the START of a
  turn (UserPromptSubmit, after previous thinking is evicted) vs end of
  turn (PostToolUse). The difference would show the transient spike.

### Note on Claude Code vs raw API

Claude Code may handle thinking eviction differently from the raw API. The
above is from the API docs. Claude Code's context management (compaction,
statusline reporting) may or may not align exactly. This needs verification.

## Open Questions

1. **Is `settings.json` the right mechanism?** Mutating a global config file
   has side effects (persists across sessions). A per-session or per-turn
   override mechanism would be preferable if one exists. The hook should
   restore the original effort level on session end if it changed it.
   **Update**: SessionEnd hook now restores `original_effort`.

2. **Trust and autonomy.** Should the model that's running low on context
   be the one deciding to reduce its own thinking depth? There's a paradox:
   the degrading model may make worse decisions about when to degrade itself.
   Counterargument: a simple threshold rule (e.g., "drop to medium at 60%,
   low at 80%") doesn't require nuanced judgment.

3. **Quality impact.** What tasks suffer meaningfully from lower thinking
   effort? Simple edits and file reads likely don't need high thinking.
   Complex architectural decisions or debugging likely do. The planMode
   approach addresses this by keeping high effort for planning only.

4. **planMode detection.** How does Claude know it's in a "planning" vs
   "execution" phase? Options: explicit user signal, heuristic based on
   tool call patterns, or Claude self-declares phase transitions.

5. **Does thinking eviction apply in Claude Code?** The API docs describe
   eviction behavior for the raw API. Need to confirm whether Claude Code's
   context management (statusline `used_percentage`, compaction triggers)
   accounts for evicted thinking tokens or reports gross usage.

## Next Steps

- [x] Confirm settings.json changes take effect mid-session
- [x] Design the three-mode system (off / adaptive / planMode)
- [x] Add effort_mode to tracking file and /autonomous-mode command
- [x] Implement adaptive threshold logic in the hook
- [x] Add SessionEnd hook to restore original effort level
- [ ] **Isolate transient vs persistent burn rate** — compare UserPromptSubmit
      percentage (post-eviction) with PostToolUse percentage (mid-turn) to
      measure the thinking token spike
- [ ] Collect more data points across sessions to confirm burn rate
      differential between effort levels
- [ ] Implement planMode phase detection
- [ ] Investigate whether per-session effort overrides exist in Claude Code
- [ ] Verify whether Claude Code's used_percentage includes evicted thinking
