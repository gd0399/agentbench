# Fix #156: day_of_year accepts Feb 29 in non-leap years

branch: `fix/issue-156`

Fixes #156

## Root cause
day_of_year only checked 1 <= day <= 31 regardless of month and year.

## Change
day_of_year now validates the day against days_in_month(year, month), so Feb 29 in a non-leap year raises ValueError. It also rejects other invalid dates such as Apr 31, and an out-of-range month. I added tests in tests/test_issue_repro.py, and the full suite passes (86 tests).

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
