# Fix #102: summarize() reports the wrong median for even-length data

branch: `fix/issue-102`

Fixes #102

## Root cause
stats.median averaged ordered[mid] and ordered[mid+1] for even n, an off-by-one. It should use ordered[mid-1] and ordered[mid].

## Change
Fixed the even-length median to average the two middle elements. Added regression tests; the full suite passes.

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
