# Fix #102: summarize() reports the wrong median for even-length data

branch: `fix/issue-102`

Fixes #102

## Root cause
The even-length branch of stats.median averaged ordered[mid] and ordered[mid+1], which is off by one. For [1,2,3,4] that gave 3.5, and for [1,2] it would raise IndexError.

## Change
Fixed the even-length median in stats.median. It now averages the two middle elements, ordered[mid-1] and ordered[mid]. Added tests/test_issue_repro.py, and the full suite passes.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: ? / ? / component `?`
Handoffs: single agent
Recovered errors: 0
</details>

_Opened automatically by agentbench._
