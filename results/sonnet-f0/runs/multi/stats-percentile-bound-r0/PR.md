# Fix #109: percentile(…, 100) raises ValueError

branch: `fix/issue-109`

Fixes #109

## Root cause
toolkit/stats.py line 52, in percentile(): the range check `if p < 0 or p >= 100:` wrongly rejects p == 100, although the docstring says "p in [0, 100]". It should be `p > 100`. The existing test test_percentile_bounds only checks p=101, so it doesn't conflict with the fix. After the check, the nearest-rank computation is correct for p=100. The rank is -(-100*n//100) = n, so it returns ordered[n-1] = 3. p=0 is handled separately and works. The repro test tests/test_issue_repro.py fails with ValueError on current code.

## Change
Fixed percentile() range check to `p > 100` (was `p >= 100`) so p=100 is accepted and returns the max. Expanded tests/test_issue_repro.py with p=100, p=0, in-between, and p=101/-1 error cases. Full suite: 86 passed.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The range check was off by one: `p >= 100` rejected the documented inclusive upper bound. It is now `p > 100`. The rank calculation already gives n for p=100, so the function returns the max.

I probed p = 0, 1, 25, 50, 75, 99, 100, 33.3 and 99.9 on several inputs, including a single-element list. All results are correct nearest-rank values. The full suite passes (86 tests). The new tests in tests/test_issue_repro.py cover p=100, p=0, in-between values and the p=101 and p=-1 errors. No existing tests were changed or weakened.

One nit: the diff includes committed `__pycache__/*.pyc` files. Please drop them and add `__pycache__/` to `.gitignore` before merging. The code change itself is fine.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
