# Fix #155: day_of_year counts the current month twice

branch: `fix/issue-155`

Fixes #155

## Root cause
The loop used range(1, month + 1), so it included the current month's full length and then added the day on top.

## Change
Fixed the loop in day_of_year to sum only the months before the given month. Added a repro test; the full suite passes.

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
