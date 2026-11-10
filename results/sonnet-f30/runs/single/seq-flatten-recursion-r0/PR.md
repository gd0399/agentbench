# Fix #129: flatten only flattens one level

branch: `fix/issue-129`

Fixes #129

## Root cause
seq.flatten called out.extend(item) on nested lists/tuples without recursing, so it only flattened one level.

## Change
flatten now recurses into nested lists/tuples. I added tests/test_issue_repro.py, and the full suite passes (84 tests).

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
