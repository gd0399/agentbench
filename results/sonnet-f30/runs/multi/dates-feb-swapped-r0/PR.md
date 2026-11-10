# Fix #152: February lengths are swapped

branch: `fix/issue-152`

Fixes #152

## Root cause
toolkit/dates.py line 12, in days_in_month: `return 28 if is_leap_year(year) else 29` has the values swapped. It should be `return 29 if is_leap_year(year) else 28`. is_leap_year is correct and its test passes. day_of_year also uses days_in_month, so it inherits the error.

## Change
Fixed swapped February lengths in dates.days_in_month (29 for leap years, 28 otherwise). Full suite passes (80 tests), including the repro; 2023 gives 28, 1900 gives 28, 2000 gives 29.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The bug was an inverted conditional in `days_in_month`. The patch swaps the two branches, so leap years return 29 and other years return 28. `is_leap_year` is correct, and `day_of_year` picks up the fix through `days_in_month`. All 80 tests pass. The new regression test covers 2024, 2023, 1900 and 2000, so it exercises the century rule as well as the plain leap-year case. No existing tests were modified.

Before merging, drop the `__pycache__/*.pyc` files from the diff. They are build artifacts, not part of the change. They are a leftover of running the tests. A `.gitignore` entry for `__pycache__/` would stop this happening again.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
