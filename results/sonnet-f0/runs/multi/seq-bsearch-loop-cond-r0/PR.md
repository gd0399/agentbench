# Fix #134: binary_search can't find the last element

branch: `fix/issue-134`

Fixes #134

## Root cause
toolkit/seq.py binary_search (line 48): the loop condition `while lo < hi` with inclusive bounds (hi = len(items)-1, hi = mid-1) exits when lo == hi without checking items[lo]. Any target that is only reachable at lo==hi is missed: the last element (9 in [1,3,5,7,9]), also 3 and single-element lists. Fix: use `while lo <= hi`. It doesn't conflict with existing tests (they only cover 7 and a missing value).

## Change
Fixed binary_search loop condition (`while lo <= hi`) so the final remaining candidate is checked; added regression tests (first/middle/last, missing, single-element, empty). All 91 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the loop condition `while lo < hi`, which exits before checking the last remaining candidate. Changing it to `lo <= hi` is the standard, minimal fix. The `mid`, `lo = mid + 1` and `hi = mid - 1` updates were already correct for an inclusive range.

I ran the full suite and 91 tests pass. I also brute-forced sorted lists of length 0 to 11 against every target, both present and absent. Every result was correct. No existing tests were modified, only added.

Nits, which don't block the merge:
- The diff includes `__pycache__/*.pyc` files. Drop them from the commit and add them to `.gitignore`.
- `tests/test_issue_repro.py` duplicates the new tests in `test_toolkit.py`. Keep one copy, preferably the ones in `test_toolkit.py`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
