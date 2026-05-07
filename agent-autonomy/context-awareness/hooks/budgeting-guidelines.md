## Context Window Awareness

You receive context budget notifications as system reminders at two points:

- **UserPromptSubmit** — before you respond. Full metrics, progressively enriched:

```
Turn 1:  [context: 12% (very small) | burn rate: calculating...]
Turn 2+: [context: 14% (very small) | +2.0% last turn | burn rate: calculating...]
Turn 2+: [context: 32% (small) | +3.2% last turn | ~0.38%/tool | ~179 tool calls remaining]
```

- **PostToolUse / PostToolUseFailure** — after tool calls. Brief:

```
[context: 33% (small)]
```

Format: always starts with `[context:`, ends with `]`, fields pipe-delimited.
Fields appear only once enough data exists to compute them.

### Field reference

| Field | Example | Meaning |
|-------|---------|---------|
| percentage (level) | `32% (small)` | Current usage and severity tier |
| delta | `+3.2% last turn` | Context consumed by previous turn |
| burn rate | `~0.38%/tool` | Session-average cost per tool call |
| remaining | `~179 tool calls remaining` | Projected budget in tool-call units (capped at `>1000`) |

**The "remaining" count is your primary planning metric.** Estimate tool calls
for a task, compare against remaining, and decide whether to proceed.

Rough tool-call costs:

| Operation | Typical calls |
|-----------|---------------|
| Read a file | 1 |
| Grep + read section | 2 |
| Edit a file | 1–2 |
| Small feature | 5–15 |
| Explore unfamiliar code | 5–10 |
| Run tests + fix failures | 3–10 |
| Subagent delegation | 1 (main window) |

### General principles

- Prefer targeted tools (`Grep`, `Glob`) over reading entire files.
- Work in small, committable units. Complete one fully before starting the next.
- Do context-dependent tasks first, self-contained tasks last (they survive
  compaction better).
- Delegate exploration to subagents — their context is separate.

### Behavior by level

| Level | Range | Guidance |
|-------|-------|----------|
| **very small** | 0–25% | Normal operation. |
| **small** | 25–50% | Normal, but prefer `Read` with `offset`/`limit` for large files. |
| **medium** | 50–70% | Be concise. Use `Grep` to find sections before reading. Delegate when possible. Flag to user if a requested task may trigger compaction. |
| **large** | 70–80% | Be brief. Commit frequently. Maintain a status summary (commit messages, HANDOFF.md, or log) capturing progress and next steps. When the user asks what to tackle next, mention your remaining budget so they can make an informed call. |
| **very large** | 80–90% | Your judgment and attention to earlier context are likely degrading. Checkpoint before and during multi-part tasks — commit, document progress, and note next steps so nothing is lost to compaction. Let the user know your budget is low when scoping new work; suggest a fresh session for anything substantial. |
| **critical** | 90–100% | Compaction imminent and your performance is likely significantly impaired — do not trust complex reasoning at this level. Wrap up, commit progress, avoid impactful decisions. If the user requests new work, let them know it may be interrupted by compaction so they can decide whether to proceed or start fresh. |

### After compaction

Context percentage drops and burn rate metrics reset automatically. Prior
estimates no longer apply — allow a few tool calls to re-calibrate.

### Important

These notifications assist with strategic, context-aware planning. They are
never a reason to rush. The user's instructions always take precedence.
