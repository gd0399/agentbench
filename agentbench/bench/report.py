"""Aggregate results.jsonl into summary.json, report.md and report.html.

Statistics:
  * success rate with a 95% Wilson interval
  * paired single-vs-multi comparison on the same tasks: exact McNemar test on
    discordant pairs + bootstrap 95% CI of the success-rate difference
  * cost per task, cost per *successful* task, latency p50/p95
"""
from __future__ import annotations

import html
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

SERIES = {"single": ("#2a78d6", "#3987e5"), "multi": ("#eb6834", "#d95926")}
LABEL = {"single": "Single agent", "multi": "Multi-agent (supervisor)"}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def pct(xs: list[float], q: float) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    i = (len(s) - 1) * q
    lo, hi = math.floor(i), math.ceil(i)
    return s[lo] + (s[hi] - s[lo]) * (i - lo)


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value from discordant counts b (A only) and c (B only)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def summarize_system(rows: list[dict]) -> dict:
    n = len(rows)
    k = sum(r.get("success", False) for r in rows)
    costs = [r.get("cost_usd", 0.0) for r in rows]
    lat = [r.get("latency_s", 0.0) for r in rows]
    lo, hi = wilson(k, n)
    bugs = [r for r in rows if r["kind"] == "bug"]
    loc = [r["localized"] for r in bugs if r.get("localized") is not None]
    tri = [r["triage_component_hit"] for r in rows if r.get("triage_component_hit") is not None]
    statuses = defaultdict(int)
    for r in rows:
        statuses[r.get("status", "?")] += 1
    return {
        "n": n, "successes": k, "success_rate": k / n if n else 0.0, "success_ci95": [lo, hi],
        "false_positive_pr_rate": sum(r.get("false_positive_pr", False) for r in rows) / n if n else 0.0,
        "cost_per_task_mean": statistics.fmean(costs) if costs else 0.0,
        "cost_per_task_median": statistics.median(costs) if costs else 0.0,
        "cost_per_success": (sum(costs) / k) if k else None,
        "total_cost": sum(costs),
        "latency_mean_s": statistics.fmean(lat) if lat else 0.0,
        "latency_p50_s": pct(lat, 0.5), "latency_p95_s": pct(lat, 0.95),
        "llm_calls_mean": statistics.fmean(r.get("llm_calls", 0) for r in rows) if rows else 0.0,
        "input_tokens_mean": statistics.fmean(r.get("input_tokens", 0) for r in rows) if rows else 0.0,
        "output_tokens_mean": statistics.fmean(r.get("output_tokens", 0) for r in rows) if rows else 0.0,
        "handoffs_mean": statistics.fmean(r.get("handoffs", 0) for r in rows) if rows else 0.0,
        "injected_failures": sum(r.get("injected_failures", 0) for r in rows),
        "recovered_errors": sum(r.get("recovered_errors", 0) for r in rows),
        "localization_acc": (sum(loc) / len(loc)) if loc else None,
        "triage_acc": (sum(tri) / len(tri)) if tri else None,
        "statuses": dict(statuses),
    }


def breakdown(rows: list[dict], key: str) -> dict:
    out: dict = defaultdict(dict)
    groups: dict = defaultdict(lambda: defaultdict(list))
    for r in rows:
        groups[r[key]][r["system"]].append(r)
    for g, by_sys in sorted(groups.items()):
        for s, rs in by_sys.items():
            out[g][s] = {"n": len(rs), "success_rate": sum(r.get("success", False) for r in rs) / len(rs)}
    return dict(out)


def paired(rows: list[dict], a: str = "single", b: str = "multi", iters: int = 5000, seed: int = 0) -> dict | None:
    by = defaultdict(dict)
    for r in rows:
        by[(r["task_id"], r["repeat"])][r["system"]] = r
    pairs = [(v[a], v[b]) for v in by.values() if a in v and b in v]
    if not pairs:
        return None
    sa = [int(x.get("success", False)) for x, _ in pairs]
    sb = [int(y.get("success", False)) for _, y in pairs]
    only_a = sum(1 for x, y in zip(sa, sb) if x and not y)
    only_b = sum(1 for x, y in zip(sa, sb) if y and not x)
    rng = random.Random(seed)
    diffs = []
    n = len(pairs)
    for _ in range(iters):
        idx = [rng.randrange(n) for _ in range(n)]
        diffs.append(sum(sb[i] - sa[i] for i in idx) / n)
    ca = sum(x.get("cost_usd", 0) for x, _ in pairs)
    cb = sum(y.get("cost_usd", 0) for _, y in pairs)
    la = statistics.median(x.get("latency_s", 0) for x, _ in pairs)
    lb = statistics.median(y.get("latency_s", 0) for _, y in pairs)
    return {"pairs": n, f"{a}_only": only_a, f"{b}_only": only_b, "both": sum(1 for x, y in zip(sa, sb) if x and y),
            "neither": sum(1 for x, y in zip(sa, sb) if not x and not y),
            "success_diff": (sum(sb) - sum(sa)) / n, "success_diff_ci95": [pct(diffs, 0.025), pct(diffs, 0.975)],
            "mcnemar_p": mcnemar_exact(only_a, only_b),
            "cost_ratio": (cb / ca) if ca else None, "latency_ratio_p50": (lb / la) if la else None}


def build_summary(results_path: Path) -> dict:
    rows = [json.loads(l) for l in results_path.read_text().splitlines() if l.strip()]
    cfg_path = results_path.parent / "config.json"
    cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
    systems = sorted({r["system"] for r in rows}, key=lambda s: list(SERIES).index(s) if s in SERIES else 9)
    return {
        "config": cfg, "n_rows": len(rows), "n_tasks": len({r["task_id"] for r in rows}),
        "systems": {s: summarize_system([r for r in rows if r["system"] == s]) for s in systems},
        "by_difficulty": breakdown(rows, "difficulty"), "by_category": breakdown(rows, "category"),
        "by_kind": breakdown(rows, "kind"),
        "paired": paired(rows) if {"single", "multi"} <= set(systems) else None,
        "harness_errors": [r["task_id"] for r in rows if r.get("status") == "harness_error"],
    }


# --------------------------------------------------------------------------- markdown

def _f(x, kind="pct"):
    if x is None:
        return "—"
    return {"pct": f"{100 * x:.1f}%", "usd": f"${x:.4f}", "s": f"{x:.1f}s", "n": f"{x:.1f}"}[kind]


def render_md(s: dict) -> str:
    cfg = s["config"]
    offline = cfg.get("backend") == "offline"
    L = [f"# Benchmark results — {s['n_tasks']} tasks, {s['n_rows']} runs", ""]
    L.append(f"backend: `{cfg.get('backend')}`" + ("" if offline else f" · model: `{cfg.get('model')}` "
             f"(fallbacks: {', '.join(cfg.get('fallback_models', [])) or 'none'})") +
             f" · router: `{cfg.get('router')}` · injected fault rate: {cfg.get('fault_rate', 0):.0%}"
             f" · repeats: {cfg.get('repeats', 1)}")
    if offline:
        L += ["", "> **Offline backend.** These runs use the deterministic program-repair heuristics, not a language "
              "model: they validate the graph, fallbacks and harness. Cost is $0 by construction. Do not read them "
              "as evidence about LLM single- vs multi-agent performance."]
    L += ["", "| metric | " + " | ".join(LABEL.get(k, k) for k in s["systems"]) + " |",
          "|---|" + "---|" * len(s["systems"])]
    rows = [("success rate", lambda m: f"{_f(m['success_rate'])} ({_f(m['success_ci95'][0])}–{_f(m['success_ci95'][1])})"),
            ("wrong PRs opened (false positives)", lambda m: _f(m["false_positive_pr_rate"])),
            ("cost / task (mean)", lambda m: _f(m["cost_per_task_mean"], "usd")),
            ("cost / successful task", lambda m: _f(m["cost_per_success"], "usd")),
            ("latency p50 / p95", lambda m: f"{_f(m['latency_p50_s'], 's')} / {_f(m['latency_p95_s'], 's')}"),
            ("LLM calls / task", lambda m: _f(m["llm_calls_mean"], "n")),
            ("tokens in / out per task", lambda m: f"{m['input_tokens_mean']:,.0f} / {m['output_tokens_mean']:,.0f}"),
            ("handoffs / task", lambda m: _f(m["handoffs_mean"], "n")),
            ("fault localisation (top-3 file)", lambda m: _f(m["localization_acc"])),
            ("triage component accuracy", lambda m: _f(m["triage_acc"])),
            ("injected failures / recovered errors", lambda m: f"{m['injected_failures']} / {m['recovered_errors']}"),
            ("outcomes", lambda m: ", ".join(f"{k}: {v}" for k, v in sorted(m["statuses"].items())))]
    for name, fn in rows:
        L.append(f"| {name} | " + " | ".join(fn(m) for m in s["systems"].values()) + " |")
    p = s.get("paired")
    if p:
        L += ["", "## Paired comparison (same tasks)", "",
              f"- tasks solved by both: {p['both']}, neither: {p['neither']}, only single: {p['single_only']}, "
              f"only multi: {p['multi_only']}",
              f"- success difference (multi − single): {100 * p['success_diff']:+.1f} pp, bootstrap 95% CI "
              f"[{100 * p['success_diff_ci95'][0]:+.1f}, {100 * p['success_diff_ci95'][1]:+.1f}] pp, "
              f"exact McNemar p = {p['mcnemar_p']:.3g}",
              f"- cost ratio multi/single: {p['cost_ratio']:.2f}×" if p["cost_ratio"] else "- cost ratio: n/a ($0)",
              f"- median latency ratio multi/single: {p['latency_ratio_p50']:.2f}×" if p["latency_ratio_p50"] else ""]
    for title, key in (("By difficulty", "by_difficulty"), ("By category", "by_category")):
        systems = list(s["systems"])
        L += ["", f"## {title}", "", "| group | n | " + " | ".join(LABEL.get(x, x) for x in systems) + " |",
              "|---|---|" + "---|" * len(systems)]
        for g, d in s[key].items():
            n = next(iter(d.values()))["n"]
            L.append(f"| {g} | {n} | " + " | ".join(_f(d[x]["success_rate"]) if x in d else "—" for x in systems) + " |")
    if s["harness_errors"]:
        L += ["", f"**Harness errors:** {', '.join(s['harness_errors'])}"]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- html

def _bars(title: str, systems: dict, value, fmt, ci=None, unit_max=None) -> str:
    """Horizontal bar chart (one bar per system) as inline SVG with hover titles."""
    W, row, left, right = 560, 44, 190, 90
    vals = {k: value(m) or 0.0 for k, m in systems.items()}
    vmax = unit_max or max([*vals.values(), *(ci(m)[1] for m in systems.values())] if ci else vals.values()) or 1.0
    H = row * len(vals) + 16
    out = [f'<figure class="chart"><figcaption>{html.escape(title)}</figcaption>'
           f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">']
    plot_w = W - left - right
    out.append(f'<line x1="{left}" x2="{left}" y1="4" y2="{H - 8}" class="axis"/>')
    for i, (k, v) in enumerate(vals.items()):
        y = 10 + i * row
        w = max(2.0, plot_w * v / vmax)
        out.append(f'<g class="mark"><title>{html.escape(LABEL.get(k, k))}: {fmt(v)}</title>'
                   f'<rect x="{left - 6}" y="{y - 4}" width="{plot_w + right}" height="{row - 6}" class="hit"/>'
                   f'<text x="{left - 10}" y="{y + 15}" text-anchor="end" class="lbl">{html.escape(LABEL.get(k, k))}</text>'
                   f'<path d="M{left},{y + 2} h{w - 4} a4,4 0 0 1 4,4 v16 a4,4 0 0 1 -4,4 h-{w - 4} z" '
                   f'fill="var(--series-{k})"/>')
        if ci:
            lo, hi = ci(systems[k])
            x0, x1 = left + plot_w * lo / vmax, left + plot_w * hi / vmax
            out.append(f'<path d="M{x0},{y + 14} H{x1} M{x0},{y + 9} v10 M{x1},{y + 9} v10" class="ci"/>')
        tx = left + w + 8 if not ci else left + plot_w * ci(systems[k])[1] / vmax + 8
        out.append(f'<text x="{tx}" y="{y + 18}" class="val">{fmt(v)}</text></g>')
    out.append("</svg></figure>")
    return "".join(out)


def render_html(s: dict, md: str) -> str:
    systems = s["systems"]
    offline = s["config"].get("backend") == "offline"
    charts = [
        _bars("Success rate (95% Wilson CI)", systems, lambda m: m["success_rate"], lambda v: f"{100 * v:.1f}%",
              ci=lambda m: m["success_ci95"], unit_max=1.0),
        _bars("Cost per task (mean, USD)", systems, lambda m: m["cost_per_task_mean"], lambda v: f"${v:.4f}"),
        _bars("Latency per task (p50, seconds)", systems, lambda m: m["latency_p50_s"], lambda v: f"{v:.1f}s"),
        _bars("Wrong PRs opened (share of tasks)", systems, lambda m: m["false_positive_pr_rate"],
              lambda v: f"{100 * v:.1f}%", unit_max=max(0.05, *(m["false_positive_pr_rate"] for m in systems.values()))),
    ]
    css_vars_light = "".join(f"--series-{k}:{c[0]};" for k, c in SERIES.items())
    css_vars_dark = "".join(f"--series-{k}:{c[1]};" for k, c in SERIES.items())
    body_md = html.escape(md)
    banner = ('<p class="banner">Offline backend: deterministic repair heuristics, not an LLM. These numbers validate '
              'the harness, graph and fallbacks only; cost is $0 by construction.</p>' if offline else "")
    legend = "".join(f'<span class="key"><i style="background:var(--series-{k})"></i>{LABEL.get(k, k)}</span>'
                     for k in systems)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>agentbench — single vs multi-agent</title><style>
.viz-root{{color-scheme:light;--surface-1:#fcfcfb;--text-primary:#0b0b0b;--text-secondary:#52514e;--rule:#e4e3df;{css_vars_light}}}
@media (prefers-color-scheme:dark){{:root:where(:not([data-theme="light"])) .viz-root{{color-scheme:dark;--surface-1:#1a1a19;--text-primary:#f0efec;--text-secondary:#c3c2b7;--rule:#3a3a37;{css_vars_dark}}}}}
body{{margin:0}} .viz-root{{background:var(--surface-1);color:var(--text-primary);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;min-height:100vh;padding:32px 20px}}
main{{max-width:1100px;margin:0 auto}} h1{{font-size:26px;margin:0 0 4px}} .sub{{color:var(--text-secondary);margin:0 0 20px}}
.banner{{border:1px solid var(--rule);border-left:4px solid var(--text-secondary);padding:10px 14px;border-radius:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(460px,1fr));gap:18px;margin:18px 0}}
.chart{{margin:0;border:1px solid var(--rule);border-radius:10px;padding:12px 14px}} figcaption{{font-weight:600;margin-bottom:6px}}
svg{{width:100%;height:auto;overflow:visible}} .axis{{stroke:var(--rule)}} .lbl,.val{{fill:var(--text-secondary);font-size:13px}}
.val{{fill:var(--text-primary);font-variant-numeric:tabular-nums}} .ci{{stroke:var(--text-primary);stroke-width:1.5;fill:none}}
.hit{{fill:transparent}} .mark:hover .hit{{fill:var(--rule);opacity:.5}}
.legend{{display:flex;gap:18px;color:var(--text-secondary)}} .key i{{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}}
pre{{white-space:pre-wrap;border:1px solid var(--rule);border-radius:10px;padding:16px;font:13px/1.45 ui-monospace,Menlo,monospace;overflow:auto}}
</style></head><body><div class="viz-root"><main>
<h1>Single agent vs. supervisor multi-agent</h1>
<p class="sub">{s['n_tasks']} GitHub-style issues · {s['n_rows']} graded runs · backend <b>{html.escape(str(s['config'].get('backend')))}</b>
{'' if offline else '· model <b>' + html.escape(str(s['config'].get('model'))) + '</b>'} · injected fault rate {s['config'].get('fault_rate', 0):.0%}</p>
{banner}<div class="legend">{legend}</div>
<div class="grid">{''.join(charts)}</div>
<h2>Full results (table view)</h2><pre>{body_md}</pre>
</main></div></body></html>"""


def write_reports(results_path: Path) -> dict:
    s = build_summary(results_path)
    out = results_path.parent
    (out / "summary.json").write_text(json.dumps(s, indent=2))
    md = render_md(s)
    (out / "report.md").write_text(md)
    (out / "report.html").write_text(render_html(s, md))
    return s
