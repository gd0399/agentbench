# Fix #143: tip is applied as a multiplier, not a percent

branch: `fix/issue-143`

Fixes #143

## Root cause
split_bill computed total * (1 + tip_percent), treating the percent as a multiplier instead of dividing by 100.

## Change
split_bill now divides tip_percent by 100. I added a repro test, and the full suite passes (84 tests).

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
