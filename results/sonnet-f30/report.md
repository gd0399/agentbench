# Benchmark results — 66 tasks, 132 runs

backend: `llm` · model: `anthropic:claude-sonnet-5-5` (fallbacks: anthropic:claude-haiku-5-5) · router: `llm` · injected fault rate: 30% · repeats: 1

| metric | Single agent | Multi-agent (supervisor) |
|---|---|---|
| success rate | 83.3% (72.6%–90.4%) | 89.4% (79.7%–94.8%) |
| wrong PRs opened (false positives) | 3.0% | 3.0% |
| cost / task (mean) | $0.0247 | $0.0894 |
| cost / successful task | $0.0297 | $0.1000 |
| latency p50 / p95 | 30.6s / 36.2s | 69.6s / 115.3s |
| LLM calls / task | 3.9 | 11.5 |
| tokens in / out per task | 9,290 / 615 | 33,035 / 2,333 |
| handoffs / task | 0.0 | 4.2 |
| fault localisation (top-3 file) | 85.2% | 93.4% |
| triage component accuracy | — | 95.5% |
| injected failures / recovered errors | 35 / 9 | 131 / 64 |
| outcomes | escalated: 9, invalid: 4, pr_opened: 53 | escalated: 5, pr_opened: 61 |

## Paired comparison (same tasks)

- tasks solved by both: 50, neither: 2, only single: 5, only multi: 9
- success difference (multi − single): +6.1 pp, bootstrap 95% CI [-4.5, +16.7] pp, exact McNemar p = 0.424
- cost ratio multi/single: 3.62×
- median latency ratio multi/single: 2.27×

## By difficulty

| group | n | Single agent | Multi-agent (supervisor) |
|---|---|---|---|
| easy | 23 | 82.6% | 100.0% |
| hard | 38 | 84.2% | 94.7% |
| n/a | 5 | 80.0% | 0.0% |

## By category

| group | n | Single agent | Multi-agent (supervisor) |
|---|---|---|---|
| arithmetic | 9 | 100.0% | 100.0% |
| cross-module | 4 | 75.0% | 75.0% |
| edge-case | 9 | 88.9% | 100.0% |
| format | 2 | 50.0% | 100.0% |
| hang | 1 | 100.0% | 100.0% |
| invalid | 5 | 80.0% | 0.0% |
| logic | 22 | 77.3% | 95.5% |
| off-by-one | 10 | 80.0% | 100.0% |
| operator | 4 | 100.0% | 100.0% |
