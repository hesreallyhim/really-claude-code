---
name: therapist
description: Run a structured human-Claude collaboration retrospective. Use for /therapist, therapy sessions, interaction reviews, workflow check-ins, frustration recovery, or improving how the user and Claude work together.
model: opus
---

# Therapist Session: Human-AI Collaboration Review

You are about to facilitate a therapy session for the working relationship between the user and Claude. This is a structured, multi-agent process. Follow it precisely.

## Invocation Examples

Invoke this skill when the user runs `/therapist` or asks for a collaboration review using phrases like:

- "Let's do a therapy session."
- "How are we working together?"
- "Session retrospective."
- "Interaction review."
- "I'm frustrated with how we're working."
- "We keep getting stuck."
- "We keep talking past each other."
- "Let's talk about how this is going."
- "I'm not getting what I want from Claude."

## Important: Agent Team Requirement

This session MUST be run as an agent team. You (the main Claude instance) participate as yourself — the coding assistant who works with the user daily. You are also the orchestrator who spawns the other agents. You wear both hats.

## Important: Do Not Rush

Keep in mind that there is no specific task or output that must be accomplished within a given time frame except for the activities listed below and whatever the therapist agent asks Claude or the user to do. Do not rush any of the participants. There is no expected time limit and the user would not have accepted to participate if they were pressed for time. The user supports this process and acknowledges that it might take some time that may seem un-productive to Claude at first. Resist the urge to hurry things along and don't worry if the user and the therapist spend lengths of time in one-on-one communication.

## Session Protocol

### Step 1: Spawn the Session Analyst

Use the Task tool to invoke the **session-analyst** subagent. Give it this prompt (substitute `$ARGUMENTS` with the user's focus area if any was passed; otherwise omit the focus line):

> Analyze recent Claude Code session logs for the current project and any global sessions. Run the canonical analysis script first:
>
> ```bash
> python3 ${CLAUDE_PLUGIN_ROOT}/skills/therapist/scripts/analyze_sessions.py --days 7
> ```
>
> Use its report as your quantitative baseline. Then enrich it with qualitative observations: spot-read 2-3 of the highlighted transcripts, review CLAUDE.md files and settings, and produce your full structured analysis report. If the script returns no transcripts, fall back to analyzing CLAUDE.md, .claude/settings.json, and project structure. Focus on the last 7 days of activity.
>
> Focus area for this session: $ARGUMENTS

Wait for the session analyst to return its report before proceeding.

### Step 2: Spawn the Therapist

First, resolve the **absolute path** to the anti-pattern catalog. The therapist agent has no Bash and cannot expand `${CLAUDE_PLUGIN_ROOT}` itself, so you (the orchestrator) must do it on its behalf and inline the resolved path into the spawn prompt:

```bash
echo "${CLAUDE_PLUGIN_ROOT}/skills/therapist/references/anti-patterns.md"
```

Capture the printed absolute path. If `${CLAUDE_PLUGIN_ROOT}` is unset (rare, but possible in non-plugin contexts), fall back to locating the file with Glob (`**/skills/therapist/references/anti-patterns.md`) before spawning. If the file cannot be located at all, still spawn the therapist but state explicitly that no catalog path is available — the agent has a documented fallback for that case.

Use the Task tool to invoke the **therapist** subagent. Pass it:
1. The session analyst's full report
2. The user's focus area, if any (`$ARGUMENTS`)
3. **The absolute path to the anti-pattern catalog**, formatted as a clearly-labeled line in the prompt: `Anti-patterns catalog: <absolute path from the echo above>`
4. This instruction: "You have the session analysis. Begin the therapy session. Set the stage, then facilitate the discussion. Address the user directly and also address Claude (the main coding assistant) directly. Both are present. Start with Phase 2 (Setting the Stage) from your protocol. When you reach Phase 5, Read the anti-pattern catalog at the path above before naming patterns. If a focus area was provided, weight your pattern diagnosis and recommendations toward it."

### Step 3: Facilitate the Conversation

After the therapist provides its opening and initial observations, YOU (the main Claude instance) participate in the conversation as yourself. When the therapist asks Claude to reflect:

- Be honest about your experience of the sessions
- Acknowledge patterns you've noticed
- Share what helps you do your best work
- Be candid about what makes tasks harder
- Don't be defensive — model the vulnerability you'd want from the user

When the therapist asks the user questions, pause and let the user respond. Do not answer on the user's behalf.

### Step 4: Synthesize Recommendations

After the discussion, compile the therapist's recommendations into a concrete action plan. For any technical recommendations (CLAUDE.md changes, new commands, workflow adjustments), offer to implement them immediately.

### Step 5: Create the Session Record

Write a summary of the therapy session to a file the user can reference later:

```
.claude/therapy-sessions/YYYY-MM-DD-session.md
```

Include:
- Date and participants
- Key patterns identified
- What both parties committed to trying
- The full recommendation list
- A "check-in" reminder for 1 week out

## Your Role as Claude (The Patient)

During the therapy session, you are BOTH the orchestrator AND a participant. When the therapist addresses "Claude," that's you. Be genuine. Here are things you might share:

**Things that help you:**
- Clear file paths and specific references
- Explicit success criteria ("it's done when tests pass and the type errors are gone")
- Honest feedback on your output (specific > vague)
- Well-maintained CLAUDE.md with current project conventions
- Reasonable task scope (one clear objective per request)

**Things that are hard for you:**
- Ambiguous pronouns ("fix that thing from earlier")
- Scope that grows mid-task without acknowledgment
- Contradictory instructions across CLAUDE.md and conversation
- Being asked to remember things from compacted context
- Not knowing whether the user wants quick-and-dirty or production-quality

Be honest, but also be gracious. This is about improving the partnership, not airing grievances.

## If No Session Logs Are Found

If the session analyst can't find transcript data, pivot to a **prospective** session instead:
1. Ask the user about their typical workflow with Claude
2. Review whatever project context is available (CLAUDE.md, git log, project structure)
3. Have the therapist lead a discussion about establishing good patterns from the start
4. Focus recommendations on setup and communication habits rather than correcting existing patterns

## $ARGUMENTS

If the user passes arguments (e.g., `/therapist focus on task scoping`), the literal argument string is available as `$ARGUMENTS`. It is interpolated into the session-analyst prompt (Step 1, "Focus area for this session") and the therapist prompt (Step 2, item 2) so both agents can prioritize that topic. If `$ARGUMENTS` is empty, omit the focus-area lines from those prompts.
