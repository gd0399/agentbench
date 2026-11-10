# Fix #131: rotate() rotates left, docs say right

branch: `fix/issue-131`

Fixes #131

## Root cause
The slice used items[k:] + items[:k], which rotates left. It now uses k = len - k, which rotates right.

## Change
rotate now rotates right as documented; added a regression test, and the full suite passes.

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
