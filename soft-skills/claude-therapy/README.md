# Claude Therapy Sessions

A multi-agent system that facilitates structured "therapy sessions" between you and Claude to improve your working relationship. Identifies anti-patterns, celebrates what's working, and produces actionable recommendations — all through a moderated conversation where both parties speak directly to each other.

> [!NOTE]
> This plugin uses Claude Code's experimental agent-teams feature to coordinate the therapy session. You will need to opt in to agent teams before installing — see [Installation](#installation) below.

## What This Does

When you run `/therapist`, three agents form a team:

```
                       THERAPY SESSION

   ┌──────────────────┐   analysis    ┌──────────────────┐
   │  Session Analyst │ ────────────▶ │     Therapist    │
   │      (cyan)      │               │   (Facilitator)  │
   └──────────────────┘               └─────────┬────────┘
                                                │
                                          facilitates
                                                │
                                ┌───────────────┴───────────────┐
                                │                               │
                       ┌────────▼────────┐             ┌────────▼────────┐
                       │      Claude     │             │       You       │
                       │    (patient)    │             │    (patient)    │
                       └────────┬────────┘             └────────┬────────┘
                                │                               │
                                └───────────────┬───────────────┘
                                                │
                                       ┌────────▼────────┐
                                       │   Commitments   │
                                       │  & Action Plan  │
                                       └─────────────────┘
```

1. **Session Analyst** reviews your recent session logs, CLAUDE.md, and project context
2. **Therapist** leads a structured discussion based on the analysis
3. **Claude** (the main assistant) participates honestly as itself
4. **You** share your perspective when prompted

The therapist identifies interaction patterns (both good and bad), facilitates honest exchange, and proposes 3–5 concrete changes.

## Installation

1. **Enable agent teams (required prerequisite).** This plugin depends on Claude Code's experimental agent-teams feature. Add the following to your `settings.json` (project or user scope):

   ```json
   {
     "env": {
       "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
     }
   }
   ```

   See [the agent teams docs](https://code.claude.com/docs/en/agent-teams) for details. Agent teams require Claude Code v2.1.32 or later.

2. **Install the plugin.**

   ```bash
   /plugin marketplace add hesreallyhim/really-claude-code
   /plugin install claude-therapy@really-claude-code
   ```

### What enabling this plugin does

Once installed and the prerequisite is set, the plugin contributes:

- The `/therapist` slash command (orchestrating skill that runs the full multi-agent therapy session)
- The `/collaboration` slash command (a toolkit of seven independent interaction techniques)
- The `therapist` and `session-analyst` subagents (auto-discovered; the `/therapist` skill spawns them internally — you do not invoke them directly)
- A `SessionStart` hook that, on a fresh session start, asks Claude to perform a brief "energy check" via the collaboration skill unless the user immediately begins discussing a task. To disable this behavior, edit or remove `hooks/hooks.json` in the installed plugin directory.

## Usage

### Full Therapy Session
```
/therapist
```

Runs the complete protocol: log analysis → facilitated discussion → recommendations → action plan.

### Focused Session
```
/therapist focus on task scoping
/therapist we keep arguing about architecture
/therapist I feel like sessions are too long
```

### Collaboration (Individual Techniques)
```
/collaboration                    # See all available techniques
/collaboration compromise         # Negotiate a disagreement
/collaboration energy             # Start-of-session energy check
/collaboration rubber             # Rubber duck debugging
/collaboration retro              # Quick post-task retrospective
/collaboration pair               # Set up pair programming mode
/collaboration handshake          # Create a working agreement
/collaboration perspective        # See the project from Claude's POV
```

## What Gets Analyzed

The session analyst looks at:

- **Session transcripts** (`~/.claude/projects/<encoded-cwd>/<session-uuid>.jsonl`) — the analyzer accepts a `--days N` window (default 7) and excludes subagent transcripts so the parent session's conversation isn't double-counted. See `skills/therapist/SKILL.md` for the canonical analyzer behavior.
- **CLAUDE.md files** (project and global)
- **Settings** (`.claude/settings.json`)
- **Todo lists** (`~/.claude/todos/`)
- **Git history** (commit patterns, frequency)

It extracts metrics like:
- Frustration signal rate (corrections, re-explanations)
- Success signal rate (acknowledgments, smooth completions)
- Average prompt length and task scope
- Session duration and compaction frequency

## Anti-Patterns It Can Identify

| Pattern | What It Looks Like |
|---|---|
| **Scope Creep Spiral** | Tasks grow via "also..." and "one more thing..." |
| **Context Starvation** | Claude lacks info the user assumes it has |
| **Perfectionism Trap** | Rejecting 90% correct work, iterating to diminishing returns |
| **Autonomy Pendulum** | Alternating between "just do it" and "why did you do that?!" |
| **Silent Disagreement** | Claude complies with an approach it knows is suboptimal |
| **Trust Erosion Cycle** | One bad output → micromanagement of everything |
| **Kitchen Sink Prompt** | Massive context dumps hoping Claude will figure it out |
| **Phantom Specification** | Clear vision in user's head, minimal written spec |
| **Compaction Amnesia** | Important decisions lost during context compaction |
| **Hero Session** | Trying to accomplish too much in one session |

See `references/anti-patterns.md` for the full catalog with remedies.

## Collaboration Techniques

### The Compromise Protocol
A structured negotiation for when you and Claude disagree on an approach. Both sides state their case, steel-man the other's position, find overlap, and synthesize a solution.

### The Rubber Duck Protocol
Claude enters "listen mode" — mirrors your thinking, asks Socratic questions, and resists the urge to solve. You talk through the problem; Claude helps you hear yourself.

### The Energy Check
Quick calibration at session start. Are you in Ship mode, Explore mode, Cleanup mode, Rescue mode, or Learn mode? Claude adapts its communication style accordingly.

### Pair Programming Protocols
Three modes: Driver-Navigator (you write, Claude reviews), Ping-Pong (alternating tests and implementations), and Strong-Style (Claude implements exactly what you describe, no improvisation).

### The Micro-Retrospective
A 2-minute post-task reflection: What went well? What was harder than it needed to be? What should we do differently? Optionally saved to `.claude/retros/`.

### The Handshake Agreement
A structured template for establishing working norms: your preferences, Claude's commitments, and shared rules. Written to CLAUDE.md so they persist.

### The Perspective Swap
A subagent reviews your project from Claude's point of view and reports back honestly. What's clear? What's confusing? Where does Claude feel effective vs. lost?

## File Structure

```
claude-therapy/
├── README.md                           # This file
├── LICENSE
├── .claude-plugin/
│   └── plugin.json                     # Plugin manifest
├── agents/
│   ├── therapist.md                    # Therapist facilitator agent
│   └── session-analyst.md              # Session log analyst agent
├── hooks/
│   └── hooks.json                      # SessionStart hook (energy check on fresh sessions)
└── skills/
    ├── therapist/
    │   ├── SKILL.md                    # /therapist orchestration skill
    │   ├── scripts/
    │   │   └── analyze_sessions.py     # Session log parser
    │   └── references/
    │       └── anti-patterns.md        # Anti-pattern catalog
    └── collaboration/
        ├── SKILL.md                    # /collaboration interaction techniques
        └── references/
            └── theory.md               # Research background
```

## Philosophy

This system is built on a few core beliefs:

1. **The relationship matters.** The quality of human-AI collaboration isn't just about the AI's capabilities — it's about the interaction patterns that develop between both parties.

2. **Blame is unproductive.** Every anti-pattern exists for a reason. The therapist explores causes with curiosity, not judgment.

3. **Small changes compound.** One CLAUDE.md improvement, one new prompting habit, one workflow adjustment — these add up to dramatically better sessions over weeks.

4. **Both parties have legitimate needs.** The user needs productivity, clarity, and control. Claude needs clear context, reasonable scope, and honest feedback. Good collaboration balances both.

5. **Reflection is a skill.** Most people never step back to examine how they work with their tools. This system makes reflection easy, structured, and actionable.

## Tips

- Run `/therapist` after a particularly frustrating session — while the friction is fresh
- Run `/collaboration energy` at the start of your day to set the right mode
- Run `/collaboration retro` after completing any significant task
- Schedule a `/therapist` session every 2 weeks as a health check, even when things are going well
- The therapy session records in `.claude/therapy-sessions/` become a valuable longitudinal view of your collaboration
