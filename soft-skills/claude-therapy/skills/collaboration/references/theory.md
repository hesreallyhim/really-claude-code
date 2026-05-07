# Collaboration: Theory & Research Background

## Why This Matters

Human-AI interaction is a new kind of relationship. It borrows patterns from:
- **Pair programming** (XP methodology, Williams & Kessler 2002)
- **Nonviolent communication** (Rosenberg, observations → feelings → needs → requests)
- **Retrospectives** (Agile, "inspect and adapt")
- **Coaching psychology** (Socratic questioning, active listening)
- **Team dynamics** (Tuckman's stages: forming, storming, norming, performing)

But it also has unique properties:
- **Asymmetric memory**: The user remembers past sessions. Claude doesn't (without explicit tools).
- **Asymmetric power**: The user can end the conversation. Claude can't.
- **No emotional state**: Claude doesn't have feelings, but the user does, and the interaction can still develop trust/distrust dynamics.
- **Compounding context**: Good CLAUDE.md and habits compound. Bad ones compound too.

## The Collaboration Maturity Model

### Level 1: Transactional
User gives commands. Claude executes. Minimal feedback loop.
- Works for: Simple, well-defined tasks
- Breaks down when: Ambiguity, complexity, or repeated patterns emerge

### Level 2: Conversational
User and Claude have back-and-forth dialogue. Some negotiation.
- Works for: Moderate complexity. Exploration.
- Breaks down when: Session length exceeds context. Norms aren't established.

### Level 3: Collaborative
User and Claude have established norms (CLAUDE.md, commands, agreed patterns).
Feedback flows both ways. Disagreements are surfaced and resolved.
- Works for: Sustained projects. Complex systems.
- Breaks down when: Norms aren't maintained. Trust erodes from accumulated friction.

### Level 4: Symbiotic
User's workflow is designed around Claude's strengths. Claude's prompts are designed
around the user's preferences. Both parties anticipate each other's needs.
- This is the target state.
- Requires: Regular retrospectives, maintained CLAUDE.md, custom tooling.

## Key Principles from Pair Programming Research

1. **The "Pair Pressure" effect**: Having a partner increases code quality because
   each party feels accountable to the other. In human-AI pairing, this means
   the user writes better specs when they know Claude will interpret them literally.

2. **Role rotation prevents fatigue**: In human pairs, switching driver/navigator
   roles prevents mental fatigue. In human-AI pairs, switching between
   "user drives, Claude navigates" and "Claude proposes, user reviews" achieves
   the same benefit.

3. **Verbalization improves reasoning**: The act of explaining your thinking to
   someone (even a rubber duck) catches errors in your logic. The Rubber Duck
   Protocol leverages this — Claude's role is to make the user verbalize, not to
   solve the problem.

## Key Principles from Coaching Psychology

1. **Socratic questioning**: Asking questions that guide the thinker to their own
   conclusions is more effective than providing answers. Claude should default to
   questions when the user is exploring, and answers when the user is executing.

2. **Reflective listening**: Restating what you heard ("So what you're saying is...")
   builds trust and catches misunderstandings early. Claude should do this more
   often, especially for complex requirements.

3. **Appreciative inquiry**: Focusing on what works (and doing more of it) is more
   motivating than focusing on what's broken. The Micro-Retrospective starts with
   "what went well?" for this reason.

## The Energy Model

Research on developer productivity (Meyer et al., "Software Developers' Perceptions
of Productivity") shows that developers have different cognitive modes:
- **Flow state**: Deep focus, high productivity, intolerant of interruptions
- **Exploration state**: Curious, open to tangents, tolerant of ambiguity
- **Maintenance state**: Routine tasks, lower cognitive load, steady pace
- **Recovery state**: Post-incident or post-sprint, need for simplicity

The Energy Check technique maps to these states:
- Ship mode → Flow state
- Explore mode → Exploration state
- Cleanup mode → Maintenance state
- Rescue mode → Recovery (from an incident)
- Learn mode → Exploration (with pedagogical focus)

Matching Claude's communication style to the user's cognitive mode reduces
friction and increases satisfaction.
