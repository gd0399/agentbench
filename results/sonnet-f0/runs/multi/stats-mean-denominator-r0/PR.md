# Fix #101: mean() gives the wrong average

branch: `fix/issue-101`

Fixes #101

## Root cause
toolkit/stats.py line 7, in mean(): `return sum(values) / (len(values) - 1)` divides by n-1 instead of n (sample-variance style off-by-one). Should be `sum(values) / len(values)`. This also corrupts variance() (line 41 uses mean()) and report.py's mean. Note that a single-element list would raise ZeroDivisionError. No existing test or docs contradict the expected behaviour (only test_mean_empty exists).

## Change
Fixed mean() in toolkit/stats.py to divide by len(values) instead of len(values)-1. Added regression tests (mean([1,2,3,4])==2.5, mean([5])==5). variance() now gives 1.667 (sample) and 1.25 (population), and report.summarize gives mean 2.5. Full suite passes (81 passed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the `len(values) - 1` divisor in `mean()`, and the patch changes it to `len(values)`. I ran the suite and all 81 tests pass. The only other caller of `mean()` is `variance()`, which already divides by `n - 1` or `n` itself, so it is unaffected. `report.summarize` now gets the correct mean. The existing `test_mean_empty` is unchanged, and no existing tests were weakened. The new tests check the issue's input and a single-element list.

Two nits to clean up before merging:
- The diff includes `__pycache__/*.pyc` files. These are test-run artifacts and should be dropped from the commit, or `__pycache__/` added to `.gitignore`.
- `tests/test_issue_repro.py` repeats `test_mean_basic`, which is already in `tests/test_toolkit.py`. Delete the duplicate file.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
