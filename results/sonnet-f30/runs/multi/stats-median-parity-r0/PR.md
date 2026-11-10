# Fix #103: median of odd-length list is wrong

branch: `fix/issue-103`

Fixes #103

## Root cause
toolkit/stats.py median() lines 16-18: the even/odd branches are swapped. `if n % 2 == 0: return ordered[mid]` returns the upper-middle element for even lengths, and the odd-length fallthrough `return (ordered[mid-1] + ordered[mid]) / 2` averages two neighbours (for [3,1,2] sorted [1,2,3], mid=1 -> (1+2)/2 = 1.5). Fix: odd n -> return ordered[mid]; even n -> return (ordered[mid-1] + ordered[mid]) / 2. Even-length lists are also wrong (e.g. [4,1,3,2] gives 3 instead of 2.5). Sorting is fine. Repro tests in tests/test_issue_repro.py (odd and even). No existing test covers non-empty median, and nothing contradicts the requested behaviour.

## Change
Fixed swapped parity branches in stats.median: odd length returns the middle element, even length averages the two middle elements. All 82 tests pass, including the repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix addresses the root cause. The parity branches in `median` were inverted, and the one-line change from `n % 2 == 0` to `n % 2 == 1` corrects them. I ran the following checks:
- The full suite passes (82 tests).
- `median([3,1,2])` returns 2.
- `median([4,1,3,2])` returns 2.5.
- `median([5])` returns 5.
- `median([1,2])` returns 1.5.
- `median([])` still raises `ValueError`.

The new tests in `tests/test_issue_repro.py` cover both parities, and no existing tests were changed. `report.py` is the only other caller and needs no change.

One cleanup before merging: the diff includes compiled `__pycache__/*.pyc` files. Drop them from the commit and add `__pycache__/` to `.gitignore`. They are build artifacts and not part of the fix. The source change itself is fine.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
