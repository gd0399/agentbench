# Benchmark results — 5 tasks, 5 runs

backend: `llm` · model: `anthropic:claude-sonnet-5-5` (fallbacks: anthropic:claude-haiku-5-5) · router: `llm` · injected fault rate: 0% · repeats: 1

| metric | Multi-agent (supervisor) |
|---|---|
| success rate | 80.0% (37.6%–96.4%) |
| wrong PRs opened (false positives) | 20.0% |
| cost / task (mean) | $0.0544 |
| cost / successful task | $0.0681 |
| latency p50 / p95 | 16.9s / 29.0s |
| LLM calls / task | 7.6 |
| tokens in / out per task | 18,166 / 1,811 |
| handoffs / task | 2.4 |
| fault localisation (top-3 file) | — |
| triage component accuracy | 100.0% |
| injected failures / recovered errors | 0 / 0 |
| outcomes | invalid: 4, pr_opened: 1 |

## By difficulty

| group | n | Multi-agent (supervisor) |
|---|---|---|
| n/a | 5 | 80.0% |

## By category

| group | n | Multi-agent (supervisor) |
|---|---|---|
| invalid | 5 | 80.0% |
