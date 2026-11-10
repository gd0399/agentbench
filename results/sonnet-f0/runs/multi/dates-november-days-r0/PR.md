# Fix #151: November has 31 days

branch: `fix/issue-151`

Fixes #151

## Root cause
toolkit/dates.py line 13, in days_in_month: the 30-day month tuple is `(4, 6, 9)` and omits November (11). Month 11 falls through to `return 31` on line 15. Fix: change the tuple to `(4, 6, 9, 11)`. The repro test tests/test_issue_repro.py covers all 12 months plus leap February. Only the month 11 case fails. day_of_year is affected downstream for dates after November, because it sums days_in_month.

## Change
Added November (11) to the 30-day months tuple in dates.days_in_month. The full suite passes (95 tests), including the repro test's month 11 case; day_of_year tests still pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The fix is correct and minimal. The root cause was November missing from the 30-day tuple in `days_in_month`, and the one-line change fixes it for every year, not just the repro input. `day_of_year` calls `days_in_month`, so it now returns correct values for dates after November too. The full suite passes (95 tests). The new `tests/test_issue_repro.py` checks all 12 months for 2023 plus leap February. No existing tests were changed.

Before committing, drop the `__pycache__/*.pyc` files that appear in the diff. They are build artifacts, not part of the fix. A `.gitignore` entry for `__pycache__/` would prevent this.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
