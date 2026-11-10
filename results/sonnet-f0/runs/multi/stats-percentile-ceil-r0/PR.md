# Fix #108: percentile() rounds the rank down instead of up

branch: `fix/issue-108`

Fixes #108

## Root cause
toolkit/stats.py line 57: `rank = p * len(ordered) // 100` uses floor division, so the nearest-rank rank is floored instead of ceil(p*n/100). For p=30, n=5: 150//100 = 1 -> ordered[0]=15, but ceil(1.5)=2 -> 20. Fix: rank = math.ceil(p * len(ordered) / 100) (or -(-p*n // 100) to stay in integer arithmetic; beware float p). Line 58 `int(rank) - 1` indexing is fine. Existing tests (p=0, 40, 100) pass because those ranks are exact integers, so the fix doesn't conflict with them.

## Change
percentile() now uses nearest-rank ceil(p*n/100) (added import math; rank clamped to ≥1) instead of floor division. Added regression test in tests/test_toolkit.py; full suite passes (86 passed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approving. The fix addresses the root cause. The old code used `p*n//100`, which floors the rank. The patch switches to `ceil(p*n/100)`, which is the nearest-rank definition the docstring states. I checked these outputs on [15,20,35,40,50]:
- p=0 gives 15.
- p=0.5 gives 15.
- p=30 gives 20.
- p=40 gives 20.
- p=50 gives 35.
- p=99 and p=100 give 50.
The full suite passes (86 passed). No existing tests were modified or weakened.

Please clean up before merging:
- Remove the `__pycache__/*.pyc` files from the diff and add a `.gitignore` entry if one is missing.
- Delete `tests/test_issue_repro.py`. It duplicates `test_percentile_rank_rounds_up` in `tests/test_toolkit.py`.
- `max(int(rank), 1)` is redundant, because p>0 already gives rank ≥ 1. `int()` is also redundant, because `math.ceil` returns an int. Neither is harmful.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
