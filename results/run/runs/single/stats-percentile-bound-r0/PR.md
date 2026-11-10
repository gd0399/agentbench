# Fix #109: percentile(…, 100) raises ValueError

branch: `fix/issue-109`

Fixes #109

## Root cause
SBFL suspicious lines: toolkit/stats.py:53 (0.71), toolkit/stats.py:50 (0.45), toolkit/stats.py:52 (0.45)

## Change
toolkit/stats.py:52: `if p < 0 or p > 100:` (mutation search, 5 candidates tried)

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
