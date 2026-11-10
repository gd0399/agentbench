# Fix #114: clamp() rejects lo == hi

branch: `fix/issue-114`

Fixes #114

## Root cause
toolkit/stats.py line 71, in clamp(): the guard `if lo >= hi: raise ValueError("lo must be <= hi")` rejects equal bounds. It should be `if lo > hi`. The error message already says "lo must be <= hi", so the comparison contradicts its own intent. The existing test test_clamp_bad only checks clamp(1, 5, 0), where lo > hi, so it still passes after the fix.

## Change
Changed clamp() guard in toolkit/stats.py from `lo >= hi` to `lo > hi` so equal bounds are accepted. Regression test tests/test_issue_repro.py covers it; full suite passes (84).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the over-strict guard `lo >= hi`. Changing it to `lo > hi` fixes it. The error message already said "lo must be <= hi", so the fix matches the intended contract. `clamp(3,3,3)` now returns 3 and `clamp(10,3,3)` returns 3. `lo > hi` still raises, and the existing `test_clamp_bad` (1, 5, 0) still passes. The full suite passes (84), and no existing tests were modified. The new regression test covers equal bounds with the value both at and above the bound. The source change is one line, which is minimal.

Nit: the diff includes `__pycache__/*.pyc` files. These are build artifacts from running the tests. Make sure they are not committed, and consider adding `__pycache__/` to `.gitignore`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
