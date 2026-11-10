# Fix #104: median() crashes with TypeError

branch: `fix/issue-104`

Fixes #104

## Root cause
Float division produced a float list index, causing TypeError for odd-length input.

## Change
Changed `mid = n / 2` to `n // 2` in stats.median. Added repro tests; full suite passes.

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
