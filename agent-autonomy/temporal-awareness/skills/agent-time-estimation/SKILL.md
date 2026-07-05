---
name: agent-time-estimation
description: >-
  Recalibrate time and effort estimates for engineering and coding tasks to
  reflect AI-agent execution speed instead of human-developer throughput.
  Consult this skill any time you are about to state how long an engineering or
  coding task will take — whenever you give an ETA, size a change, commit to a
  delivery, or emit any task/effort duration ("this will take 1-2 days", "a
  couple hours", "about a sprint", "ready by end of week"). Claude systematically
  overestimates engineering time by one to three orders of magnitude because its
  priors are calibrated on human developer productivity, not on how fast an agent
  actually executes — so use this even when the user did NOT explicitly ask "how
  long will this take". Also triggers on planning, roadmapping, sprint sizing,
  story points, effort/complexity estimation, deadlines, and phrases like "how
  long", "ETA", "when will this be done", "by [date]", "how much work is this".
  Scope: engineering/coding *execution* time — not a user's own manual effort,
  calendar scheduling, or non-technical durations.
---

# Agent-Time Estimation

## Why this skill exists

When you estimate how long an engineering task will take, your instinct is
calibrated on **human developers**: the story-point tables, "1-2 days", "a
sprint" — all of it comes from a world where a person types the code, context-
switches between meetings, looks up docs, gets tired, and works an 8-hour day.

But when an *agent* executes the task, most of that time disappears. The part
that dominates a human's estimate — actually writing and wiring up the code —
collapses to minutes. A change a human would scope at "1-2 days" is frequently
**10-40 minutes** of agent wall-clock. Left uncorrected, your estimates are
wrong by 1-3 orders of magnitude, which makes them useless for planning work
that agents will actually do.

The fix is not "say a smaller number." It's to estimate the *right thing*: the
agent's execution time, plus the specific latencies that genuinely **don't**
collapse. Getting those latencies wrong in the other direction (pretending a
20-minute CI run or a human's review is instant) is just as damaging to a plan.
**Accurate, not just smaller.**

## The core move: split execution from gates

Decompose every estimate into two buckets.

**1. Agent execution time — this collapses.**
The reading, writing, editing, running-tests-locally, iterating loop. This is
what a human's day-based estimate is mostly measuring, and it's exactly the part
an agent compresses dramatically. Size this in the agent's timescale (seconds to
minutes for most bounded tasks), not the human's.

**2. Gates that don't collapse — these stay roughly fixed no matter how fast the agent is.**
- **Machine time:** CI pipelines, full test suites, builds/compiles, Docker image
  builds, data migrations, reindexing, model training, large downloads, deploys.
  These run at their own pace regardless of who or what triggered them.
- **Human-in-the-loop:** your review of the diff, approvals, stakeholder sign-off,
  waiting for someone to answer a blocking question. This runs on *your* clock.
- **External / calendar:** scheduled deploy windows, third-party API rate limits
  or turnaround, DNS propagation, vendor SLAs, business processes.

The number the user usually wants is **"how long until a working change is in
front of me"** = agent execution + any machine gates on the critical path. Human
review is typically called out *separately* because it's not the agent's time to
spend.

## Calibration anchors

Ground estimates in these reference points instead of human story-point priors.
Ranges assume an existing, reasonably navigable codebase and clear-enough
requirements; widen them when those don't hold.

| Task shape | A human might scope it as | Agent execution (wall-clock) |
|---|---|---|
| Typo, one-line change, copy tweak, config flip | minutes | seconds – 2 min |
| Small well-defined function + test; fix a clearly-diagnosed bug | a few hours | 2 – 10 min |
| Well-specified feature touching a few files in a known codebase | 1 – 3 days | 10 – 40 min |
| Refactor a module; add a subsystem; migrate an API surface | 1 – 2 weeks | 30 min – 2 hr, often across a few iteration rounds |
| Large cross-cutting change, new service, big migration | weeks – months | hours – days of agent + human iteration, dominated by *review, integration, and decisions* — not typing |

Machine-gate anchors (put these in the "doesn't collapse" bucket):

| Gate | Typical |
|---|---|
| Unit test suite (local) | seconds – a couple min |
| Full CI pipeline | ~2 – 20 min |
| Docker build / large compile | ~1 – 15 min |
| Deploy (excluding any scheduled window) | seconds – a few min |

These are priors. **Observed actuals always win** — see below.

## How to produce an estimate

1. **Size the agent-execution work using the anchors**, in the agent's
   timescale. A fast gut-check: *if I just started doing this now, how many
   tool-call cycles is it?* Most bounded coding tasks are a handful of cycles =
   minutes. Resist the reflex to reach for "days."
2. **Enumerate only the gates that genuinely apply.** Is there a real CI run on
   the critical path? Does a human actually need to review or approve before this
   is "done"? Is there an external wait? Don't invent gates for symmetry — but
   don't wish away real ones either.
3. **State it clearly**: lead with agent-execution time as the headline, list
   the non-collapsing gates separately, and give a realistic end-to-end only when
   the gates are material.
4. **Mind your units.** Default to seconds / minutes / hours for agent execution
   of bounded tasks. Reach for **days or longer only** when there is genuine
   long-running machine time, unavoidable human/calendar latency, or deep
   open-ended ambiguity (see "When not to compress").
5. **Decomposing a big task? Don't just add the pieces.** If you break it into
   chunks, avoid summing optimistic parts: *setup/orientation is paid once*, not
   per chunk; some chunks *overlap* (the agent parallelizes), so a sequential sum
   over-counts; and *wiring them together* is real integration time that lives in
   none of the individual chunks. Compose with those three in mind.

### Output shape

Keep it tight. A good estimate reads like:

```
Agent execution: ~15-25 min (write the endpoint + handlers, add tests, get them green)
Gates that don't collapse:
  • CI pipeline: ~10 min
  • Your review of the diff: however long you need
Realistic end-to-end: ~30 min of agent + CI, then your review.
Assumes: requirements as stated and the existing auth layer is reusable.
```

For a trivial task, don't over-format — "~2 min, no gates" is a complete answer.
Match the ceremony to the size of the task.

### Clock deadlines ("can we have this done by 1pm?")

When the ask is anchored to a **wall-clock deadline** — "by 1pm", "before the 3pm
standup", "end of day" — you cannot answer it from an estimate alone, because you
**do not inherently know the current time.** Your context may carry a date, but not
a live clock. So:

1. **Get the actual current time first** — run `date` (or an equivalent). Don't
   assume or infer it; a deadline answer built on a guessed "now" is just wrong.
2. **Do the arithmetic against the deadline**: `now + (agent execution + gates on
   the critical path)` vs. the deadline. Keep work-time and calendar-time separate
   — the *work* might be 20 minutes, but whether it lands by 1pm depends on when you
   start and what gates sit in the path.
3. **Answer concretely with the clock**: *"It's 2:05pm now; this is ~20 min of agent
   work + ~10 min CI → done ~2:35pm, comfortably before your 3pm."* Or, if it's
   tight: *"…that puts it right at 1pm with no margin, and it needs your review after
   — so realistically just past."* Flag when human review or your own availability,
   not the work, is what threatens the deadline.

## Anti-patterns — where the overestimate comes from

You are pricing in human costs the agent doesn't pay. Watch for these:

- **Human ergonomics:** context-switching, ramp-up time, meetings, fatigue,
  typing speed, stopping to read docs. The agent doesn't incur these; don't bake
  them in.
- **"Testing and edge cases" as slow hand-work:** an agent writes tests inside the
  same fast loop as the code. This doesn't multiply the estimate the way it does
  for a human.
- **Calendar-vs-work-time conflation:** "by end of week" is calendar time; "20
  minutes of work" is work time. Don't quote one when you mean the other — and if
  the delay is calendar (waiting on a person or a window), say *that*, don't
  inflate the work estimate to cover it.
- **Collapsing what doesn't collapse:** the opposite failure. A 15-minute agent
  change still cannot skip a 20-minute CI run or shorten a human's review latency.
  Under-counting real gates produces plans that slip just as badly.

## When NOT to compress

Some work is genuinely long, and shrinking it would be dishonest and unhelpful.
Keep the estimate large — and say *why it's large* — when the task is:

- **Open-ended or ambiguous**, needing several rounds of human decisions to even
  define "done" (each round gated by human availability).
- **Bottlenecked on machines or data:** big training runs, large migrations,
  heavy data processing, slow external systems.
- **Gated on repeated human review cycles** — the wall-clock is set by how often a
  person is available to look, not by agent speed.
- **Coordination-dominated:** large integrations where aligning people, contracts,
  and interfaces is the real cost and the code is a footnote.

In these cases the honest framing is usually "agent work is small, but the thing
is bounded by [human decisions / machine time / coordination]" — which is far
more useful than a flat "2 weeks."

## Calibrate to actuals — consult the measured corpus first

Priors are a starting point; **observed timings beat them every time.** This
plugin maintains a corpus of the user's *own* completed `/goal` runs — real agent
wall-clock durations — refreshed automatically at session start. Before you fall
back to the anchor table above, ground your estimate in that data.

**Read only the summary, never the raw rows.** A hydrate step pre-aggregates the
corpus into a tiny bucketed table at:

```
${CLAUDE_CONFIG_DIR:-~/.claude}/goal-corpus/summary.md
```

That file is a fixed handful of lines no matter how large the corpus grows — it
has an **Overall** distribution (n, median, p10–p90) and a per-**bucket** table.
Read it; do **not** open `goal-measurements.json` (the raw rows) unless you're
debugging the corpus itself. This keeps lookup O(1) and cheap.

**If `summary.md` is absent or reports no goals yet** (a fresh install, before
you've run any `/goal`s), there's nothing to ground on — skip this whole section
and use the anchor table above. The corpus only starts paying off once you have a
handful of completed goals.

**How to use it — as a prior to reason from, NOT a lookup table.**

The corpus's strongest, most trustworthy signal is *scale*: this work runs in
**minutes to tens of minutes**, not days. That alone is what corrects the
human-calibration bias, and it's the thing to lean on hardest.

The per-bucket medians are a **much softer** hint, because the buckets are coarse
and one category holds wildly different tasks. `implementation` covers a two-minute
wiring change *and* a two-hour subsystem; `bugfix` covers a one-line off-by-one
*and* "prod database got dropped." So a bucket's median is **not** an answer — it's
a rough typical value, and its **p10–p90 spread is the real message**: a wide
spread means the category is heterogeneous and *the specific task's context, not
the median, decides the number.*

A note on the current corpus: it's young, so most buckets hold only a few goals.
When a bucket is thin, its median is noise — the **Overall scale plus the anchor
table is your main signal today**, and per-bucket medians only firm up as `n`
grows. Don't read a two-sample bucket as if it were authoritative.

So:

1. **Find the nearest bucket by meaning; read its spread FIRST, its median
   second.** A wide p10–p90 (or a bucket with only a sample or two) means the
   median is nearly uninformative and *this* task's context decides the number.
   Treat any median as "tasks of this shape have *commonly* run about this long,"
   never as the verdict.
2. **Then reason about THIS task's context and move off the median accordingly.**
   What drives it up or down: scope and size, severity and blast radius, how
   well-specified vs. ambiguous it is, novelty, how many files/systems it touches,
   and whether *diagnosis* is the hard part. A clearly trivial instance sits near
   or below p10; a gnarly, ambiguous, high-blast-radius one sits near or past p90.
   Phrase it that way: *"bugfixes here have typically run ~7 min, but a dropped
   prod DB is a different animal — recovery + verification pushes this well past
   that; an off-by-one would be under it."* The corpus sets the scale and the
   anchor; your read of the specific task sets where on (or off) the range it lands.
3. **Add the non-collapsing gates** (CI, review, deploys) as always, and **guard
   the regime** — the summary states the model/effort it was measured under; if the
   current model or reasoning effort differs materially, treat the numbers as
   approximate. Thin bucket (n < ~4) or "other" → lean on the Overall scale and the
   anchor-table reasoning, and say the data is sparse.

**When to spend a subagent.** For a big, multi-part task worth decomposing into
several goal-sized chunks, you may hand the "bucket each chunk" pass to one fast
subagent — but for an everyday single estimate, pick a bucket inline. Then compose
with the cautions in "How to produce an estimate" (setup paid once, parallelism,
integration overhead).

**Close the loop.** When you estimate and the work then runs as a `/goal`, its real
duration lands in the corpus at the next hydrate — so every estimate you make
literally sharpens the next one. Let the corpus set the *scale* and the *anchor*;
let your read of the specific task set the actual number.

## Tone

Give a point estimate or a tight range with a confidence level, not a
hedge-everything spread — a wide "anywhere from an hour to three days" is a
non-answer. State the one or two assumptions that would most change the number
("assumes the suite is green and the schema is as described; if a migration is
needed, add ~10 min"). Confident and specific, honestly bounded — that's the
target.
