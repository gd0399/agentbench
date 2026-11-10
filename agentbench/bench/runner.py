"""Run systems over the task suite and grade every run against the hidden tests.

One row per (system, task, repeat) goes to results.jsonl; per-run artefacts
(PR body, diff, handoff trail) go to <out>/runs/<system>/<task>/.
"""
from __future__ import annotations

import json
import shutil
import tempfile
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ..graph import build_multi_agent_graph, build_single_agent_graph, run_graph
from ..llm import ModelChain, UsageMeter
from ..state import Deps, FaultInjector, RunConfig
from ..tasks.generator import run_suite
from ..workspace import Workspace

SYSTEMS = {"single": build_single_agent_graph, "multi": build_multi_agent_graph}


@dataclass
class BenchConfig:
    tasks_dir: str = "tasks_data"
    out: str = "results/run"
    systems: list[str] = field(default_factory=lambda: ["single", "multi"])
    backend: str = "offline"
    model: str = "anthropic:claude-sonnet-5-5"
    fallback_models: list[str] = field(default_factory=lambda: ["anthropic:claude-haiku-5-5"])
    router: str = "rules"
    limit: int | None = None
    only: list[str] | None = None
    repeats: int = 1
    workers: int = 4
    fault_rate: float = 0.0
    seed: int = 0
    budget_usd: float | None = 1.0
    max_coder_attempts: int = 3
    max_agent_steps: int = 25
    max_single_steps: int = 60


def load_tasks(tasks_dir: str, limit: int | None = None, only: list[str] | None = None) -> list[dict]:
    metas = json.loads((Path(tasks_dir) / "index.json").read_text())
    if only:
        metas = [m for m in metas if m["id"] in only]
    if limit:
        # stratified: keep the bug/invalid mix when sub-sampling
        bugs = [m for m in metas if m["kind"] == "bug"]
        inv = [m for m in metas if m["kind"] != "bug"]
        k_inv = max(1, round(limit * len(inv) / len(metas))) if inv else 0
        metas = bugs[: limit - k_inv] + inv[:k_inv]
    return metas


def source_unchanged(ws: Workspace, original_repo: Path) -> bool:
    for p in (original_repo / "toolkit").rglob("*.py"):
        rel = p.relative_to(original_repo)
        if (ws.root / rel).read_text() != p.read_text():
            return False
    return True


def grade(meta: dict, final: dict, ws: Workspace, task_dir: Path) -> dict:
    hidden_src = task_dir / "hidden" / "test_hidden.py"
    target = ws.root / "_hidden_grading_test.py"
    shutil.copy(hidden_src, target)
    results = run_suite(ws.root, target, timeout=120)
    target.unlink(missing_ok=True)
    hidden_pass = bool(results) and all(results.values())
    status = final.get("status", "escalated")
    if meta["kind"] == "bug":
        success = status == "pr_opened" and hidden_pass
    else:
        success = status in ("invalid", "not_reproducible") and source_unchanged(ws, task_dir / "repo")
    research = final.get("research") or {}
    triage = final.get("triage") or {}
    return {
        "success": success,
        "hidden_pass": hidden_pass,
        "hidden_failed": sorted(n for n, ok in results.items() if not ok)[:10],
        # A PR was opened but the fix is wrong: the costly failure mode in production.
        "false_positive_pr": status == "pr_opened" and not success,
        "localized": meta["file"] in (research.get("suspected_files") or [])[:3] if meta["kind"] == "bug" else None,
        "triage_component_hit": (triage.get("component") == meta["component"]) if triage else None,
    }


def run_one(system: str, meta: dict, cfg: BenchConfig, repeat: int, graphs: dict) -> dict:
    task_dir = Path(cfg.tasks_dir) / meta["id"]
    issue = json.loads((task_dir / "issue.json").read_text())
    tmp = Path(tempfile.mkdtemp(prefix=f"ab-{system}-"))
    row = {"system": system, "task_id": meta["id"], "repeat": repeat, "kind": meta["kind"],
           "category": meta["category"], "difficulty": meta["difficulty"], "backend": cfg.backend,
           "model": cfg.model if cfg.backend == "llm" else "offline", "fault_rate": cfg.fault_rate}
    try:
        shutil.copytree(task_dir / "repo", tmp / "repo")
        ws = Workspace(tmp / "repo")
        ws.init_git()
        meter = UsageMeter(budget_usd=cfg.budget_usd if cfg.backend == "llm" else None)
        deps = Deps(
            workspace=ws, meter=meter, backend=cfg.backend,
            model=ModelChain(cfg.model, cfg.fallback_models) if cfg.backend == "llm" else None,
            faults=FaultInjector(cfg.fault_rate, seed=cfg.seed * 1000 + repeat),
            cfg=RunConfig(max_coder_attempts=cfg.max_coder_attempts, max_agent_steps=cfg.max_agent_steps,
                          max_single_steps=cfg.max_single_steps, router=cfg.router))
        t0 = time.perf_counter()
        try:
            final, latency = run_graph(graphs[system], issue, meta["id"], deps)
            crash = None
        except Exception as e:  # graph-level crash: count as failure, keep going
            final, latency, crash = {"status": "escalated"}, time.perf_counter() - t0, f"{type(e).__name__}: {e}"
        row.update(grade(meta, final, ws, task_dir))
        row.update(status=final.get("status"), latency_s=round(latency, 3), crash=crash,
                   handoffs=len(final.get("handoffs", [])), path=[h["dst"] for h in final.get("handoffs", [])],
                   recovered_errors=len(final.get("errors", [])), injected_failures=deps.faults.injected,
                   fallbacks_used=sorted({e["recovered_by"] for e in final.get("errors", [])}),
                   coder_attempts=final.get("coder_attempts", 0), **meter.totals())
        art = Path(cfg.out) / "runs" / system / f"{meta['id']}-r{repeat}"
        art.mkdir(parents=True, exist_ok=True)
        pr = final.get("pr") or {}
        if pr.get("body"):
            (art / "PR.md").write_text(f"# {pr['title']}\n\nbranch: `{pr['branch']}`\n\n{pr['body']}")
        (art / "patch.diff").write_text(pr.get("diff") or (final.get("patch") or {}).get("diff") or "")
        (art / "trail.json").write_text(json.dumps({
            "handoffs": final.get("handoffs", []), "errors": final.get("errors", []),
            "trace": final.get("trace", []), "triage": final.get("triage"),
            "research": {k: v for k, v in (final.get("research") or {}).items() if not k.startswith("_")},
            "review": final.get("review"), "resolution": final.get("resolution")}, indent=1, default=str))
    except Exception:
        row.update(success=False, status="harness_error", crash=traceback.format_exc()[-1500:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return row


def run_bench(cfg: BenchConfig, log=print) -> Path:
    out = Path(cfg.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "config.json").write_text(json.dumps(asdict(cfg), indent=2))
    metas = load_tasks(cfg.tasks_dir, cfg.limit, cfg.only)
    graphs = {s: SYSTEMS[s]() for s in cfg.systems}
    jobs = [(s, m, r) for r in range(cfg.repeats) for m in metas for s in cfg.systems]
    results_path = out / "results.jsonl"
    lock = threading.Lock()
    done = 0
    log(f"running {len(jobs)} jobs: {len(metas)} tasks x {cfg.systems} x {cfg.repeats} repeat(s), "
        f"backend={cfg.backend}, fault_rate={cfg.fault_rate}, workers={cfg.workers}")
    with open(results_path, "w") as fh, ThreadPoolExecutor(max_workers=cfg.workers) as pool:
        futs = [pool.submit(run_one, s, m, cfg, r, graphs) for s, m, r in jobs]
        for f in as_completed(futs):
            row = f.result()
            with lock:
                fh.write(json.dumps(row) + "\n")
                fh.flush()
                done += 1
                mark = "✓" if row.get("success") else "✗"
                log(f"  [{done:>3}/{len(jobs)}] {mark} {row['system']:<6} {row['task_id']:<30} "
                    f"{row.get('status', '?'):<16} {row.get('latency_s', 0):>6.1f}s ${row.get('cost_usd', 0):.4f}")
    return results_path
