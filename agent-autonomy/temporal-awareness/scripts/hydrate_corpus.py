#!/usr/bin/env python3
"""Hydrate the goal-duration corpus from Claude Code transcripts, then precompute a
compact bucket summary the skill can consult without reading raw rows.

Source of truth: transcript records with
    .attachment.type == "goal_status" && .attachment.met == true   -> durationMs (authoritative)
    .attachment.type == "goal_status" && .attachment.met == false && sentinel  -> start

Confounds (model, speed, permission_mode, reasoning effort, thinking proxy) are captured
where available; effort/permission come from the session's hook-input debug log when it
still exists. Anything we can't measure is OMITTED, never placeholdered.

FAST BY DESIGN (safe for a SessionStart hook):
  * incremental — only re-scans transcript files modified since the last hydrate
  * the corpus accumulates (overlay merge), so rows survive transcript rotation/pruning
  * the summary is recomputed from the full (small) corpus each run — O(n) over goals, not turns

Outputs (under $CLAUDE_CONFIG_DIR/goal-corpus, default ~/.claude/goal-corpus):
    goal-measurements.json   full corpus (one row per completed goal)
    summary.json / summary.md   compact per-bucket stats  <-- what the skill reads
    .hydrate_state.json      watermark for incremental runs
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict
import json, glob, os, re, time, shutil, subprocess

CONFIG = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude")))
PROJECTS = CONFIG / "projects"
DEBUG = CONFIG / "debug"
CORPUS_DIR = CONFIG / "goal-corpus"
CORPUS = CORPUS_DIR / "goal-measurements.json"
SUMMARY_JSON = CORPUS_DIR / "summary.json"
SUMMARY_MD = CORPUS_DIR / "summary.md"
STATE = CORPUS_DIR / ".hydrate_state.json"

IDLE_GAP_S = 300
INTERRUPT = "[Request interrupted by user]"
MTIME_BUFFER_S = 3600  # re-scan files touched up to an hour before last watermark (safety)

TS_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}T[\d:.]+Z)")
EFFORT_RE = re.compile(r'"effort":\{"level":"([a-z]+)"\}')
PM_RE = re.compile(r'"permission_mode":"([a-zA-Z]+)"')

# --- crude, cheap bucketing: keyword categories. Claude classifies a new task by picking
#     the nearest label; the summary is keyed by these, so lookups are O(1). ---
CATEGORY_HINTS = {
    "skill-creation": ("skill-creator", "create a skill"),
    "bulk-processing": ("go through", "one by one", "each file", "markdown files", "batch", "descending order"),
    "review-audit": ("signoff", "sign off", "review", "audit", "evaluate"),
    "bugfix": ("bug", "flaky", "fix "),
    "design-planning": ("design", "architecture", "curate", "roadmap", "plan"),
    "ui": ("readability", "ui", "css", "overlay", "translucent", "dark mode"),
    "implementation": ("implement", "mvp", "feature", "register"),
}

def parse_ts(s):
    try: return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception: return None

def text_of(o):
    m = o.get("message")
    c = m.get("content") if isinstance(m, dict) else o.get("content")
    if isinstance(c, list):
        return " ".join(str(x.get("text","") if isinstance(x, dict) else x) for x in c)
    return str(c) if c is not None else ""

BUCKETS = list(CATEGORY_HINTS.keys()) + ["other"]

def classify(cond: str) -> str:
    """Instant keyword bucketing — the offline fallback / cold default."""
    c = cond.lower()
    for cat, hints in CATEGORY_HINTS.items():
        if any(h in c for h in hints):
            return cat
    return "other"

def _classify_chunk(claude, descriptions):
    """One batched `claude -p` call (Haiku, stripped context) -> list of buckets aligned
    to input, or all-None on failure so the caller keeps keyword labels."""
    items = "\n".join(f"{i}: {d[:240]}" for i, d in enumerate(descriptions))
    prompt = ("Classify each numbered task into exactly one bucket.\n"
              f"Buckets: {', '.join(BUCKETS)}.\n"
              "Return ONLY a JSON array of strings — one bucket per task, in index order. "
              "No prose, no keys.\n\n" + items)
    try:
        r = subprocess.run(
            [claude, "-p", prompt, "--model", "haiku", "--output-format", "text",
             "--setting-sources", "", "--strict-mcp-config",
             "--dangerously-skip-permissions",
             "--system-prompt", "You are a terse text classifier. Output only what is requested."],
            capture_output=True, text=True, timeout=90)
        txt = r.stdout.strip()
        s, e = txt.find("["), txt.rfind("]")
        arr = json.loads(txt[s:e + 1])
        if isinstance(arr, list) and len(arr) == len(descriptions):
            return [a if a in BUCKETS else "other" for a in arr]
    except Exception:
        pass
    return [None] * len(descriptions)

def classify_llm(descriptions):
    """Batched Haiku bucketing (chunked). Returns labels aligned to input; None where the
    model call failed (caller retains the keyword label for those)."""
    claude = shutil.which("claude")
    if not claude or not descriptions:
        return [None] * len(descriptions)
    out = []
    for i in range(0, len(descriptions), 40):
        out.extend(_classify_chunk(claude, descriptions[i:i + 40]))
    return out

def top(counter):
    return counter.most_common(1)[0][0] if counter else None

def percentile(sorted_vals, q):
    if not sorted_vals: return None
    if len(sorted_vals) == 1: return sorted_vals[0]
    idx = q * (len(sorted_vals) - 1)
    lo, hi = int(idx), min(int(idx) + 1, len(sorted_vals) - 1)
    frac = idx - lo
    return round(sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac, 1)

def debug_meta(sid, start, end):
    if not (sid and start and end):
        return None, None
    files = list(DEBUG.glob(f"{sid}.txt")) + list(DEBUG.glob(f"{sid}.*.txt"))
    efforts, perms = Counter(), Counter()
    for f in files:
        try:
            for l in open(f, errors="ignore"):
                m = TS_RE.match(l)
                if not m: continue
                t = parse_ts(m.group(1))
                if not t or not (start <= t <= end): continue
                em = EFFORT_RE.search(l)
                if em: efforts[em.group(1)] += 1
                pm = PM_RE.search(l)
                if pm: perms[pm.group(1)] += 1
        except OSError:
            pass
    return top(efforts), top(perms)

def load_file(f):
    events, ameta, pmeta, goals = [], [], [], []
    for ln in open(f, errors="ignore"):
        try: o = json.loads(ln)
        except Exception: continue
        ts = parse_ts(o.get("timestamp", ""))
        att = o.get("attachment")
        if isinstance(att, dict) and att.get("type") == "goal_status":
            goals.append({"ts": ts, "att": att})
        if ts:
            events.append((ts, text_of(o)))
            pm = o.get("permissionMode")
            if pm: pmeta.append((ts, pm))
        if o.get("type") == "assistant" and ts:
            m = o.get("message") or {}
            u = m.get("usage") or {}
            content = m.get("content") or []
            has_think = any(isinstance(x, dict) and x.get("type") == "thinking" for x in content)
            ameta.append((ts, m.get("model"), u.get("speed"), u.get("service_tier"),
                          o.get("version"), has_think, u.get("output_tokens") or 0))
    events.sort(key=lambda e: e[0])
    return events, ameta, pmeta, goals

def active_minutes(events, start, end):
    win = [(t, tx) for (t, tx) in events if start <= t <= end]
    if len(win) < 2: return None
    total = 0.0
    for i in range(1, len(win)):
        gap = (win[i][0] - win[i-1][0]).total_seconds()
        if gap <= IDLE_GAP_S and INTERRUPT not in win[i-1][1]:
            total += gap
    return round(total / 60, 1)

def mine(files):
    rows = []
    for f in files:
        try:
            events, ameta, pmeta, goals = load_file(f)
        except OSError:
            continue
        if not any(g["att"].get("met") is True for g in goals):
            continue
        sid = Path(f).stem
        sentinels = [g for g in goals if g["att"].get("met") is False and g["att"].get("sentinel")]
        for g in goals:
            att = g["att"]
            if att.get("met") is not True:
                continue
            end, dur_ms, cond = g["ts"], att.get("durationMs"), (att.get("condition") or "").strip()
            start = None
            for s in sentinels:
                if (s["att"].get("condition") or "").strip() == cond and s["ts"] and end and s["ts"] <= end:
                    start = s["ts"]
            win_start = start or (events[0][0] if events else None)
            wm = [a for a in ameta if win_start and end and win_start <= a[0] <= end]
            models, speeds, tiers, versions = (Counter() for _ in range(4))
            n_msg = n_think = out_tok = 0
            for (_, mdl, spd, tier, ver, ht, ot) in wm:
                if mdl: models[mdl] += 1
                if spd: speeds[spd] += 1
                if tier: tiers[tier] += 1
                if ver: versions[ver] += 1
                n_msg += 1; n_think += 1 if ht else 0; out_tok += ot or 0
            perms = Counter(pm for (t, pm) in pmeta if win_start and end and win_start <= t <= end)
            effort, pm_dbg = debug_meta(sid, win_start, end)
            row = {
                "description": cond,   # full goal prompt — persisted for research / re-bucketing
                "category": classify(cond),
                "category_source": "keyword",
                "duration_min": round(dur_ms / 60000, 2) if dur_ms is not None else None,
                "active_min_est": active_minutes(events, start, end) if (start and end) else None,
                "interrupts": sum(1 for (t, tx) in events if start and end and start <= t <= end and INTERRUPT in tx),
                "iterations": att.get("iterations"),
                "goal_tokens": att.get("tokens"),
                "model": top(models),
                "speed": top(speeds),
                "effort": effort,
                "permission_mode": top(perms) or pm_dbg,
                "service_tier": top(tiers),
                "cc_version": top(versions),
                "thinking_frac": round(n_think / n_msg, 2) if n_msg else None,
                "output_tokens": out_tok or None,
                "reason": ((att.get("reason") or "")[:280]) or None,
                "session_ts": end.isoformat() if end else None,
                "boundary_confidence": "authoritative",
                "source": "goal_status.durationMs",
            }
            rows.append({k: v for k, v in row.items() if v is not None})
    return rows

def summarize(measurements):
    def stats(vals):
        v = sorted(vals)
        if not v: return None
        return {"n": len(v), "median": percentile(v, .5), "p10": percentile(v, .1),
                "p90": percentile(v, .9), "min": v[0], "max": v[-1]}
    all_dur = [r["duration_min"] for r in measurements if r.get("duration_min")]
    by_cat = defaultdict(list)
    for r in measurements:
        if r.get("duration_min"):
            by_cat[r.get("category", "other")].append(r["duration_min"])
    models = Counter(r.get("model") for r in measurements if r.get("model"))
    efforts = Counter(r.get("effort") for r in measurements if r.get("effort"))
    return {
        "overall": stats(all_dur),
        "by_category": {c: stats(v) for c, v in sorted(by_cat.items())},
        "models": dict(models),
        "efforts": dict(efforts) or {"unknown": len(measurements)},
        "category_hints": {c: list(h) for c, h in CATEGORY_HINTS.items()},
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

def render_md(summary):
    o = summary["overall"]
    if not o:
        return "# Goal-duration corpus\n\n(No completed goals recorded yet.)\n"
    L = []
    L.append("# Goal-duration corpus summary")
    L.append("")
    L.append("Measured durations of the user's **own completed `/goal` runs** — real agent")
    L.append("wall-clock, in **minutes**. Regenerated by the hydrate hook; do not hand-edit.")
    L.append("")
    L.append("**Use as a prior, not a lookup.** The strong signal is *scale* (this work is")
    L.append("minutes, not days). Bucket medians are soft — categories are coarse, and a wide")
    L.append("p10–p90 means the specific task's context (scope, severity, ambiguity), not the")
    L.append("median, decides the number. Read a bucket as *typical*, then reason about THIS task.")
    L.append("")
    L.append(f"**Overall** — n={o['n']}, median **{o['median']}m**, p10–p90 {o['p10']}–{o['p90']}m "
             f"(range {o['min']}–{o['max']}m)")
    mdl = ", ".join(f"{k}×{v}" for k, v in summary["models"].items()) or "unknown"
    eff = ", ".join(f"{k}×{v}" for k, v in summary["efforts"].items())
    L.append(f"Regime: model {mdl}; effort {eff}. Compare only within a like regime.")
    L.append("")
    L.append("| bucket | n | median | p10–p90 |")
    L.append("|---|---|---|---|")
    for cat, s in summary["by_category"].items():
        if not s: continue
        rng = f"{s['p10']}–{s['p90']}" if s["n"] >= 3 else f"{s['min']}–{s['max']}"
        L.append(f"| {cat} | {s['n']} | {s['median']}m | {rng}m |")
    L.append(f"| _(no match → use Overall)_ | {o['n']} | {o['median']}m | {o['p10']}–{o['p90']}m |")
    L.append("")
    L.append("Buckets (corpus rows are Haiku-classified). Match a new task to the nearest "
             "by meaning — these keyword hints are just a guide:")
    for c, hints in summary["category_hints"].items():
        L.append(f"- **{c}**: {', '.join(hints)}")
    L.append("- **other**: anything else → fall back to Overall (or the sibling anchor table).")
    return "\n".join(L) + "\n"

def main():
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    # load state + existing corpus
    watermark = 0.0
    if STATE.exists():
        try: watermark = json.loads(STATE.read_text()).get("last_mtime", 0.0)
        except Exception: pass
    existing = {}
    if CORPUS.exists():
        try:
            for r in json.loads(CORPUS.read_text()).get("measurements", []):
                existing[(r.get("description"), r.get("duration_min"), r.get("session_ts"))] = r
        except Exception: pass

    # incremental file selection
    all_files = glob.glob(str(PROJECTS / "*" / "*.jsonl"))
    if watermark and existing:
        files = [f for f in all_files if os.path.getmtime(f) >= watermark - MTIME_BUFFER_S]
    else:
        files = all_files  # cold start: full scan

    mined = mine(files)
    for r in mined:
        existing[(r.get("description"), r.get("duration_min"), r.get("session_ts"))] = r
    measurements = sorted(existing.values(), key=lambda r: r.get("session_ts") or "")

    # Upgrade keyword buckets to Haiku-assigned ones — batched, cached, one-time per goal.
    # TEMPORAL_REBUCKET=1 forces a full re-classification (e.g. after changing the bucket set).
    rebucket = bool(os.environ.get("TEMPORAL_REBUCKET"))
    need = [r for r in measurements if rebucket or r.get("category_source") != "llm"]
    upgraded = 0
    if need:
        labels = classify_llm([r["description"] for r in need])
        for r, lab in zip(need, labels):
            if lab:
                r["category"], r["category_source"] = lab, "llm"
                upgraded += 1

    corpus = {
        "meta": {
            "source": "goal_status.durationMs (authoritative); confounds where available, omitted otherwise",
            "n": len(measurements),
            "note": "duration_min = authoritative goal wall-clock (set->met). Compare within like model/effort regime.",
        },
        "measurements": measurements,
    }
    CORPUS.write_text(json.dumps(corpus, indent=2))
    summary = summarize(measurements)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))
    SUMMARY_MD.write_text(render_md(summary))
    STATE.write_text(json.dumps({"last_mtime": time.time(), "n": len(measurements)}))

    print(f"[temporal-awareness] hydrated: scanned {len(files)} file(s), "
          f"+{len(mined)} mined, {upgraded} haiku-bucketed, corpus n={len(measurements)}")

if __name__ == "__main__":
    main()
