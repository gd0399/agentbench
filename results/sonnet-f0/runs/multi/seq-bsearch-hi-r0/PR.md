# Fix #135: binary_search returns -1 for the largest element

branch: `fix/issue-135`

Fixes #135

## Root cause
toolkit/seq.py line 47, in binary_search: `lo, hi = 0, len(items) - 2` initialises the upper bound one too low, so the last index (len-1) is never examined. The loop condition `lo <= hi` is correct. The fix is `hi = len(items) - 1`. Single-element lists also fail, because hi = -1. Existing tests only cover a middle element and a missing value, so they don't conflict with the fix.

## Change
Fixed binary_search upper bound (len(items) - 2 -> len(items) - 1) so the last element and single-element lists are found; added regression tests (last, first, single, empty, missing). Full suite passes (92).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line fix in toolkit/seq.py is correct. The upper bound `len(items) - 2` skipped the last index, and `len(items) - 1` is the right value. I checked this exhaustively for sorted lists of length 0 to 29, with every target in and out of range, and every result matched. The full suite passes (92 tests), and no existing tests were changed or weakened.

Please clean up two things before merging. Neither affects correctness:
1. The diff includes committed `__pycache__/*.pyc` files. Remove them and add `__pycache__/` to `.gitignore`.
2. `tests/test_issue_repro.py` duplicates the regression tests added to `tests/test_toolkit.py`. Delete the repro file and keep the tests in `test_toolkit.py`.

<details><summary>Agent trail</summary>

Triage: bug / high / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
