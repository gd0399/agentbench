# Fix #113: clamp() returns the lower bound for in-range values

branch: `fix/issue-113`

Fixes #113

## Root cause
toolkit/stats.py line 73, clamp(): `return min(lo, max(x, hi))` has lo and hi swapped. max(x, hi) is always >= hi, and min(lo, ...) then always returns lo (since lo <= hi). So the function always returns lo, which is why clamp(5,0,10) gives 0 and clamp(15,0,10) also gives 0. The correct expression is `max(lo, min(x, hi))`. The existing tests (clamp_low, equal bounds, bad bounds) pass by coincidence and don't conflict with the fix.

## Change
Fix clamp() in toolkit/stats.py: swapped min/max; now `max(lo, min(x, hi))`. Full suite passes (84), including repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the min and max calls being nested the wrong way round. `max(lo, min(x, hi))` is the correct clamp. I ran the full suite and 84 tests pass. I also checked clamp directly: in-range, below, above, both boundary values and lo==hi all return the right result. The `lo > hi` ValueError is unchanged. No existing tests were modified, and the new repro tests are reasonable. Before merging, please drop the committed `__pycache__/*.pyc` files from the diff and add `__pycache__/` to `.gitignore` if it isn't there already. They aren't part of the fix.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
