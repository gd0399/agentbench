# Fix #154: quarter_of(12) raises ValueError

branch: `fix/issue-154`

Fixes #154

## Root cause
toolkit/dates.py line 19, in quarter_of: the validation is `if month < 1 or month > 11`. It is off by one, so month 12 raises ValueError("month must be 1..12"). The bound should be `month > 12`, as in days_in_month. The formula on line 21, (month-1)//3+1, already returns 4 for 12. No existing test or docstring contradicts the fix.

## Change
Fixed off-by-one in quarter_of validation (month > 11 -> month > 12) in toolkit/dates.py; quarter_of(12) now returns 4. Full suite passes (85 passed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The upper bound in `quarter_of` was off by one, and changing it to `month > 12` matches `days_in_month`. I checked months 1–12 and got [1,1,1,2,2,2,3,3,3,4,4,4]. 0 and 13 still raise ValueError. The full suite passes (85 tests). The new tests in `tests/test_issue_repro.py` are additive, and no existing tests were changed.

One cleanup before merge: the diff includes `__pycache__/*.pyc` files. Please drop them and add `__pycache__/` to `.gitignore` if it isn't already there. I'm not blocking on this.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
