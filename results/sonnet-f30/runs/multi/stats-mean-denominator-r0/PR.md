# Fix #101: mean() gives the wrong average

branch: `fix/issue-101`

Fixes #101

## Root cause
toolkit/stats.py line 7, mean() returns sum(values) / (len(values) - 1) instead of / len(values). This is an off-by-one divisor, so [1,2,3,4] gives 10/3. It also affects variance() (which calls mean) and report.py's mean. A single-element list would raise ZeroDivisionError.

## Change
Fixed off-by-one in stats.mean(): divide by len(values) instead of len(values)-1. report.py has no separate mean (it calls stats.mean), so it needed no change. Empty-list ValueError is kept. Added regression tests for mean([1,2,3,4]), mean([5]) and variance. All 82 tests pass, including tests/test_issue_repro.py.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The root cause was `mean()` dividing by `len(values) - 1`, and it now divides by `len(values)`. The empty-list ValueError is kept. `variance()` calls `mean()`, so it was also wrong before and is now correct. The new variance test checks both the sample and population forms. `report.py` only calls `stats.mean`, so it needs no change. I found no other off-by-one of the same kind in the repo. All 82 tests pass, and no existing tests were changed or weakened.

Nits, not blocking:
- The diff includes generated `__pycache__/*.pyc` files. Drop them before merging, or add them to `.gitignore`.
- `test_mean_basic` appears in both `tests/test_issue_repro.py` and `tests/test_toolkit.py`. One copy is enough.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
