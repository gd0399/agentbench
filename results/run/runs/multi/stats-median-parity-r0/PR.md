# Fix #103: median of odd-length list is wrong

branch: `fix/issue-103`

Fixes #103

## Root cause
SBFL suspicious lines: toolkit/stats.py:13 (1.00), toolkit/stats.py:14 (1.00), toolkit/stats.py:15 (1.00), toolkit/stats.py:16 (1.00), toolkit/stats.py:18 (1.00)

## Change
toolkit/stats.py:14: `n = len(ordered) - 1` (mutation search, 1 candidates tried)

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
