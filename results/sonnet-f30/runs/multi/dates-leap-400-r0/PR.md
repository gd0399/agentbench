# Fix #150: is_leap_year(2000) is False

branch: `fix/issue-150`

Fixes #150

## Root cause
toolkit/dates.py line 5, is_leap_year: `year % 4 == 0 and (year % 100 != 0 or year % 400 != 0)`. The last clause should be `year % 400 == 0`, not `!= 0`. As written, any century year not divisible by 400 (1900, 2100) wrongly returns True, and every year divisible by 400 (2000, 2400) wrongly returns False. The triage guess, that the 400 exception is omitted, is slightly off: the exception is present but inverted. The issue also misses the 1900/2100 -> True side effect. Correct: `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`. No existing tests or docs conflict: the 2024/2023 tests pass either way.

## Change
Fix inverted 400-year clause in is_leap_year (`year % 400 == 0`), so 2000/2400 are leap and 1900/2100 are not. All 89 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The one-character change (`year % 400 != 0` to `year % 400 == 0`) fixes the root cause. I checked `is_leap_year` against `calendar.isleap` for years 1 to 2999 and every year matched. All 89 tests pass. No existing tests were modified. The new regression test in tests/test_issue_repro.py covers 2000, 1900, 2100 and 2400. Before merging, drop the committed `__pycache__/*.pyc` files from the diff and add `__pycache__/` to .gitignore. They are build artifacts and shouldn't be in the patch. You could also fold the regression test into tests/test_toolkit.py instead of keeping a separate "issue_repro" file.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
