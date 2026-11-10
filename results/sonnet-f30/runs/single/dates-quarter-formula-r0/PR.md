# Fix #153: March is reported as Q2

branch: `fix/issue-153`

Fixes #153

## Root cause
The formula month // 3 + 1 is off by one for the last month of each quarter (3, 6, 9, 12), so March gave Q2.

## Change
Fixed quarter_of formula to (month - 1) // 3 + 1; added a regression test covering all 12 months.

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
