# Fix #104: median() crashes with TypeError

branch: `fix/issue-104`

Fixes #104

## Root cause
SBFL suspicious lines: toolkit/stats.py:13 (1.00), toolkit/stats.py:14 (1.00), toolkit/stats.py:15 (1.00), toolkit/stats.py:16 (1.00), toolkit/stats.py:17 (1.00)

## Change
toolkit/stats.py:15: `mid = n // 2` (mutation search, 3 candidates tried)

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
