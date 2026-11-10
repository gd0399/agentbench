# Fix #149: 2024 is not treated as a leap year

branch: `fix/issue-149`

Fixes #149

## Root cause
toolkit/dates.py line 5, is_leap_year: the expression `year % 4 == 0 and (year % 100 != 0 and year % 400 == 0)` has the inner `and` where it should be `or`. A year that isn't divisible by 400 can never pass, so 2024 returns False. The correct expression is `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`. days_in_month(2024, 2) returns 28 for the same reason, and day_of_year is also affected. No existing test or doc contradicts the expected behaviour.

## Change
Fixed is_leap_year in toolkit/dates.py: changed inner `and` to `or` so years divisible by 4 but not 100 (e.g. 2024) are leap years. This also fixes days_in_month and day_of_year. Full suite passes (83 passed), including the repro tests. 1900=False, 2000=True, 2024=True, 2023=False.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line change in `is_leap_year` fixes the root cause. The old condition `year % 100 != 0 and year % 400 == 0` could never be true for a year that is a multiple of 4 but not of 400. The new condition is the correct Gregorian rule.

I ran the full suite: 83 passed. I also checked these years directly:
- 1900 and 2100 return False.
- 2000, 2400, 1600, 2024 and 4 return True.
- 2023 returns False.
- `days_in_month(2024, 2)` is 29 and `days_in_month(1900, 2)` is 28.

The new tests in `tests/test_issue_repro.py` are additive. No existing tests were changed or weakened.

Before merge, please drop the `__pycache__/*.pyc` files from the diff. They are build artifacts and shouldn't be committed. Consider adding `__pycache__/` to `.gitignore`. This is hygiene only and doesn't affect the fix.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
