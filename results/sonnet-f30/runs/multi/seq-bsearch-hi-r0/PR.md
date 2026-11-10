# Fix #135: binary_search returns -1 for the largest element

branch: `fix/issue-135`

Fixes #135

## Root cause
toolkit/seq.py line 47 in binary_search: the upper bound is initialised as `hi = len(items) - 2` instead of `len(items) - 1`. The last element is therefore never examined, so searching for the largest element returns -1. A single-element list also fails, because hi = -1. The fix is to set `hi = len(items) - 1`. The existing tests and docstring ("Index of target in sorted items, or -1") do not contradict the expected behaviour.

## Change
Fixed binary_search in toolkit/seq.py: upper bound was `len(items) - 2`, now `len(items) - 1`, so the last element is searched (loop `while lo <= hi` and `hi = mid - 1` already match the inclusive bound). I added edge-case tests to tests/test_issue_repro.py: empty list, single-element miss, absent targets. Full suite: 88 passed.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The root cause is correct. The upper bound `len(items) - 2` skipped the last index, and the loop (`lo <= hi`, `hi = mid - 1`) is written for an inclusive bound. Changing it to `len(items) - 1` fixes this for every input, not only the issue's example. The change is one line and minimal. All 88 tests pass, and no existing tests were modified. The new tests cover each element, an empty list, single-element misses and absent targets, so the boundary behaviour is checked well. One thing to fix before merging: the diff includes `__pycache__/*.pyc` files. Drop them from the commit and add `__pycache__/` to `.gitignore` if it isn't there already.

<details><summary>Agent trail</summary>

Triage: bug / high / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
