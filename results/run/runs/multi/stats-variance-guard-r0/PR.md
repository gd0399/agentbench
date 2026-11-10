# Fix #107: variance() raises for perfectly valid input

branch: `fix/issue-107`

Fixes #107

## Root cause
SBFL suspicious lines: toolkit/stats.py:38 (0.71), toolkit/stats.py:36 (0.58), toolkit/stats.py:37 (0.58)

## Change
toolkit/stats.py:37: `if n < 2 and sample:` (mutation search, 7 candidates tried)

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
