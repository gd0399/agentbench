# Fix #110: percentile() is off by one

branch: `fix/issue-110`

Fixes #110

## Root cause
toolkit/stats.py line 58 in percentile(): the nearest-rank value `rank = ceil(p*n/100)` is 1-based, but the code uses it directly as a 0-based index (`ordered[int(rank)]`). It should be `ordered[int(rank) - 1]`. For [15,20,35,40,50], p=40 gives rank 2, which returns ordered[2]=35 instead of ordered[1]=20. The same bug makes p=100 raise IndexError (rank=n). The p==0 special case is correct and the existing tests don't conflict with the fix.

## Change
Fix off-by-one in percentile(): convert 1-based nearest rank to 0-based index (ordered[int(rank) - 1]). Fixes p=40 -> 20 and p=100 IndexError; full suite passes (83).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is that nearest-rank is 1-based and the code indexed the list with it as if it were 0-based. Changing it to `ordered[int(rank) - 1]` is the correct and minimal fix.

I checked it against the standard nearest-rank definition. For [15, 20, 35, 40, 50] it gives:
- p=0 → 15
- p=20 → 15
- p=25 → 20
- p=40 → 20
- p=50 → 35
- p=100 → 50
- a single-element list at p=100 → 7

The old code raised IndexError at p=100. That is now fixed too. The p=0 branch still handles rank 0, so it never produces index -1. The full suite passes (83 tests), and the existing tests were not modified. The new regression tests in tests/test_issue_repro.py are appropriate.

Nit: the diff includes committed `__pycache__/*.pyc` files. Please drop them before merging and add `__pycache__/` to .gitignore. You could also move the two new tests into tests/test_toolkit.py rather than keeping a separate repro file.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
