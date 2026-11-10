# Fix #156: day_of_year accepts Feb 29 in non-leap years

branch: `fix/issue-156`

Fixes #156

## Root cause
toolkit/dates.py day_of_year (lines 24-30) only checks `1 <= day <= 31` (line 25) rather than validating against days_in_month(year, month). So (2023, 2, 29) passes and returns 28+... = 31+29 = 60. The month argument is also not validated up front. It's only checked indirectly through days_in_month for months before `month`, so month=13 or 0 is silently accepted. Fix: validate the month (1..12), then check `day > days_in_month(year, month)` and raise ValueError. Existing tests (day_of_year(2023,3,1)==60, day_of_year(2024,12,31)==366) are unaffected. Repro test is in tests/test_issue_repro.py. The non-leap case fails, and the leap-year Feb 29 case already passes.

## Change
day_of_year now checks day against days_in_month(year, month), which also validates month (1..12), so (2023,2,29) raises ValueError while leap-year Feb 29 still works. Added tests/test_day_of_year_validation.py for invalid month/day cases; full suite passes (94 passed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the hardcoded `day > 31` bound. The patch replaces it with `days_in_month(year, month)`, which handles leap years, the century rules (1900 is not a leap year, 2000 is) and month validation. The source change is one line, and the full suite passes (94 passed). No existing tests were modified. The new tests cover non-leap and leap Feb 29, 30-day months, and out-of-range month and day values.

One behaviour change: month 0 or 13 now raises ValueError. Before, `day_of_year(2023, 0, 1)` returned a bogus value. This is reasonable and is tested.

Before merging, drop the committed `__pycache__/*.pyc` files from the diff and add them to .gitignore. They are test-run artifacts and shouldn't be in the repo.

Optionally, fold `tests/test_issue_repro.py` into `test_day_of_year_validation.py`. The two files overlap.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
