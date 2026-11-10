# Fix #125: initials() are not capitalised

branch: `fix/issue-125`

Fixes #125

## Root cause
text.initials joined the first character of each word without uppercasing it.

## Change
initials() now uppercases each initial. I added a repro test, and the full suite passes (84 tests).

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
