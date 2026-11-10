# Fix #155: day_of_year counts the current month twice

branch: `fix/issue-155`

Fixes #155

## Root cause
toolkit/dates.py line 28, in day_of_year: `for m in range(1, month + 1)` includes the current month's full length in the running total. It should be `range(1, month)` so that only preceding months are summed before adding `day`. For example, March 1, 2023 gives 31+28+31+1 = 91 instead of 31+28+1 = 60. Leap-year handling is fine, because days_in_month handles February correctly. The existing test test_day_of_year_bad only checks the ValueError case, so there is no conflict with the tests.

## Change
Fix day_of_year in toolkit/dates.py to sum only preceding months (range(1, month)) instead of including the current month. The full suite passes (85 tests), including the repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The root cause was `range(1, month + 1)` including the current month. It is now `range(1, month)`. I checked these cases:
- 2023-03-01 gives 60.
- 2023-12-31 gives 365.
- 2024-12-31 gives 366.
- An invalid month still raises ValueError.

The full suite passes (85 tests). No existing tests were modified. The new tests in tests/test_issue_repro.py cover the issue case, Jan 1 and a leap year.

One cleanup before merge: the diff includes compiled `__pycache__/*.pyc` files. Please drop them from the commit and add `__pycache__/` to .gitignore. This doesn't affect the code change, so I'm approving.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
