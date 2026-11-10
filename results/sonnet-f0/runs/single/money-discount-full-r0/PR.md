# Fix #141: 100% discount raises ValueError

branch: `fix/issue-141`

Fixes #141

## Root cause
The validation used `percent >= 100`, which wrongly rejected exactly 100.

## Change
Changed the bounds check in apply_discount to reject only percent > 100, so a 100% discount returns 0.0. Added a repro test; all 84 tests pass.

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
