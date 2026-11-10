# Fix #102: summarize() reports the wrong median for even-length data

branch: `fix/issue-102`

Fixes #102

## Root cause
SBFL suspicious lines: toolkit/stats.py:18 (1.00), toolkit/report.py:6 (0.71), toolkit/report.py:7 (0.71), toolkit/report.py:8 (0.71), toolkit/report.py:9 (0.71)

## Change
toolkit/stats.py:18: `return (ordered[mid] + ordered[mid - 1]) / 2` (mutation search, 2 candidates tried)

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
