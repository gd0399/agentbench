# Fix #145: compound_interest ignores periods_per_year

branch: `fix/issue-145`

Fixes #145

## Root cause
toolkit/money.py compound_interest (line 21): `n = years` should be `n = years * periods_per_year`. The rate is divided by periods_per_year (line 20) but the exponent is not multiplied by it, so only `years` compounding periods are applied (1000*1.01 = 1010.0). Fix: n = years * periods_per_year. The existing test (1000, 0.05, 2) uses the default periods_per_year=1, so it is unaffected.

## Change
Fixed compound_interest in toolkit/money.py: the exponent is now years * periods_per_year instead of just years. compound_interest(1000, 0.12, 1, 12) now returns 1126.83. The full suite passes (84 tests), including the repro test and the existing default-period test. I left tests/test_issue_repro.py where it is and didn't merge it into the main money tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line fix in toolkit/money.py is correct and minimal. The exponent is now years * periods_per_year, and the rate is still divided by periods_per_year. It fixes the root cause rather than the specific input. I checked these cases:
- compound_interest(1000, 0.12, 1, 12) returns 1126.83, matching the issue.
- compound_interest(1000, 0.05, 2, 4) returns 1104.49, which is correct.
- compound_interest(1000, 0.05, 0.5, 2) returns 1025.0, which is correct.
- The default periods_per_year=1 behaviour is unchanged, and the existing test at tests/test_toolkit.py:202 still passes.
- All 84 tests pass, and no existing tests were modified.

Nits to clean up before merging (not blocking):
1. The diff includes __pycache__/*.pyc files. These are build artifacts, so drop them from the commit and consider adding a .gitignore entry.
2. The new test lives in tests/test_issue_repro.py. I'd move it into tests/test_toolkit.py next to the existing compound_interest test. Adding a case with a non-default periods_per_year and a fractional-years case would also help.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
