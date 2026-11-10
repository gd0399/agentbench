# Fix #144: monthly compounding wildly overstates interest

branch: `fix/issue-144`

Fixes #144

## Root cause
toolkit/money.py compound_interest (lines 20-22): `r = rate` is not divided by periods_per_year, so the formula is principal*(1+rate)**(n*years) instead of principal*(1+rate/n)**(n*years). For (1000, 0.12, 1, 12) this gives 1000*1.12**12 = 3895.98. Fix: `r = rate / periods_per_year`. The existing test (periods_per_year=1) is unaffected since dividing by 1 changes nothing. No conflict with tests or docs.

## Change
Fix compound_interest to divide the annual rate by periods_per_year (r = rate / periods_per_year). compound_interest(1000, 0.12, 1, 12) now returns 1126.83. Full suite passes (84 tests).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The root cause is fixed. The function used the annual rate as the per-period rate, and `r = rate / periods_per_year` corrects that. The change is a single line and the compounding exponent `n` is untouched.

I checked these cases:
- `compound_interest(1000, 0.12, 1, 12)` returns 1126.83, which matches the issue.
- The default `periods_per_year=1` behaves as before. `(1000, 0.12, 1, 1)` returns 1120.0, and the existing test `(1000, 0.05, 2) == 1102.5` still passes.
- Fractional years work: `(1000, 0.12, 0.5, 2)` returns 1060.0.
- The full suite passes (84 tests), and no existing tests were modified. The new regression test is appropriate.

Notes, none of which block the merge:
- The diff includes `__pycache__/*.pyc` files. Drop them before merging, and consider adding a `.gitignore`.
- `periods_per_year=0` now raises `ZeroDivisionError`. Before, it silently returned the principal. The input is meaningless, but you could add a `ValueError("periods_per_year must be positive")` guard for a clearer message.
- The regression test compares floats with `==`. That is fine here because the result is rounded to 2 places.

<details><summary>Agent trail</summary>

Triage: bug / high / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
