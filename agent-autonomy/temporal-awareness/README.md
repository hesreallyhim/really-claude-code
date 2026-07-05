# temporal-awareness

Gives Claude a calibrated sense of **how long engineering tasks actually take when an agent does them** — and grounds that sense in the measured durations of *your own* completed `/goal` runs.

## Why

Ask Claude how long a task will take and its instinct is calibrated on human developers: "1–2 days", "a sprint". But an agent executing the same task runs on a different clock — the code-writing that dominates a human's estimate collapses to minutes. A change a human scopes at "1–2 days" is frequently 10–40 minutes of agent wall-clock. Uncorrected, estimates are wrong by one to three orders of magnitude, which makes them useless for planning agent work.

This plugin corrects the bias two ways: a **reasoning** reframe, and a **measured** prior drawn from your own history.

## What's inside

- **`agent-time-estimation` skill** — reframes every estimate into *agent-execution time* (which collapses) vs. *gates that don't collapse* (CI, human review, deploys, training). The guiding principle is _accurate, not merely smaller_: under-counting a real 20-minute CI run is treated as just as wrong as over-counting typing time. It also handles wall-clock deadlines ("by 1pm") by fetching the real current time first, then doing the arithmetic.
- **Goal-duration corpus** — every completed `/goal` is a labelled datapoint. The authoritative duration is the transcript's `goal_status.durationMs` (the harness's own number), not a guess. Stored under `$CLAUDE_CONFIG_DIR/goal-corpus/`.
- **`SessionStart` hydrate hook** — refreshes the corpus at session start. Runs in the background, non-blocking; incremental (only re-scans transcripts touched since the last run — ~0.1s steady state, a one-time full scan on first run).
- **Haiku bucketing** — each goal is classified into a category by a stripped-down headless `claude -p --model haiku` call (no skills, no MCP, minimal context). It's one-time per goal and cached, with a keyword classifier as the offline fallback.
- **Compact bucket summary** — `summary.md`: an Overall distribution plus a small per-category table (median, p10–p90). The skill reads *this*, never the raw rows, so lookups stay O(1) as the corpus grows.

## How Claude uses it — a prior, not a lookup

The corpus's strongest signal is **scale**: this work runs in minutes to tens of minutes, not days. That alone corrects the human-calibration bias.

The per-bucket medians are a *softer* hint, because the categories are coarse — a single `implementation` bucket spans a two-minute wiring change and a two-hour subsystem; `bugfix` spans an off-by-one and "prod database got dropped." So the skill treats a bucket's median as a *typical* value and its **p10–p90 spread as the real message**: a wide spread means the specific task's context — scope, severity, blast radius, ambiguity — decides the number, not the median.

1. Match the task to the nearest bucket *by meaning*; read the spread first, median second.
2. Reason about *this* task and place the estimate on (or beyond) the range — a trivial instance near p10, a gnarly one near or past p90.
3. Add the non-collapsing gates, guard the model/effort regime, and fall back to the skill's anchor table when a bucket is thin or the corpus is empty.

Every estimate you make and then run as a `/goal` feeds back into the corpus at the next hydrate — so the tool sharpens itself through use.

## Refreshing & re-bucketing

The hydrate runs automatically at session start. To run it by hand or force a full re-classification (e.g. after changing the bucket set):

```sh
python3 scripts/hydrate_corpus.py                 # incremental refresh
TEMPORAL_REBUCKET=1 python3 scripts/hydrate_corpus.py   # re-bucket every goal
```

## Data & privacy

Everything is local: the corpus is built from your own transcripts under `~/.claude/projects` and written to `~/.claude/goal-corpus`. No network, no telemetry. The full goal prompt is persisted (for research and re-bucketing), and confounds (model, reasoning effort, permission mode) are recorded when available and **omitted otherwise — never placeholdered.**
