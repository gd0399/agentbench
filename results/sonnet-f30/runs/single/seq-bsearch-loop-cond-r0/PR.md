# Fix #134: binary_search can't find the last element

branch: `fix/issue-134`

Fixes #134

## Root cause
Off-by-one in loop condition skipped the final candidate range when lo == hi.

## Change
Changed loop condition in binary_search from `lo < hi` to `lo <= hi`; added repro tests; full suite passes.

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
