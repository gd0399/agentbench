# Fix #103: median of odd-length list is wrong

branch: `fix/issue-103`

Fixes #103

## Root cause
toolkit/stats.py median(), lines 16-18: the parity branches are swapped. `if n % 2 == 0: return ordered[mid]` handles even length by returning the upper-middle element, and the fall-through `return (ordered[mid-1] + ordered[mid]) / 2` handles odd length by averaging two elements. For [3,1,2] this gives (1+2)/2 = 1.5 instead of ordered[1] = 2. Even-length input is also wrong: [4,1,3,2] gives 3 instead of 2.5. The sort is present and correct. The fix is to return ordered[mid] when n is odd, and average ordered[mid-1] and ordered[mid] when n is even. There is no conflict with existing tests, since the only median test covers the empty-input error.

## Change
Fixed swapped parity branches in stats.median(): odd n returns ordered[mid], even n averages the two middle elements. Full suite (82 tests, including repro tests) passes.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The parity check in `median()` was inverted. Changing `n % 2 == 0` to `n % 2 == 1` fixes the root cause, so odd lengths return the middle element and even lengths average the two middle elements. No special-casing of the issue's input. I read the code and ran the suite: 82 tests pass. The `report.py` caller of `median` needs no change. The new tests in `tests/test_issue_repro.py` cover odd and even lengths, and no existing tests were modified or removed.

Nit: the diff includes many `__pycache__/*.pyc` files. Drop them from the commit and consider adding a `.gitignore` for them. They don't affect behaviour.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
