# Fix #112: moving_average(window=0) raises ZeroDivisionError instead of ValueError

branch: `fix/issue-112`

Fixes #112

## Root cause
toolkit/stats.py line 62, in moving_average: the guard is `if window < 0`, so window == 0 passes validation. It then reaches `/ window` on line 66 and raises ZeroDivisionError. The guard should be `window < 1` (or `window <= 0`). The error message already says "window must be positive". No existing test or doc contradicts this.

## Change
Changed moving_average guard from `window < 0` to `window < 1` so window=0 raises ValueError instead of ZeroDivisionError. Added regression tests for zero and negative windows. Full suite: 86 passed, including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approving. The fix addresses the root cause. The old guard `window < 0` let 0 through, and 0 then caused the division by `window`. Changing it to `window < 1` closes that gap for every non-positive window, not just the repro input.

What I checked:
- `moving_average([1,2], 0)` and `moving_average([1,2], -1)` both raise `ValueError("window must be positive")`.
- Valid inputs are unchanged: a window larger than the list returns `[]`, an empty list returns `[]`, and the existing tests pass.
- The full suite passes, 86 tests. No existing tests were modified or removed. The new tests only add coverage.

Minor nits, not blocking:
- The diff includes `__pycache__/*.pyc` files. Please make sure they are not committed, and add them to `.gitignore` if they aren't already ignored.
- `tests/test_issue_repro.py` duplicates `test_moving_average_zero_window` in `tests/test_toolkit.py`. You could drop the separate repro file.
- A float window such as 1.5 raises `TypeError` from `range`. That is outside this issue's scope.

<details><summary>Agent trail</summary>

Triage: bug / low / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
