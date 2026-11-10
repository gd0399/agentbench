# Fix #153: March is reported as Q2

branch: `fix/issue-153`

Fixes #153

## Root cause
toolkit/dates.py line 21, quarter_of returns `month // 3 + 1`. This is off by one for months 3, 6, 9 and 12, which return 2, 3, 4 and 5. Month 12 returns 5, which is not a valid quarter. The correct expression is `(month - 1) // 3 + 1`. The repro test tests/test_issue_repro.py covers all 12 months. Months 3, 6, 9 and 12 fail and the other 8 pass. No existing test or doc covers quarter_of, so the issue does not conflict with documented behaviour.

## Change
Fixed quarter_of in toolkit/dates.py to use (month - 1) // 3 + 1, so months 3, 6, 9 and 12 now return 1, 2, 3 and 4. Added regression tests to tests/test_toolkit.py covering all 12 months and the invalid months 0 and 13. The full suite passes (108 tests), including tests/test_issue_repro.py.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was `month // 3 + 1`, which is off by one for months 3, 6, 9 and 12. `(month - 1) // 3 + 1` is the correct formula. The range validation is unchanged. No other code uses the same pattern. All 108 tests pass, and the new tests cover all 12 months plus the invalid months 0 and 13. No existing tests were modified.

Before merging, please clean up two things:
- The diff includes `__pycache__/*.pyc` files. Drop them from the commit and add them to `.gitignore`.
- `tests/test_issue_repro.py` duplicates `test_quarter_of_all_months` in `tests/test_toolkit.py`. Keep only one of them.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
