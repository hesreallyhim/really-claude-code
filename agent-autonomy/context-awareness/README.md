<p align="center">
  <img src="assets/banner.svg" alt="context-awareness — what Claude sees, every turn. The injected notification line plus a six-tier ladder showing the current pressure level." width="100%">
</p>

## Context-Awareness

> [!NOTE]
> This plug-in was not designed for use with 1M-token context agents, such as Opus 4.8. I have found it to be counter-productive when used with a large-context agent.

I used to think the status line was just an ornamental thing that had little practical value. I still do, but I used to, too. But one cool thing about it is it keeps track of the context window, and gives you direct access to how much of the context has been consumed. And trying to keep track of that manually is a bit tedious. So that's pretty useful information. But Claude doesn't have any idea what its current context budget is. First, you can just ask it - in my experience its response is usually just dependent on the length of the conversation, something which it does have access to, but not in a very precise way; second, you can look at what information is being passed around when you send a message - it tends to include things like what branch you're on, and the current working directory, but the context budget does not appear to be part of that. So, what would it do if it _did_ have that information?

So this plugin tries to provide that feedback to Claude. There are a few hooks that allow you to add information into the context without interrupting Claude's work - in particular, UserPromptSubmit and PostToolUse(Failure). The plugin leverages those hooks to send little updates to Claude about its context budget as the session goes on. The notifications look like this:

```sh
[context: 32% used (small) | +3.2% last turn | ~0.38%/tool | ~179 tool calls remaining]
```

It sends the `context_window.used_percentage` directly from the status line. Then it keeps track of the "burn rate", and gives a rough estimate of how many tool calls Claude should expect to be able to make before its context budget runs out. According to some Claudes, this information is the most useful, because it is directly actionable:

> "The "remaining tool calls" metric is what actually guides my decisions — it's concrete and immediate, whereas the percentage and burn rate require mental calculation. "

 The plugin grabs the data from the status line and writes it to a file for the hooks to consume. And at the start of the session it includes some general guidelines to Claude informing it about the injected notifications and how to optimize its behavior. Here's what it looks like:

```mermaid
flowchart TD
    subgraph init ["Session Start"]
        S["setup-statusline.sh"] -->|patches| SET["settings.json"]
        S -->|installs to stable path| W["statusline-wrapper.sh"]
        BG["budgeting-guidelines.md"]
    end

    subgraph tick ["Every Statusline Tick"]
        SL["Claude Code<br>statusline JSON"] -->|stdin| SW["statusline-wrapper.sh"]
        SW -->|persists| SF[("session state file<br>(used_percentage)")]
    end

    subgraph hook ["Hook Events"]
        SF -->|reads current %| HK["context-awareness-hook.sh"]
        TF[("tracking file<br>(calls, turns, burn rate)")] <-->|reads/writes| HK
        HK -->|UserPromptSubmit| RICH["Enriched notification<br>% + delta + burn rate + remaining"]
        HK -->|PostToolUse| BRIEF["Brief notification<br>% only"]
    end

    BG -->|injected at start| C((Claude))
    RICH -->|system-reminder| C
    BRIEF -->|system-reminder| C

    init -.-> tick -.-> hook
```

<br>
And here's what it looks like but more horizontal:

<br>

```mermaid
sequenceDiagram
    participant SL as Statusline
    participant S as State File
    participant H as Hook
    participant C as Claude

    SL->>S: persist used_%

    Note over H,C: UserPromptSubmit
    H->>S: read %
    H-->>C: [context: 32% used (small) | +3.2% | ~0.38%/tool | ~179 remaining]

    Note over H,C: PostToolUse
    H->>S: read %
    H-->>C: [context: 33% used (small)]
```

### Status Lines

Status lines are not integrated with plugins, so you have to come up with your own way to ship a plugin that involves a status line. The status line has its own channel where it receives data from Claude Code. On SessionStart, the plugin runs a script that adds a status line entry to the user's settings file. It acts as a transparent pass-through proxy that captures the input from stdin, stores the relevant data to a directory inside `$HOME/.claude/context-awareness`, and then passes it on to any other status lines that the user may have configured. This is not the most elegant solution, but I've tried to design the plugin to be minimally disruptive to the user's existing setup. Additionally, although this is unlikely in practice, if the plugin were disabled or uninstalled, the status line wrapper would be left over in the user's `settings.json`. However, it would not cause an error and would simply end up silently failing.

### Advanced Configuration

The plugin ships with sensible defaults, but you can customize what data Claude sees and how it responds to it. Run `/context-awareness:config` to view or change settings interactively, or edit the config file directly at `$CLAUDE_PLUGIN_DATA/config.yaml`.

**Providers** control which data sources are included in notifications:

| Provider | Default | What it does |
|----------|---------|--------------|
| `context` | enabled | Context window usage percentage, burn rate, remaining tool calls |
| `cost` | disabled | Session spend in USD against a user-defined budget |
| `rate_limits` | disabled | 5-hour and 7-day API rate limit usage |

Enabling `cost` requires setting a `session_budget` (in USD). Rate limits require no additional configuration.

Note that the `used_percentage` from the status line is already adjusted to whatever the user has set as the threshold for auto-compaction - so 100% always means "100% of the usable context window".

**Guidelines** control the behavioral guidance injected at session start. By default, Claude receives a set of tier-based instructions (e.g., "be concise above 50%", "checkpoint frequently above 70%"). To use your own, set `guidelines` to a file path:

```yaml
guidelines: /path/to/my-guidelines.md
```

Custom guidelines completely replace the defaults — they are not merged.

**Effort mode** is a session-scoped setting that controls whether the plugin automatically adjusts Claude's thinking effort as context pressure increases. There are obvious intersections between this configuration and Claude's extended thinking capacity. It can be cycled via `/context-awareness:config change`:

| Mode | Behavior |
|------|----------|
| `off` (default) | No adjustment — effort stays wherever you set it |
| `adaptive` | Downshifts effort at 50% (medium) and 70% (low) |
| `planMode` | High effort for planning, low for execution |

---

MIT Copyright (c) 2026 Really Him
