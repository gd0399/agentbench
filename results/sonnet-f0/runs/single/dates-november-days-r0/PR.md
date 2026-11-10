# Fix #151: November has 31 days

branch: `fix/issue-151`

Fixes #151

## Root cause
days_in_month listed only (4, 6, 9) as 30-day months and omitted November.

## Change
Added 11 to the 30-day months in days_in_month. Added a regression test, and the full suite passes.

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
