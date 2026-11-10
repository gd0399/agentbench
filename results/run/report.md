# Benchmark results — 10 tasks, 20 runs

backend: `offline` · router: `rules` · injected fault rate: 0% · repeats: 1

> **Offline backend.** These runs use the deterministic program-repair heuristics, not a language model: they validate the graph, fallbacks and harness. Cost is $0 by construction. Do not read them as evidence about LLM single- vs multi-agent performance.

| metric | Single agent | Multi-agent (supervisor) |
|---|---|---|
| success rate | 60.0% (31.3%–83.2%) | 60.0% (31.3%–83.2%) |
| wrong PRs opened (false positives) | 10.0% | 10.0% |
| cost / task (mean) | $0.0000 | $0.0000 |
| cost / successful task | $0.0000 | $0.0000 |
| latency p50 / p95 | 2.0s / 5.1s | 2.0s / 4.1s |
| LLM calls / task | 1.0 | 4.1 |
| tokens in / out per task | 0 / 0 | 0 / 0 |
| handoffs / task | 0.0 | 5.1 |
| fault localisation (top-3 file) | 100.0% | 100.0% |
| triage component accuracy | — | 90.0% |
| injected failures / recovered errors | 0 / 0 | 0 / 0 |
| outcomes | invalid: 4, pr_opened: 6 | invalid: 4, pr_opened: 6 |

## Paired comparison (same tasks)

- tasks solved by both: 6, neither: 4, only single: 0, only multi: 0
- success difference (multi − single): +0.0 pp, bootstrap 95% CI [+0.0, +0.0] pp, exact McNemar p = 1
- cost ratio: n/a ($0)
- median latency ratio multi/single: 0.97×

## By difficulty

| group | n | Single agent | Multi-agent (supervisor) |
|---|---|---|---|
| easy | 4 | 75.0% | 75.0% |
| hard | 5 | 40.0% | 40.0% |
| n/a | 1 | 100.0% | 100.0% |

## By category

| group | n | Single agent | Multi-agent (supervisor) |
|---|---|---|---|
| arithmetic | 4 | 50.0% | 50.0% |
| cross-module | 1 | 100.0% | 100.0% |
| edge-case | 1 | 100.0% | 100.0% |
| invalid | 1 | 100.0% | 100.0% |
| logic | 2 | 50.0% | 50.0% |
| operator | 1 | 0.0% | 0.0% |
