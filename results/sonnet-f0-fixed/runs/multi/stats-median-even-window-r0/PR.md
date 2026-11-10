# Fix #102: summarize() reports the wrong median for even-length data

branch: `fix/issue-102`

Fixes #102

## Root cause
Off-by-one in toolkit/stats.py median(), line 18. For even n it returns (ordered[mid] + ordered[mid + 1]) / 2, which averages the upper-middle element and the one after it. For [1,2,3,4] that is (3+4)/2 = 3.5. The two middle elements are ordered[mid-1] and ordered[mid], so the line should be (ordered[mid - 1] + ordered[mid]) / 2. It can also raise IndexError for n=2. report.summarize in toolkit/report.py just calls stats.median and is correct. The existing tests only cover odd-length and empty input, so they don't conflict with the fix.

## Change
Fixed the off-by-one in stats.median() for even-length input. It now averages ordered[mid-1] and ordered[mid], which also removes the IndexError for n=2. Added a test for median([1, 2]) == 1.5. All 85 tests pass, including the repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approving. The root cause is in stats.median(): the even-length branch averaged ordered[mid] and ordered[mid+1], which is off by one. The fix averages ordered[mid-1] and ordered[mid], which is correct for every even n. It also removes the IndexError the old code raised for n=2.

I ran the full suite and 85 tests pass. I also checked these cases by hand:
- median([4,1,3,2]) returns 2.5.
- median([1,2]) returns 1.5.
- median([5,5]) returns 5.0.
- A float list of even length returns the right value.
- summarize([1,2,3,4]) returns the expected dict from the issue.

No existing tests were edited or weakened. The only change to test_toolkit.py is a new n=2 test, and tests/test_issue_repro.py is a new file with regression tests.

Before merging, please drop the committed __pycache__/*.pyc files from the patch and add a .gitignore for them. They are build artifacts and do not belong in the change. The code change itself is minimal and correct.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
