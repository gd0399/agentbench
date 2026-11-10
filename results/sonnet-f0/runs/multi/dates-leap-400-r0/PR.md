# Fix #150: is_leap_year(2000) is False

branch: `fix/issue-150`

Fixes #150

## Root cause
toolkit/dates.py line 5, is_leap_year: the condition is `year % 4 == 0 and (year % 100 != 0 or year % 400 != 0)`. The last clause should be `year % 400 == 0`. As written, 2000 returns False. 1900 also wrongly returns True, and so does every century year not divisible by 400. This also makes days_in_month and day_of_year wrong for those years.

## Change
Fix is_leap_year in toolkit/dates.py: last clause changed from `year % 400 != 0` to `year % 400 == 0`. 2000 is now a leap year and 1900 is not. days_in_month and day_of_year are correct for both years (Feb 1900 = 28, Feb 2000 = 29; Dec 31 is day 365 in 1900 and day 366 in 2000). Full suite passes (85 passed), including the repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. It changes `year % 400 != 0` to `year % 400 == 0` in `is_leap_year`, which was the root cause. I checked it against `calendar.isleap` for years 1 to 4999 and every year matches. `days_in_month` and `day_of_year` get the right answers through it. The full suite passes (85 tests). The new tests in `tests/test_issue_repro.py` cover 2000, 1900, 2024 and 2023, and no existing tests were changed.

Before merging, drop the committed `__pycache__/*.pyc` files from the diff, and add `__pycache__/` to `.gitignore` if it isn't there already. They are build artifacts and don't belong in the patch. This doesn't affect the code change itself.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
