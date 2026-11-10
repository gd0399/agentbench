# Fix #111: moving_average drops the last window

branch: `fix/issue-111`

Fixes #111

## Root cause
range(len(values) - window) omitted the final window; it should be range(len(values) - window + 1).

## Change
Fixed off-by-one in moving_average's loop range; added a repro test and the full suite passes.

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
