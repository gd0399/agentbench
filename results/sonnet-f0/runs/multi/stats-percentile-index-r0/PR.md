# Fix #110: percentile() is off by one

branch: `fix/issue-110`

Fixes #110

## Root cause
toolkit/stats.py line 58, percentile(): line 57 correctly computes the 1-based nearest rank, ceil(p*n/100). Line 58 then uses it as a 0-based index with `ordered[int(rank)]`, so it needs `ordered[int(rank) - 1]`. For p=40 and n=5 the rank is 2, so the code returns ordered[2]=35 instead of ordered[1]=20. The same bug makes p=100 raise IndexError, because rank=n. The existing p=0 special case on line 55 returns ordered[0] and is unaffected. The docstring says "Nearest-rank", which agrees with the expected 20, so the issue doesn't conflict with the docs or tests. The repro tests are in tests/test_issue_repro.py.

## Change
Fix off-by-one in stats.percentile(): use ordered[int(rank) - 1] since nearest-rank is 1-based. p=40 now returns 20 and p=100 returns 50 instead of raising IndexError. Added regression tests; all 86 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and addresses the root cause. Nearest-rank is 1-based, so `ordered[int(rank) - 1]` is the right index. The p=0 special case already handles the lower bound. For any p > 0, rank is at least 1, so the index can't go negative. For p = 100, rank equals n, so the old IndexError is gone. I ran the suite and all 86 tests pass. No existing tests were modified or weakened, and the new tests check the right values: p=40 gives 20, and p=100 gives 50.

Cleanup to do before merging (not blocking):
- Remove the committed `__pycache__/*.pyc` files. They're build artifacts, and a `.gitignore` entry would stop them coming back.
- `tests/test_issue_repro.py` duplicates the new tests in `tests/test_toolkit.py`. `test_percentile_100` is defined in both files. Delete the repro file and keep the tests in `test_toolkit.py`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
