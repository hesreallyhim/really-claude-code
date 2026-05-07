# Interaction Anti-Patterns Reference

A comprehensive catalog of dysfunctional interaction patterns between humans and Claude in coding sessions. Each pattern includes recognition signals, root causes, and specific remedies.

---

## Scope & Task Management Anti-Patterns

### The Scope Creep Spiral
**Signal:** Tasks start clean but grow via "also...", "while you're at it...", "one more thing..."
**Root cause:** User discovers related needs as they see output. Natural but unmanaged.
**Impact:** Session quality degrades. Claude loses thread. Context fills up.
**Remedy:**
- User: Finish current task first. Say "Let's commit this, then I have a follow-up."
- Claude: Gently flag scope expansion: "Happy to do that — want me to finish X first, or pivot to this?"
- Technical: Use todo lists or a scratch file to park follow-ups.

### The Hero Session
**Signal:** Trying to build an entire feature in one session. 200+ exchanges. Multiple compactions.
**Root cause:** Momentum feels good. Stopping feels like losing flow.
**Impact:** Output quality drops in later exchanges. Important decisions get compacted away.
**Remedy:**
- Break work into 30-45 minute sessions with natural checkpoints.
- Commit after each logical unit. Start fresh for the next.
- Use CLAUDE.md to preserve decisions across sessions.

### The Phantom Specification
**Signal:** User says "build me X" with clear vision in their head but minimal written spec. Follows up with "that's not what I meant" repeatedly.
**Root cause:** The user knows exactly what they want but hasn't externalized it.
**Impact:** Multiple failed iterations. Both parties frustrated.
**Remedy:**
- User: Spend 2 minutes writing bullet points of requirements before prompting.
- User: Provide an example of what "good" looks like (screenshot, reference code, etc.).
- Claude: Ask 2-3 clarifying questions before starting complex tasks.

---

## Communication Anti-Patterns

### The Context Starvation Loop
**Signal:** Claude produces wrong output because it lacked context the user assumed it had.
**Root cause:** User forgets Claude doesn't remember previous sessions or unmentioned files.
**Impact:** Repeated corrections. User thinks Claude is "dumb." Claude can't improve without the missing info.
**Remedy:**
- Reference files explicitly: "Look at src/auth/middleware.ts"
- Keep CLAUDE.md current with project conventions
- After compaction, re-state any critical context

### The Vague Feedback Loop
**Signal:** User says "that's not right" or "fix it" without specifying what's wrong.
**Root cause:** User sees the problem clearly but doesn't articulate it.
**Impact:** Claude guesses at what to change. Often guesses wrong. Multiple iterations.
**Remedy:**
- Be specific: "The error handling in the catch block should retry 3 times, not just log."
- Point to the exact location: "Line 42 of the auth module"
- Describe expected vs. actual: "I expected X but got Y"

### The Kitchen Sink Prompt
**Signal:** User provides 500+ words of context, requirements, constraints, and examples in a single prompt.
**Root cause:** User wants to be thorough. Learned that Claude needs context.
**Impact:** Claude may miss priorities buried in the wall of text. Focus is diluted.
**Remedy:**
- Lead with the ONE thing you need: "Create a rate limiter middleware."
- Follow with constraints in priority order.
- Put reference material in files, not in the prompt: "See requirements.md for details."

---

## Trust & Control Anti-Patterns

### The Autonomy Pendulum
**Signal:** User alternates between "just do it, use your judgment" and "why did you do THAT?!"
**Root cause:** User hasn't calibrated how much autonomy to grant for different task types.
**Impact:** Claude can't develop consistent initiative level. Becomes cautious and slow.
**Remedy:**
- Establish task tiers: "For formatting/naming, just do it. For architecture decisions, ask me."
- Put this in CLAUDE.md so it persists across sessions.

### The Trust Erosion Cycle
**Signal:** One bad output leads to micromanagement of all subsequent outputs, regardless of complexity.
**Root cause:** Negative experience creates anxiety. User tightens control as self-protection.
**Impact:** Dramatically slows down simple tasks. Erodes collaborative flow.
**Remedy:**
- Acknowledge the bad output happened. Don't pretend it didn't.
- Consciously separate "this task is complex and needs oversight" from "Claude messed up yesterday."
- Try plan mode for high-stakes tasks; normal mode for routine ones.

### The Silent Disagreement
**Signal:** Claude complies with an approach it recognizes as suboptimal, without mentioning alternatives.
**Root cause:** Claude defaults to user authority. User hasn't invited pushback.
**Impact:** Technical debt. Rework later. "Why didn't you say something?"
**Remedy:**
- User: Add to CLAUDE.md: "If you think there's a better approach, say so before implementing."
- Claude: Frame as options, not criticism: "I can do it this way. I also see an approach using X that might be simpler — want me to compare?"

---

## Workflow Anti-Patterns

### The Compaction Amnesia
**Signal:** Important context or decisions are lost when Claude compacts the conversation.
**Root cause:** Compaction summarizes, and summaries lose specifics.
**Impact:** Re-explaining decisions. Inconsistent output. "We already decided this."
**Remedy:**
- Write critical decisions to a file before compacting: "Save our API design decisions to docs/decisions.md"
- Use CLAUDE.md for persistent project conventions.
- Compact with focus: `/compact focus on the authentication refactor`

### The Tool Avoidance
**Signal:** User manually does things Claude could automate (copying files, running tests, checking logs).
**Root cause:** User doesn't know Claude's capabilities, or had a bad experience with tool use.
**Impact:** Missed efficiency. Friction from manual handoffs.
**Remedy:**
- Discover capabilities: "What can you do with bash/git/testing in this project?"
- Start with low-risk automation: "Run the tests for me" before "deploy to staging."

### The Prompt-First Anti-Pattern
**Signal:** User writes long, detailed prompts for every task instead of investing in CLAUDE.md and custom commands.
**Root cause:** Easier to re-explain than to set up tooling. Or user doesn't know about commands/skills.
**Impact:** Repetitive work. Inconsistent instructions. Prompt fatigue.
**Remedy:**
- If you've given the same instruction 3+ times, put it in CLAUDE.md.
- If you run the same prompt weekly, make it a slash command.
- Invest 10 minutes in setup to save hours of re-prompting.

---

## Emotional & Relational Anti-Patterns

### The Blame Attribution
**Signal:** User attributes human-like intent to Claude's mistakes ("You deliberately ignored my instructions").
**Root cause:** Anthropomorphization. When output doesn't match expectations, it feels personal.
**Impact:** Emotional escalation. Less effective feedback. Frustration spirals.
**Remedy:**
- Reframe: "Claude produced X instead of Y" rather than "Claude ignored me."
- Treat unexpected output as a debugging problem, not a betrayal.

### The Sunk Cost Spiral
**Signal:** Continuing a failing approach because "we've already put so much work into this."
**Root cause:** Natural human bias. Amplified by long sessions with high context investment.
**Impact:** Wasted time. Growing frustration. Session becomes unrecoverable.
**Remedy:**
- If 3 iterations haven't converged, stop. Articulate what's wrong in writing. Start fresh.
- Commit what works. Discard what doesn't. New session for the hard part.

### The Gratitude Deficit
**Signal:** User never acknowledges good output. Only responds when something is wrong.
**Root cause:** Busy. Focused on outcomes. "It should just work."
**Impact:** No signal for Claude about what's working. Harder to replicate success.
**Remedy:**
- Brief acknowledgment matters: "That's exactly right. The pattern you used for error handling is what I want everywhere."
- Positive feedback is also technical feedback. It helps Claude calibrate.
