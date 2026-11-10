# Fix #145: compound_interest ignores periods_per_year

branch: `fix/issue-145`

Fixes #145

## Root cause
toolkit/money.py compound_interest, line 21: `n = years` should be `n = years * periods_per_year`. The rate is already divided by periods_per_year on line 20, but the exponent is not multiplied by it. So 1000*(1.01)^1 = 1010.0 instead of 1000*(1.01)^12 = 1126.83. The default periods_per_year=1 case (existing test, 1102.5) is unaffected by the fix.

## Change
Fixed compound_interest exponent: n = years * periods_per_year (rate was already divided by periods_per_year). All 85 tests pass, including the repro test; default behavior unchanged.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line fix is correct and addresses the root cause. The rate was already divided by periods_per_year, but the exponent wasn't multiplied by it. It is now `n = years * periods_per_year`.

I ran the issue repro, and `compound_interest(1000, 0.12, 1, 12)` returns 1126.83. The default case `(1000, 0.05, 2)` still returns 1102.5, and a fractional-year case also works. All 85 tests pass, and no existing tests were modified. The new tests in tests/test_issue_repro.py are reasonable.

Before merging, please drop the committed `__pycache__/*.pyc` files from the diff. They are build artifacts, and a `.gitignore` entry would keep them out. This doesn't affect the code change. You could also move the two new tests into tests/test_toolkit.py next to the existing compound_interest test.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
