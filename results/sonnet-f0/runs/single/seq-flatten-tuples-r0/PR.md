# Fix #128: flatten ignores tuples

branch: `fix/issue-128`

Fixes #128

## Root cause
flatten only checked isinstance(item, list), so tuples were treated as scalar items.

## Change
flatten now recurses into tuples as well as lists; added repro tests, full suite passes.

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
