# Fix #154: quarter_of(12) raises ValueError

branch: `fix/issue-154`

Fixes #154

## Root cause
Off-by-one in validation: `month > 11` rejected December.

## Change
Fixed the upper bound check in quarter_of so month 12 is accepted and returns 4.

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
