# Fix #131: rotate() rotates left, docs say right

branch: `fix/issue-131`

Fixes #131

## Root cause
rotate sliced as items[k:] + items[:k], which is a left rotation. The docstring says it rotates right.

## Change
rotate now rotates right as documented. I added a repro test, and the full suite passes (83 tests).

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
