# Fix #135: binary_search returns -1 for the largest element

branch: `fix/issue-135`

Fixes #135

## Root cause
hi was initialised to len(items) - 2, so the last element was never examined.

## Change
Fixed the off-by-one in the initial upper bound of binary_search (len-2 -> len-1). I added a repro test and the full suite passes.

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
