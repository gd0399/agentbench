# Fix #109: percentile(…, 100) raises ValueError

branch: `fix/issue-109`

Fixes #109

## Root cause
toolkit/stats.py line 52, in percentile(): the guard `if p < 0 or p >= 100` wrongly rejects p == 100, although the docstring says p is in [0, 100]. It should be `p > 100`. The rank computation below (line 57) is already correct for p=100: rank = len(values), so it returns the last element. The existing test test_percentile_bounds only checks p=101, so changing the guard doesn't conflict with it.

## Change
Fixed the percentile() bounds guard in toolkit/stats.py from `p >= 100` to `p > 100`, so p=100 returns the last element. p=0 already returned the first element. I added regression tests for p=100 and negative p. All 86 tests pass, including the repro and test_percentile_bounds (p=101 still raises).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The guard `p >= 100` rejected the valid upper bound, which contradicts the docstring "p in [0, 100]". Changing it to `p > 100` fixes the root cause. The nearest-rank formula already gives the right answer at p=100: rank = len, so it returns the last element.

I probed p = 0, 1, 50, 99, 99.9 and 100 on 1-, 3- and 5-element lists. All results were sensible. p=101 and p=-1 still raise ValueError. All 86 tests pass. No existing tests were modified or removed; the patch only adds tests.

Nits, not blocking:
- The diff includes committed `__pycache__/*.pyc` files. Drop them before merging and add `__pycache__/` to `.gitignore`.
- `tests/test_issue_repro.py` duplicates `test_percentile_hundred` in `test_toolkit.py`. Consider removing it.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
