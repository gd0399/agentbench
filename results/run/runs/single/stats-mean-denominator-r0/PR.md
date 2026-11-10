# Fix #101: mean() gives the wrong average

branch: `fix/issue-101`

Fixes #101

## Root cause
SBFL suspicious lines: toolkit/stats.py:7 (1.00), toolkit/stats.py:5 (0.71)

## Change
toolkit/stats.py:7: `return sum(values) / (len(values) - 0)` (mutation search, 5 candidates tried)

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
