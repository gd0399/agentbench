# Fix #132: rotate([]) raises ZeroDivisionError

branch: `fix/issue-132`

Fixes #132

## Root cause
rotate computed k % len(items) without handling empty input, so len(items) == 0 caused ZeroDivisionError.

## Change
rotate now returns an empty copy for empty input. I added tests/test_issue_repro.py; the full suite passes (84 tests).

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
