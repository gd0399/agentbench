# Fix #102: summarize() reports the wrong median for even-length data

branch: `fix/issue-102`

Fixes #102

## Root cause
toolkit/stats.py line 18, in median(): for even-length input it returns (ordered[mid] + ordered[mid + 1]) / 2. It should average the two middle elements, ordered[mid - 1] and ordered[mid]. For [1,2,3,4], mid=2, so it averages 3 and 4 and gives 3.5 instead of 2.5. For length-2 input it would raise IndexError. report.summarize (toolkit/report.py line 9) just calls stats.median, so it is not at fault. Existing tests cover only odd-length and empty input, so they don't contradict the fix.

## Change
Fix stats.median for even-length input: average ordered[mid-1] and ordered[mid] instead of ordered[mid] and ordered[mid+1]. All 84 tests pass including repro.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The bug was in stats.median, which averaged ordered[mid] and ordered[mid+1] for even-length input. The one-line change to ordered[mid-1] and ordered[mid] fixes that root cause. summarize() just calls stats.median, so it is fixed too.

I ran the full suite (84 passed). I also checked a few edge cases by hand: [1,2,3,4] gives 2.5, [5,1] gives 3.0, [1,1,1,1] gives 1.0, [1,2] gives 1.5, and an unsorted list with negatives gives 7.5. The odd-length and empty-input paths are unchanged. No existing tests were modified. The new tests in tests/test_issue_repro.py cover the issue's repro and the unsorted two-element case.

Two small things to clean up before merging:
- The diff includes committed __pycache__/*.pyc files. Remove them from the commit and add a .gitignore entry for `__pycache__/`.
- Optionally, fold the new tests into tests/test_toolkit.py next to test_median_odd instead of keeping a separate "issue_repro" file.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
