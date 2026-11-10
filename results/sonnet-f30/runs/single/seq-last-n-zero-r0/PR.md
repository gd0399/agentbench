# Fix #139: last_n(items, 0) returns everything

branch: `fix/issue-139`

Fixes #139

## Root cause
items[-0:] equals items[0:], which returns the whole sequence. The guard only handled negative n, so n=0 fell through to that slice.

## Change
Changed the guard in last_n from n < 0 to n <= 0. All 84 tests pass, including the new repro test.

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
