# Fix #102: summarize() reports the wrong median for even-length data

branch: `fix/issue-102`

Fixes #102

## Root cause
toolkit/stats.py line 18, in median(): for even n it returns (ordered[mid] + ordered[mid + 1]) / 2. It should average the two middle elements, ordered[mid - 1] and ordered[mid]. For [1,2,3,4], mid=2, so it averages 3 and 4 and gives 3.5 instead of 2.5. For n=2 it would raise IndexError. report.summarize (report.py line 9) just calls stats.median and is correct. The odd-length path is correct. Existing tests only cover odd-length and empty input, so no documented behaviour conflicts with the fix.

## Change
Fixed median() in toolkit/stats.py. For even-length input it now averages ordered[mid - 1] and ordered[mid] instead of ordered[mid] and ordered[mid + 1]. This also removes the IndexError for n=2. The full suite passes (84 tests), including both repro tests. The repro file already covers n=2 with median([4, 1]) == 2.5, so I didn't add another test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is in stats.median(). For even n it averaged ordered[mid] and ordered[mid+1], which is off by one. It also raised IndexError for n=2. The patch changes it to ordered[mid-1] and ordered[mid], which is the correct fix. It is a one-line change, and summarize() picks it up with no change of its own. I ran the full suite and all 84 tests pass. The odd-length and empty-input behaviour is unchanged. No existing tests were modified. The new tests/test_issue_repro.py covers the issue's exact case and n=2.

Before merging, drop the __pycache__/*.pyc files from the diff. They are build artifacts from running the tests, and the repo has no .gitignore. Consider adding one with `__pycache__/`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
