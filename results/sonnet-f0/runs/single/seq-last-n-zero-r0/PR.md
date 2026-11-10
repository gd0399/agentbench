# Fix #139: last_n(items, 0) returns everything

branch: `fix/issue-139`

Fixes #139

## Root cause
items[-0:] equals items[0:], which returns the whole list; n == 0 was not handled.

## Change
last_n now returns [] for n <= 0.

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
