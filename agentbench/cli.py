"""agentbench command line.

  agentbench generate                         build + validate the 66 benchmark tasks
  agentbench bench  [options]                 run single vs multi-agent and write reports
  agentbench report results/<run>             re-render reports from results.jsonl
  agentbench solve  --repo o/r --issue N      triage/repro/fix a real GitHub issue (optionally open the PR)
  agentbench graph                            print the multi-agent graph as Mermaid
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path


def cmd_generate(a):
    from .tasks.generator import generate
    metas = generate(Path(a.out))
    print(f"generated {len(metas)} tasks in {a.out}")


def cmd_bench(a):
    from .bench.report import render_md, write_reports
    from .bench.runner import BenchConfig, run_bench
    if a.backend == "llm":
        import os
        if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")):
            sys.exit("LLM backend needs ANTHROPIC_API_KEY (or OPENAI_API_KEY for openai:* models)")
    cfg = BenchConfig(tasks_dir=a.tasks, out=a.out, systems=a.systems, backend=a.backend, model=a.model,
                      fallback_models=a.fallback_model or [], router=a.router, limit=a.limit, only=a.only,
                      repeats=a.repeats, workers=a.workers, fault_rate=a.fault_rate, seed=a.seed,
                      budget_usd=a.budget, max_coder_attempts=a.max_attempts)
    path = run_bench(cfg)
    s = write_reports(path)
    print("\n" + render_md(s))
    print(f"reports: {Path(a.out) / 'report.md'}  {Path(a.out) / 'report.html'}")


def cmd_report(a):
    from .bench.report import render_md, write_reports
    print(render_md(write_reports(Path(a.run) / "results.jsonl")))


def cmd_solve(a):
    from .graph import build_multi_agent_graph, build_single_agent_graph, run_graph
    from .llm import ModelChain, UsageMeter
    from .prs import GitHubTarget, clone, fetch_issue
    from .state import Deps, RunConfig
    from .workspace import Workspace
    issue = fetch_issue(a.repo, a.issue)
    root = Path(a.workdir or tempfile.mkdtemp(prefix="agentbench-")) / a.repo.replace("/", "__")
    if not root.exists():
        clone(a.repo, root)
    ws = Workspace(root, test_timeout=600)
    deps = Deps(workspace=ws, meter=UsageMeter(budget_usd=a.budget), backend="llm",
                model=ModelChain(a.model, a.fallback_model or []),
                cfg=RunConfig(router=a.router, open_real_pr=a.open_pr),
                github=GitHubTarget(a.repo, base=a.base))
    graph = build_single_agent_graph() if a.system == "single" else build_multi_agent_graph()
    final, secs = run_graph(graph, issue, f"{a.repo}#{a.issue}", deps)
    print(json.dumps({"status": final.get("status"), "resolution": final.get("resolution"),
                      "pr": {k: v for k, v in (final.get("pr") or {}).items() if k != "diff"},
                      "handoffs": [h["dst"] for h in final.get("handoffs", [])],
                      "errors": final.get("errors", []), "seconds": round(secs, 1), **deps.meter.totals()},
                     indent=2, default=str))


def cmd_graph(a):
    from .graph import build_multi_agent_graph, build_single_agent_graph
    g = build_single_agent_graph() if a.single else build_multi_agent_graph()
    print(g.get_graph().draw_mermaid())


def main(argv=None):
    ap = argparse.ArgumentParser(prog="agentbench", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate")
    g.add_argument("--out", default="tasks_data")
    g.set_defaults(fn=cmd_generate)

    def model_args(p):
        p.add_argument("--model", default="anthropic:claude-sonnet-5-5")
        p.add_argument("--fallback-model", action="append", help="repeatable; tried in order when the primary fails")
        p.add_argument("--router", choices=["rules", "llm"], default="rules",
                       help="supervisor routing: deterministic rules, or LLM choosing among legal moves")
        p.add_argument("--budget", type=float, default=1.0, help="USD cap per task (escalates when exceeded)")

    b = sub.add_parser("bench")
    b.add_argument("--tasks", default="tasks_data")
    b.add_argument("--out", default="results/run")
    b.add_argument("--systems", nargs="+", default=["single", "multi"], choices=["single", "multi"])
    b.add_argument("--backend", choices=["offline", "llm"], default="offline")
    b.add_argument("--limit", type=int)
    b.add_argument("--only", nargs="*")
    b.add_argument("--repeats", type=int, default=1)
    b.add_argument("--workers", type=int, default=4)
    b.add_argument("--fault-rate", type=float, default=0.0, help="probability each agent call crashes")
    b.add_argument("--seed", type=int, default=0)
    b.add_argument("--max-attempts", type=int, default=3, help="coder/reviewer rounds before escalation")
    model_args(b)
    b.set_defaults(fn=cmd_bench)

    r = sub.add_parser("report")
    r.add_argument("run")
    r.set_defaults(fn=cmd_report)

    s = sub.add_parser("solve")
    s.add_argument("--repo", required=True, help="owner/name")
    s.add_argument("--issue", type=int, required=True)
    s.add_argument("--base", default="main")
    s.add_argument("--system", choices=["single", "multi"], default="multi")
    s.add_argument("--open-pr", action="store_true", help="push the branch and open a real PR with gh")
    s.add_argument("--workdir")
    model_args(s)
    s.set_defaults(fn=cmd_solve)

    gr = sub.add_parser("graph")
    gr.add_argument("--single", action="store_true")
    gr.set_defaults(fn=cmd_graph)

    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
