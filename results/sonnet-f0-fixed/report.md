# Benchmark results — 66 tasks, 66 runs

backend: `llm` · model: `anthropic:claude-sonnet-5-5` (fallbacks: anthropic:claude-haiku-5-5) · router: `llm` · injected fault rate: 0% · repeats: 1

| metric | Multi-agent (supervisor) |
|---|---|
| success rate | 33.3% (23.2%–45.3%) |
| wrong PRs opened (false positives) | 0.0% |
| cost / task (mean) | $0.0410 |
| cost / successful task | $0.1229 |
| latency p50 / p95 | 3.0s / 30.4s |
| LLM calls / task | 5.2 |
| tokens in / out per task | 15,098 / 1,078 |
| handoffs / task | 4.1 |
| fault localisation (top-3 file) | 47.5% |
| triage component accuracy | 95.5% |
| injected failures / recovered errors | 0 / 209 |
| outcomes | escalated: 44, pr_opened: 22 |

## By difficulty

| group | n | Multi-agent (supervisor) |
|---|---|---|
| easy | 23 | 43.5% |
| hard | 38 | 31.6% |
| n/a | 5 | 0.0% |

## By category

| group | n | Multi-agent (supervisor) |
|---|---|---|
| arithmetic | 9 | 44.4% |
| cross-module | 4 | 50.0% |
| edge-case | 9 | 44.4% |
| format | 2 | 0.0% |
| hang | 1 | 0.0% |
| invalid | 5 | 0.0% |
| logic | 22 | 36.4% |
| off-by-one | 10 | 30.0% |
| operator | 4 | 25.0% |
