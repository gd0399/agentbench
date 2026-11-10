# Fix #143: tip is applied as a multiplier, not a percent

branch: `fix/issue-143`

Fixes #143

## Root cause
split_bill computed total * (1 + tip_percent) and used the percent as a raw multiplier instead of dividing by 100.

## Change
split_bill now divides tip_percent by 100. split_bill(100, 4, tip_percent=20) returns 30.0. I added a repro test, and the full suite passes (84 tests).

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
