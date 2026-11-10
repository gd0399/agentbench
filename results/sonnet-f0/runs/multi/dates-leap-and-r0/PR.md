# Fix #149: 2024 is not treated as a leap year

branch: `fix/issue-149`

Fixes #149

## Root cause
toolkit/dates.py line 5, is_leap_year: `year % 4 == 0 and (year % 100 != 0 and year % 400 == 0)` uses `and` where `or` is needed. The inner clause needs both `year % 100 != 0` and `year % 400 == 0`, and no year can satisfy both, so the function always returns False. The correct expression is `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`. This also makes days_in_month(leap_year, 2) return 28 instead of 29. The repro test fails for 2024, 2000 and 1996, and passes for 1900, 2023 and 2100. No existing tests or docs contradict the fix.

## Change
Fixed is_leap_year in toolkit/dates.py by changing `and` to `or` in the century clause: `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`. Added February days_in_month tests (2024/2000 -> 29, 1900/2023 -> 28) to tests/test_issue_repro.py. The full suite passes (91 passed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The fix addresses the root cause. The century clause had `and` where it needed `or`, so only years divisible by 400 could ever be leap years. The one-line change in `toolkit/dates.py` is minimal. I compared `is_leap_year` against `calendar.isleap` for years 1 to 4999 and they match everywhere. `days_in_month(2024, m)` gives 29 for February. The full suite passes (91 tests). No existing tests were modified. The new `tests/test_issue_repro.py` covers 2024, 2000, 1900, 2100, 1996 and 2023, and checks February in `days_in_month`.

Before merging, please drop the `__pycache__/*.pyc` files from the diff. They are artifacts of running the tests, and they are not part of the change. Adding `__pycache__/` to `.gitignore` would stop this recurring. The change itself needs no further work.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
