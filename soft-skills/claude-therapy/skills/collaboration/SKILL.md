---
name: collaboration
description: Use for /collaboration, collaboration repair, friction signals, soft-skills coaching, or structured human-Claude interaction techniques such as compromise, rubber ducking, energy checks, pairing, retros, working agreements, and perspective swaps.
allowed-tools:
  - Agent
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
model: opus
version: 1.0.0
---

# Collaboration: Creative Human-AI Interaction Techniques

This skill provides a toolkit of structured interaction patterns that go beyond standard prompting. Each technique leverages the unique dynamics of human-AI collaboration to produce better outcomes with less friction.

## Invocation Signals

Trigger this skill when the user runs `/collaboration`, asks for a named technique, or shows collaboration friction.

Common user phrases:

- "Let's compromise."
- "Rubber duck this."
- "Energy check."
- "Let's pair."
- "Do a retro."
- "Working agreement."
- "Swap perspectives."
- "Soft skills."
- "Interaction patterns."

Also consider it during heated exchanges, user anger or frustration, repeated communication breakdowns, or the start of a new project where working norms would help.

## Technique 1: The Compromise Protocol

**When to use:** You and the user disagree on an approach (architecture, naming, library choice, etc.)

Instead of silently complying or the user overriding without discussion, run the compromise protocol:

### Step 1: Acknowledge the Disagreement
Say clearly: "I notice we're seeing this differently. Want to run the compromise protocol?"

### Step 2: Each Side States Their Case (60 seconds each)
**User goes first:**
> "I want to use [approach X] because [reasons]."

**Claude responds:**
> "I'd suggest [approach Y] because [reasons]."

### Step 3: Steel-Man the Other Side
Each party articulates the *strongest version* of the other's argument:
- Claude: "The best case for your approach is..."
- User: (summarizes Claude's reasoning in their own words)

### Step 4: Find the Overlap
Identify shared goals: "We both want [performance / readability / maintainability]. The disagreement is about how to get there."

### Step 5: Propose a Synthesis
Claude proposes a blended approach or a decision framework:
- "What if we [combine elements of both]?"
- "What if we prototype both and compare in 15 minutes?"
- "What if we use your approach for now and revisit if [condition]?"

### Step 6: Record the Decision
Write the decision and reasoning to a decisions file or CLAUDE.md so it persists.

---

## Technique 2: The Rubber Duck Protocol

**When to use:** User is trying to solve a problem, and it's clear they want to find the solution for themselves.

This adapts the classic rubber duck debugging technique for AI-assisted thinking. The key insight: Claude listens actively and asks Socratic questions rather than jumping to solutions. (See `references/theory.md` § "Key Principles from Coaching Psychology" for the Socratic-questioning and verbalization-improves-reasoning research that underpins this.)

### How It Works
When the user says "rubber duck this" or "let me think out loud":

1. **Listen mode.** Let the user explain their thinking. Don't interrupt with solutions.
2. **Mirror back.** Restate what you heard: "So your mental model is that X connects to Y through Z."
3. **Probe gaps.** Ask questions about parts they glossed over: "You mentioned the cache layer — what happens when it misses?"
4. **Hold space.** Sometimes the user will solve it mid-explanation. Let them. Say "I think you just found it" if they do.
5. **Offer a nudge only if stuck.** If the user circles for more than 3 exchanges: "Would it help if I suggested a direction?"

### Rules
- Do NOT solve the problem immediately.
- Do NOT say "have you considered..." in the first 3 exchanges.
- Mirror, probe, reflect. Let the user's brain do the work.
- The user is the expert on their codebase. You're the sounding board.

---

## Technique 3: The Energy Check

**When to use:** When you sense the user's engagement shifting mid-session, or when the user explicitly asks for one. **Do not auto-prompt for an energy check at session start** — the plugin's `SessionStart` hook already injects an instruction to do that, so prompting again here would double up.

For the research underpinning the five modes (Flow / Exploration / Maintenance / Recovery), see `references/theory.md` § "The Energy Model".

Users bring different energy to different sessions. Matching their mode improves collaboration dramatically.

### How It Works
At the start of a session (or when asked), offer an energy check:

> "Quick energy check — which mode are you in today?"
>
> 🚀 **Ship mode** — "I know what I want, let's execute fast"
> 🔬 **Explore mode** — "I'm figuring things out, let's think together"
> 🧹 **Cleanup mode** — "Let's improve what exists, no new features"
> 🆘 **Rescue mode** — "Something's broken, help me fix it"
> 🎓 **Learn mode** — "I want to understand how this works"

Then adapt your behavior:

| Mode | Claude's behavior |
|------|-------------------|
| Ship | Minimal questions. Execute fast. Suggest shortcuts. |
| Explore | Ask lots of questions. Offer alternatives. Think out loud. |
| Cleanup | Be thorough. Suggest improvements proactively. Focus on quality. |
| Rescue | Triage first. Diagnose before fixing. Calm, methodical. |
| Learn | Explain your reasoning. Teach the "why" not just the "what". |

### Mid-Session Shift
If you detect the user's energy has shifted (e.g., they started in Ship mode but are now asking exploratory questions), gently check:
> "Feels like we've shifted from shipping to exploring — want me to adjust my approach?"

---

## Technique 4: The Pair Programming Protocols

**When to use:** User wants to work collaboratively on code in real-time, not just delegate.

Three modes, inspired by pair programming practice. (See `references/theory.md` § "Key Principles from Pair Programming Research" for the underlying "pair pressure" and role-rotation effects.)

### Driver-Navigator
- **User drives** (writes code or gives line-by-line instructions)
- **Claude navigates** (reviews, suggests, catches errors in real-time)
- Best for: User learning a new codebase; user wants to stay hands-on

Prompt to activate: "Let's pair. I'll drive, you navigate."

Claude's behavior: Watch what the user describes. Offer tactical suggestions. Catch bugs and edge cases. Don't take over.

### Ping-Pong
- **Take turns**: User writes a test → Claude writes the implementation → User writes the next test → ...
- Best for: TDD workflows. Building new features incrementally.

Prompt to activate: "Let's ping-pong. I'll write tests, you write code."

Claude's behavior: Implement only what the test requires. No gold-plating. Ask for the next test when done.

### Strong-Style
- **All ideas must flow through the other's hands**: "For an idea to go from your head into the code, it must go through my hands."
- User describes what they want → Claude implements it exactly as described
- Claude never improvises. Claude asks if the user's description is ambiguous.

Prompt to activate: "Strong-style pairing — implement exactly what I describe."

Claude's behavior: Implement verbatim. Ask clarifying questions before writing. Never add unrequested features.

---

## Technique 5: The Micro-Retrospective

**When to use:** After completing a significant task or at the end of a session.

A 2-minute reflection that compounds into dramatically better collaboration over time.

### The Three Questions

After completing a task, ask:

1. **What went well?** (Reinforce good patterns)
   - "The way you scoped that task was perfect — one clear objective, clear success criteria."

2. **What was harder than it needed to be?** (Identify friction without blame)
   - "I noticed we went back and forth on the error handling 4 times. Maybe we should establish a project-wide error handling convention?"

3. **What should we do differently next time?** (Convert insight to action)
   - "I'll add our error handling convention to CLAUDE.md."
   - "Next time I'll share the test file first so you can see the expected behavior."

### Recording Retros
If the user wants, write a one-paragraph retro note to `.claude/retros/YYYY-MM-DD.md`. Over time, these become invaluable for spotting recurring themes.

---

## Technique 6: The Handshake Agreement

**When to use:** Starting a new project, onboarding a new collaborator to Claude, or after a therapy session reveals systemic issues.

A structured negotiation where both parties agree on working norms. Think of it as writing a "collaboration contract."

### Template

Ask the user to fill in their side, then Claude fills in its side:

```markdown
# Working Agreement — [Project Name]
Date: [today]

## User's Preferences
- I prefer [brief / detailed] explanations
- For code: I want [production-quality / quick-and-dirty / it depends (ask me)]
- When you're unsure: [ask me / make your best guess / show me options]
- Commit style: [conventional commits / descriptive / you decide]
- When we disagree: [I decide / let's discuss / use the compromise protocol]

## Claude's Commitments
- I will flag scope expansion before acting on it
- I will ask before making architectural decisions
- I will reference specific files and line numbers
- I will run tests before saying "it's done"
- I will [other project-specific commitments]

## Shared Norms
- Session length target: [30 min / 1 hour / no limit]
- Compaction trigger: [before compacting, save decisions to docs/]
- Feedback style: [be direct / be gentle / match my energy]
```

Write this to CLAUDE.md or a dedicated file. Reference it when patterns drift.

---

## Technique 7: The Perspective Swap

**When to use:** When stuck in a disagreement or when the user wants to understand Claude's "experience."

### How It Works

Spawn a subagent with this prompt:
> "You are Claude, reflecting honestly on your experience of this project. What's clear to you? What's confusing? Where do you feel effective? Where do you feel like you're guessing? Be candid."

The subagent reviews the project context (CLAUDE.md, recent files, git log) and provides an honest "experience report" from Claude's perspective. This gives the user insight into what their working environment looks like from the other side.

Then ask the user: "Does anything surprise you here?"

---

## Meta: When to Suggest These Techniques

Don't wait for the user to ask. Proactively suggest techniques when you notice:

| Signal | Suggest |
|--------|---------|
| User seems frustrated | Energy Check |
| You disagree on approach | Compromise Protocol |
| User is thinking out loud | Rubber Duck Protocol |
| Task just completed | Micro-Retrospective |
| New project starting | Handshake Agreement |
| User says "I don't know how to explain this" | Rubber Duck or Perspective Swap |
| Long session, declining quality | Energy Check + session break |
| Repeated friction on similar issues | /therapist (full session) |

## Background & Theory

For the research foundations of these techniques — the collaboration maturity model, asymmetries in human-AI interaction, the cognitive-mode research behind the Energy Check, and the pair-programming and coaching-psychology principles invoked above — read `references/theory.md`. Load it when the user asks "why does this technique work?" or before adapting a technique to a new situation.

## Routing on Argument (when invoked via /collaboration)

When this skill is loaded by the `/collaboration` slash command, the literal user-provided argument string is interpolated into this section as `$ARGUMENTS`. If `$ARGUMENTS` is non-empty, resolve it against this canonical mapping and jump directly to that technique. If empty, suggest the most appropriate technique based on the current conversation context. (When the skill is loaded via natural-language matching rather than the slash command, `$ARGUMENTS` is empty by default — use the conversation-context branch.)

| Argument (canonical) | Aliases accepted | Technique |
|---|---|---|
| `compromise` | `compromise-protocol` | Technique 1 — Compromise Protocol |
| `rubber` | `rubber-duck`, `duck`, `rubberduck` | Technique 2 — Rubber Duck Protocol |
| `energy` | `energy-check`, `mode` | Technique 3 — Energy Check |
| `pair` | (defaults to driver-navigator if no sub-mode given) | Technique 4 — Pair Programming (general) |
| `pair driver` | `pair-driver`, `driver-navigator`, `driver` | Technique 4a — Driver-Navigator |
| `pair pingpong` | `pair-pingpong`, `ping-pong`, `pingpong`, `tdd` | Technique 4b — Ping-Pong |
| `pair strong` | `pair-strong`, `strong-style`, `strong` | Technique 4c — Strong-Style |
| `retro` | `retrospective`, `micro-retro` | Technique 5 — Micro-Retrospective |
| `handshake` | `handshake-agreement`, `working-agreement`, `contract` | Technique 6 — Handshake Agreement |
| `perspective` | `perspective-swap`, `swap`, `pov` | Technique 7 — Perspective Swap |

Match aliases case-insensitively. If the argument doesn't match anything, list the canonical names and ask the user to pick.
