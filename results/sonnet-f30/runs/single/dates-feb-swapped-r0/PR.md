# Fix #152: February lengths are swapped

branch: `fix/issue-152`

Fixes #152

## Root cause
The conditional returned 28 for leap years and 29 otherwise.

## Change
Swapped the February values in days_in_month.

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
