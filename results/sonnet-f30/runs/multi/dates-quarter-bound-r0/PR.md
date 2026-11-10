# Fix #154: quarter_of(12) raises ValueError

branch: `fix/issue-154`

Fixes #154

## Root cause
toolkit/dates.py line 19, in quarter_of: the bounds check is `month < 1 or month > 11`. It should be `month > 12`, as the error message "month must be 1..12" says. December is rejected with ValueError. The formula `(month - 1) // 3 + 1` already returns 4 for 12. No existing test contradicts this. The repro test is tests/test_issue_repro.py.

## Change
Fixed the bounds check in dates.quarter_of from `month > 11` to `month > 12`, so December returns 4. Months 0 and 13 still raise ValueError. All 84 tests pass, including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix addresses the root cause. The upper bound in `quarter_of` was off by one (`> 11`), and it now matches the `> 12` check in `days_in_month`. I ran months 1-12 and got quarters 1,1,1,2,2,2,3,3,3,4,4,4. Months 0, 13 and -1 still raise ValueError. All 84 tests pass, and no existing tests were modified. The new regression test in `tests/test_issue_repro.py` is reasonable.

Nit: the diff includes many `__pycache__/*.pyc` files. Please make sure they aren't committed, and add `__pycache__/` to `.gitignore` if it isn't there already. They are build artifacts, not part of the change. The actual source change is a one-character fix.

<details><summary>Agent trail</summary>

Triage: bug / high / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
