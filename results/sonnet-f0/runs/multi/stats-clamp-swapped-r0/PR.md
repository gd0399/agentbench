# Fix #113: clamp() returns the lower bound for in-range values

branch: `fix/issue-113`

Fixes #113

## Root cause
toolkit/stats.py line 73, clamp() has min/max swapped: `return min(lo, max(x, hi))`. It always returns lo when lo <= hi, so clamp(5,0,10)=0 and clamp(15,0,10)=0. The correct expression is `min(hi, max(x, lo))`. The existing tests (low clamp, equal bounds, bad bounds) don't cover in-range or high values, so they pass despite the bug. The issue doesn't conflict with any documented behaviour.

## Change
Fixed clamp() in toolkit/stats.py: swapped min/max (`min(lo, max(x, hi))`) changed to `min(hi, max(x, lo))`. Added regression tests (in-range, high, low) in tests/test_toolkit.py; the repro tests in tests/test_issue_repro.py are kept. Full suite: 87 passed.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The swapped min/max in `clamp` is the root cause, and `min(hi, max(x, lo))` is the standard form. I ran it on in-range, high, low, equal-bound and float inputs, and all gave the right results. The `lo > hi` ValueError still works. The full suite passes (87 passed), and no existing tests were changed or weakened.

Nits to clean up before or when merging; none of them block approval:
- The diff includes `__pycache__/*.pyc` files. These are build artifacts and shouldn't be committed. Drop them and add `__pycache__/` to `.gitignore`.
- The new tests are duplicated. `tests/test_issue_repro.py` repeats `test_clamp_in_range` and `test_clamp_high` from `tests/test_toolkit.py`. `test_clamp_low_negative` is nearly identical to the existing `test_clamp_low`. Keep one copy of each.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
