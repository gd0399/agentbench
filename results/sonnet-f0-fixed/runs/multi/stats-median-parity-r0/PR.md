# Fix #103: median of odd-length list is wrong

branch: `fix/issue-103`

Fixes #103

## Root cause
toolkit/stats.py median() lines 16-18 have the even/odd branches swapped. When n % 2 == 0 it returns ordered[mid] (should return the average of ordered[mid-1] and ordered[mid]). When n is odd it returns (ordered[mid-1] + ordered[mid]) / 2 (should return ordered[mid]). So median([3,1,2]) gives (1+2)/2 = 1.5, and the even-length case is also wrong: median([4,1, 3,2]) gives 3 instead of 2.5. The fix is to swap the branch bodies, or invert the condition to n % 2 == 1. No existing tests cover this and nothing in the docs contradicts it. toolkit/report.py also calls stats.median, so it is affected too.

## Change
Fixed swapped odd/even branches in stats.median() (condition now n % 2 == 1 returns the middle element; even returns the average of the two middle ones). The repro tests and the full suite pass (82 passed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the swapped parity check in median(), and the one-line change to `n % 2 == 1` fixes it. I checked these inputs: [5] gives 5, [1,2] gives 1.5, [3,1,2] gives 2, [4,1,3,2] gives 2.5, and floats work too. The only other caller, report.summarize, doesn't compensate for the bug. The full suite passes (82). The new tests/test_issue_repro.py covers both odd and even lengths, and no existing tests were modified.

Nit: the diff includes committed __pycache__/*.pyc files. Please drop them and add `__pycache__/` to .gitignore before merging. They don't affect behaviour.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
