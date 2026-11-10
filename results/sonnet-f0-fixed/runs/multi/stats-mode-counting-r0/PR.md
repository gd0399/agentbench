# Fix #105: mode() always returns the first element

branch: `fix/issue-105`

Fixes #105

## Root cause
toolkit/stats.py line 27 in mode(): `counts[v] = counts.get(v, 1)` never increments the count, so every value has count 1. The comparison `counts[v] > counts[best]` is therefore never true, and the function always returns values[0]. It should be `counts[v] = counts.get(v, 0) + 1`. The tie-break test (`mode([5,3,3,5]) == 5`) still holds after the fix because the loop uses strict `>`.

## Change
Fix mode() in toolkit/stats.py: counts[v] = counts.get(v, 0) + 1 so counts actually increment. Strict > kept, so ties still go to first-seen. Full suite passes (85 passed), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was `counts.get(v, 1)`, which never incremented the count. Every value ended up with a count of 1, so the first element always won. The one-line change to `counts.get(v, 0) + 1` fixes that, and it is minimal.

I ran the full suite and 85 tests pass. I also probed these inputs:
- `[1,2,2,3]` gives 2.
- `[5,3,3,5]` gives 5, so first-seen tie-breaking is preserved.
- `[1]` gives 1.
- `"aabbb"` gives "b".
- `[1,2,2,3,3,3]` gives 3.

The existing tests were not modified. The new regression tests in `tests/test_issue_repro.py` are reasonable.

Please drop the `__pycache__/*.pyc` files from the commit before merging. They are build artifacts, and a `.gitignore` entry for `__pycache__/` would prevent this happening again. The fix itself is fine.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
