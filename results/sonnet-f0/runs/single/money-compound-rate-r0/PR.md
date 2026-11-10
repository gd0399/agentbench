# Fix #144: monthly compounding wildly overstates interest

branch: `fix/issue-144`

Fixes #144

## Root cause
The periodic rate was set to the full annual rate (r = rate) instead of rate / periods_per_year, while the number of periods was multiplied by periods_per_year.

## Change
compound_interest now divides the annual rate by periods_per_year, and rejects non-positive periods_per_year. Monthly 12% on 1000 for 1 year gives 1126.83. Added a repro test, and the full suite passes.

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
