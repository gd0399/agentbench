# Fix #144: monthly compounding wildly overstates interest

branch: `fix/issue-144`

Fixes #144

## Root cause
The per-period rate used the full annual rate (r = rate) instead of rate / periods_per_year, while the exponent was multiplied by periods_per_year.

## Change
compound_interest now divides the annual rate by periods_per_year; (1000, 0.12, 1, 12) gives 1126.83. Also rejects periods_per_year <= 0. Added tests/test_issue_repro.py; full suite passes.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: ? / ? / component `?`
Handoffs: single agent
Recovered errors: 0
</details>

_Opened automatically by agentbench._
