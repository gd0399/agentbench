# Fix #155: day_of_year counts the current month twice

branch: `fix/issue-155`

Fixes #155

## Root cause
toolkit/dates.py day_of_year, line 28: `for m in range(1, month + 1)` includes the current month's full length in the running total, and then `day` is added. It should be `range(1, month)`. Leap-year handling is fine, since days_in_month handles Feb correctly. The same off-by-one affects every date (e.g. Jan 1 gives 32).

## Change
Fixed day_of_year in toolkit/dates.py to sum only the months before the given month (range(1, month)). Added regression tests in tests/test_day_of_year.py covering a leap year, a non-leap year end and Jan 1. All 87 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → verifier → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
