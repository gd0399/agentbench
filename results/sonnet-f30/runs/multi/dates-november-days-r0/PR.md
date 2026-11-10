# Fix #151: November has 31 days

branch: `fix/issue-151`

Fixes #151

## Root cause
toolkit/dates.py line 13, in days_in_month: the 30-day months tuple is `(4, 6, 9)` and omits 11 (November). November falls through to `return 31` on line 15. Fix: use `(4, 6, 9, 11)`. This also makes day_of_year wrong for dates after November, and it accepts day 31 for November.

## Change
Added November (11) to the 30-day months tuple in dates.days_in_month. This also fixes day_of_year for December and rejects Nov 31. Added tests/test_dates_november.py covering all month lengths, Nov 31 rejection and December day_of_year. Full suite passes (86 tests).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. It adds 11 to the 30-day tuple in `days_in_month`, which was the root cause. `day_of_year` is the only other caller, and it now gives the right answer for December and rejects Nov 31. The full suite passes (86 tests). No existing tests were modified, and the new tests cover all 12 month lengths, Nov 31 rejection and December day_of_year.

One nit: the diff includes many `__pycache__/*.pyc` files. Drop them before merging and add `__pycache__/` to `.gitignore`. They are build artifacts and not part of the change.

<details><summary>Agent trail</summary>

Triage: bug / high / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
