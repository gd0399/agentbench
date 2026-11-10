# Fix #106: sample variance uses the population formula

branch: `fix/issue-106`

Fixes #106

## Root cause
toolkit/stats.py variance(), lines 43-45: the `if sample:` branch returns `total / n`, identical to the population branch. It should return `total / (n - 1)`. The function already has `sample=True` as the default and already raises ValueError for n<2 when sample is true, so only the divisor is wrong. The existing tests (population variance with sample=False == 4, and variance([1]) raising) stay consistent with the fix. The issue's request does not conflict with the tests or docs.

## Change
Fixed sample variance in toolkit/stats.py to divide by (n - 1) instead of n. The population branch (sample=False) and the n<2 ValueError are unchanged. All 85 tests pass, including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The sample branch of `variance` now divides by `n - 1`, which is the root cause. The population branch (`sample=False`) and the `n < 2` ValueError are unchanged. Nothing else in the repo calls `variance`, and `report.py` only uses mean and median, so no callers are affected. All 85 tests pass. The existing tests were not modified. The new `tests/test_issue_repro.py` covers the issue's example and checks that the population branch is unchanged.

Before merging, drop the `__pycache__/*.pyc` files from the commit. They are build artifacts, not part of the fix, and should be gitignored.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
