# Benchmark results — 66 tasks, 132 runs

backend: `llm` · model: `anthropic:claude-sonnet-5-5` (fallbacks: anthropic:claude-haiku-5-5) · router: `llm` · injected fault rate: 0% · repeats: 1

| metric | Single agent | Multi-agent (supervisor) |
|---|---|---|
| success rate | 97.0% (89.6%–99.2%) | 90.9% (81.6%–95.8%) |
| wrong PRs opened (false positives) | 3.0% | 3.0% |
| cost / task (mean) | $0.0290 | $0.1121 |
| cost / successful task | $0.0300 | $0.1233 |
| latency p50 / p95 | 30.8s / 36.1s | 75.7s / 118.1s |
| LLM calls / task | 4.6 | 13.6 |
| tokens in / out per task | 10,954 / 714 | 41,342 / 2,940 |
| handoffs / task | 0.0 | 4.1 |
| fault localisation (top-3 file) | 100.0% | 100.0% |
| triage component accuracy | — | 95.5% |
| injected failures / recovered errors | 0 / 0 | 0 / 0 |
| outcomes | invalid: 4, pr_opened: 62 | escalated: 4, pr_opened: 62 |

## Paired comparison (same tasks)

- tasks solved by both: 60, neither: 2, only single: 4, only multi: 0
- success difference (multi − single): -6.1 pp, bootstrap 95% CI [-12.1, -1.5] pp, exact McNemar p = 0.125
- cost ratio multi/single: 3.86×
- median latency ratio multi/single: 2.46×

## By difficulty

| group | n | Single agent | Multi-agent (supervisor) |
|---|---|---|---|
| easy | 23 | 100.0% | 100.0% |
| hard | 38 | 97.4% | 97.4% |
| n/a | 5 | 80.0% | 0.0% |

## By category

| group | n | Single agent | Multi-agent (supervisor) |
|---|---|---|---|
| arithmetic | 9 | 100.0% | 100.0% |
| cross-module | 4 | 100.0% | 100.0% |
| edge-case | 9 | 100.0% | 100.0% |
| format | 2 | 100.0% | 100.0% |
| hang | 1 | 100.0% | 100.0% |
| invalid | 5 | 80.0% | 0.0% |
| logic | 22 | 95.5% | 95.5% |
| off-by-one | 10 | 100.0% | 100.0% |
| operator | 4 | 100.0% | 100.0% |
