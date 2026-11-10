# Fix #110: percentile() is off by one

branch: `fix/issue-110`

Fixes #110

## Root cause
toolkit/stats.py line 58 in percentile(): the nearest-rank rank (computed on line 57 as ceil(p*n/100), 1-based) is used directly as a 0-based list index (`ordered[int(rank)]`). It should be `ordered[int(rank) - 1]`. For p=40, n=5 the rank is 2, but ordered[2] is 35 instead of 20. For p=100 the rank is 5, which raises IndexError. The p==0 special case (returns ordered[0]) is unaffected and the existing tests still pass. The repro is tests/test_issue_repro.py, which has two failing tests: the issue example and p=100.

## Change
Fix percentile() off-by-one: nearest-rank is 1-based, so index with ordered[int(rank) - 1]. Fixes the issue example (returns 20) and p=100 IndexError. All 83 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is correct. The rank is computed as ceil(p*n/100), which is 1-based nearest-rank, but it was used as a 0-based index. Changing the lookup to `ordered[int(rank) - 1]` fixes that, and it also fixes the IndexError at p=100.

I ran the function on [15,20,35,40,50] and the results match nearest-rank:
- p=25 gives 20, p=40 gives 20, p=50 gives 35, p=100 gives 50.
- p=0 still returns the minimum through the existing special case.
- A single-element list works at p=100 and at a tiny p.
- [1,2,3,4] gives 2 at p=50 and 3 at p=75.

All 83 tests pass. No existing tests were modified, and the new regression tests cover the issue example and p=100.

The diff includes `__pycache__/*.pyc` files. Please keep them out of the commit and add them to `.gitignore`. They don't appear in the repo file listing, so this looks like a diff artifact and doesn't block the merge.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
