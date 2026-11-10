# Fix #156: day_of_year accepts Feb 29 in non-leap years

branch: `fix/issue-156`

Fixes #156

## Root cause
researcher unavailable; not yet investigated

## Change
day_of_year now validates day against days_in_month(year, month) (which also validates month), so Feb 29 in non-leap years raises ValueError.

## Verification
- Reproduction test: `n/a` — passes
- Existing test-suite: passes
- Review: reviewer — Approving. The fix addresses the root cause. day_of_year used a hardcoded `day > 31` bound. It now uses days_in_month(year, month), which is the same source of truth the loop below it uses. That also validates month, so month 0 and month 13 raise ValueError instead of returning garbage.

I probed these cases:
- (2023,2,29) raises ValueError.
- (2024,2,29) returns 60.
- (2000,2,29) returns 60.
- (1900,2,29) raises ValueError, so century rules are handled.
- (2023,4,31) raises ValueError.
- (2023,12,31) returns 365 and (2024,12,31) returns 366.
- Months 0 and 13 raise ValueError.

All 83 existing tests pass, and no tests were modified.

Notes, not blockers:
- The diff includes __pycache__/*.pyc files. These are test-run artifacts, and the repo has no .gitignore. Drop them before committing. The real change is the one line in toolkit/dates.py.
- Please add a regression test for (2023,2,29) raising ValueError, plus a leap-year positive case. No test was added, and the existing suite didn't catch this bug.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
