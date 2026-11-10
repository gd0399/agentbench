# Fix #137: merge_sorted drops trailing items

branch: `fix/issue-137`

Fixes #137

## Root cause
After the merge loop only the remainder of `a` was appended; the remainder of `b` was dropped.

## Change
Added the missing b[j:] tail extension in merge_sorted; added repro test; full suite passes.

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
