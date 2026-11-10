# Fix #153: March is reported as Q2

branch: `fix/issue-153`

Fixes #153

## Root cause
Off-by-one: month // 3 + 1 put months 3, 6, 9, 12 in the next quarter.

## Change
Fixed quarter_of formula to (month-1)//3+1; added regression test.

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
