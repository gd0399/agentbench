# Fix #145: compound_interest ignores periods_per_year

branch: `fix/issue-145`

Fixes #145

## Root cause
compound_interest divided the rate by periods_per_year but used n = years as the exponent, so the number of compounding periods was never scaled.

## Change
The compounding exponent now multiplies years by periods_per_year. compound_interest(1000, 0.12, 1, 12) returns 1126.83. The full suite passes (84 tests), including the new repro test.

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
