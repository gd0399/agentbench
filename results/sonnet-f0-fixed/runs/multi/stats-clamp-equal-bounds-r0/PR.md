# Fix #114: clamp() rejects lo == hi

branch: `fix/issue-114`

Fixes #114

## Root cause
toolkit/stats.py line 71, in clamp(): the validation is `if lo >= hi: raise ValueError("lo must be <= hi")`. It rejects equal bounds. The error message and intent say lo == hi is allowed, so the condition should be `lo > hi`. The existing test test_clamp_bad uses clamp(1, 5, 0), where lo > hi, so it still raises after the fix. No conflict with the tests.

## Change
In stats.clamp(), changed the validation from `lo >= hi` to `lo > hi`, so equal bounds are allowed (clamp(3,3,3) == 3). lo > hi still raises ValueError. The full suite passes (84 tests), including the repro test and test_clamp_bad.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approving. The fix changes the guard from `lo >= hi` to `lo > hi`. That matches the error message ("lo must be <= hi") and fixes the root cause. I ran clamp(3,3,3), clamp(1,3,3) and clamp(9,3,3), and all return 3. clamp(1,5,0) still raises ValueError. The full suite passes (84 tests). The existing tests were not changed, and the new regression test is appropriate. clamp has no other callers in the repo.

Nit: the diff includes committed `__pycache__/*.pyc` files. Please drop them from the patch and add `__pycache__/` to .gitignore. This doesn't block the merge.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
