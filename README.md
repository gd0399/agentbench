# agentbench — supervisor multi-agent vs single agent, graded

A LangGraph **supervisor** routes GitHub issues to **researcher → coder → reviewer** agents, which then **open a PR**. A harness compares this setup against a **single-agent** baseline on 66 graded tasks and reports success rate, cost per task and latency.

## Quick start
```bash
pip install -e .
agentbench generate                                   # build + validate 66 tasks (61 bugs, 5 invalid issues)
agentbench bench --backend offline --workers 8        # no API key needed: tests the plumbing
export ANTHROPIC_API_KEY=...
agentbench bench --backend llm --model anthropic:claude-sonnet-5-5 \
  --fallback-model anthropic:claude-haiku-5-5 --router llm --workers 4 --out results/sonnet
agentbench bench --backend llm --fault-rate 0.3 --out results/sonnet-faults   # robustness
agentbench solve --repo you/yourrepo --issue 42 --open-pr                     # live mode (uses gh)
```
Each run writes `results.jsonl`, `summary.json`, `report.md` and `report.html`, plus a PR.md, diff and handoff log for every task.

## Architecture
- **Shared state** (`state.py`): issue, triage, research report, patch, review, PR, plus append-only logs of handoffs, errors and rejected patches.
- **Handoffs**: every specialist returns `Command(goto="supervisor")`. The supervisor works out the *legal moves* from the state. It picks the first one (`--router rules`), or the LLM chooses among them (`--router llm`). An illegal choice falls back to the rules.
- **Fallbacks**: a crashed agent is retried once, then replaced: researcher → coder investigates on its own; coder → generalist (a single agent); reviewer → a deterministic test-runner; generalist → escalate to a human. Models fall back from primary to secondary with backoff. A per-task USD budget escalates when it is exceeded. A guardrail stops the reviewer from approving a patch whose tests fail.
- **Grading**: the agents only see the tests that pass on the buggy code. Grading uses a hidden suite. A task succeeds when a PR is opened **and** the hidden suite passes. For invalid issues, it succeeds when the issue is closed with no source change. The report also counts **wrong PRs opened** (plausible patches that fail the hidden suite).
- **Stats**: Wilson 95% CIs, a paired exact McNemar test, a bootstrap CI on the success-rate difference, cost per successful task, and p50/p95 latency.

## About the offline backend
`--backend offline` replaces the LLM with classical program repair: spectrum-based fault localisation plus mutation search. It lets the graph, fallbacks and harness run in CI. **Its numbers say nothing about LLM agents.** Publish numbers from `--backend llm` only.

## Results — Claude Sonnet 5.5 (fallback: Haiku 5.5), LLM router, 66 tasks, Nov 2026

| | Single agent | Multi-agent | Single, 30% faults | Multi, 30% faults |
|---|---|---|---|---|
| Success rate | **97.0%** (89.6–99.2) | 90.9% (81.6–95.8) | 83.3% (72.6–90.4) | **89.4%** (79.7–94.8) |
| Cost / task | **$0.029** | $0.112 | **$0.025** | $0.089 |
| Cost / success | **$0.030** | $0.123 | **$0.030** | $0.100 |
| Latency p50 / p95 | **31s / 36s** | 76s / 118s | **31s / 36s** | 70s / 115s |
| Wrong PRs opened | 3.0% | 3.0% | 3.0% | 3.0% |

These are pre-fix numbers (see the bug note below). With no failures injected, the single agent was more accurate (paired difference −6.1 pp, 95% CI [−12.1, −1.5], McNemar p = 0.125), 3.9× cheaper and 2.5× faster. When 30% of agent calls crashed, the single agent lost 14 points, while the multi-agent lost 1.5 points because the fallbacks recovered 64 failures. In that setting multi-agent leads by +6.1 pp, but the CI [−4.5, +16.7] crosses zero.

**Bug found by the benchmark:** the multi-agent setup escalated all 5 invalid issues. The researcher had correctly flagged them, but "close as invalid" wasn't a legal move at that point. That is fixed in `graph.py`. Re-running only those 5 tasks gives 4/5 closed correctly (`results/sonnet-f0-invalid-fix`), which would put multi-agent at about 97% with no faults. A full re-run is still needed before quoting that number.
