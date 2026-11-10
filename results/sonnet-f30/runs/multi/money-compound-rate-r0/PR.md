# Fix #144: monthly compounding wildly overstates interest

branch: `fix/issue-144`

Fixes #144

## Root cause
toolkit/money.py compound_interest (lines 20-22): `r = rate` is used undivided, so the formula is principal*(1+rate)**(periods*years). It should use r = rate / periods_per_year. With 12 periods this gives 1000*1.12**12 = 3895.98 instead of 1000*(1+0.12/12)**12 = 1126.83. The exponent n = periods_per_year*years is correct. The existing test (1000, 0.05, 2) uses the default periods=1, so it still passes after the fix. It does not conflict with the tests.

## Change
compound_interest now divides the annual rate by periods_per_year (r = rate / periods_per_year). compound_interest(1000, 0.12, 1, 12) now gives 1126.83. The full suite passes (84 tests), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line fix in compound_interest is correct. The root cause was that the annual rate was applied once per period, and it is now divided by periods_per_year. I checked these cases:
- (1000, 0.12, 1, 12) returns 1126.83, which matches the issue.
- The existing annual case (1000, 0.05, 2) still returns 1102.5.
- A fractional-year case, (1000, 0.12, 0.5, 12), returns 1061.52, which is plausible.
- All 84 tests pass.
- The existing tests were not modified. The coder only added tests/test_issue_repro.py, a small regression test.

Before merging, please:
1. Drop the committed __pycache__/*.pyc files from the patch. They are build artifacts and add noise. A .gitignore entry for __pycache__/ would help.
2. Optionally, validate periods_per_year. Passing 0 used to return the principal and now raises a bare ZeroDivisionError. Raising ValueError("periods_per_year must be positive"), like the existing years check, would be cleaner. This is not blocking.

<details><summary>Agent trail</summary>

Triage: bug / high / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
