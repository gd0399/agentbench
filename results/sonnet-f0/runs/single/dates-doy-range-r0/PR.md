# Fix #155: day_of_year counts the current month twice

branch: `fix/issue-155`

Fixes #155

## Root cause
range(1, month + 1) included the current month's full length, in addition to adding day.

## Change
Loop in day_of_year now sums only the months before the current one.

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
