# Fix #134: binary_search can't find the last element

branch: `fix/issue-134`

Fixes #134

## Root cause
toolkit/seq.py line 48, binary_search: the loop condition `while lo < hi` with inclusive bounds (hi = len(items)-1, hi = mid-1) exits when lo == hi without checking that final candidate. So the last element, and any element where the window narrows to one slot (e.g. 3 in [1,3,5,7,9], or a single-element list), is missed and -1 is returned. Fix: change to `while lo <= hi`. Existing tests don't contradict this.

## Change
Fixed binary_search in toolkit/seq.py by changing the loop condition from `while lo < hi` to `while lo <= hi`. The old condition skipped the last remaining candidate. Added regression tests to tests/test_toolkit.py for the last element, every position, single-element and empty lists, and missing targets. All 89 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is the loop condition `while lo < hi`. It exits while one candidate is still unchecked, which is why the last element was missed. Changing it to `lo <= hi` is correct. It is consistent with the existing `hi = len-1` and `mid±1` updates. The patch is a one-line fix in seq.py.

I ran all 89 tests and they pass. I also compared binary_search against list.index for every target from -2 to the end of the list, on lists of length 0 to 11. All results matched. The new regression tests cover the last element, every position, single-element and empty lists, and targets outside the ends. No existing tests were modified.

Cleanup before merge, not blocking:
- The diff includes .pyc files under __pycache__. Please drop them and add a .gitignore.
- tests/test_issue_repro.py duplicates tests that are already in tests/test_toolkit.py. Please delete it.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
