# Fix #156: day_of_year accepts Feb 29 in non-leap years

branch: `fix/issue-156`

Fixes #156

## Root cause
day_of_year only checked 1 <= day <= 31 instead of using the month's actual length for the given year.

## Change
day_of_year now validates day against days_in_month(year, month), so (2023, 2, 29) raises ValueError. It also now rejects an invalid month. I added repro tests, and the full suite passes.

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
