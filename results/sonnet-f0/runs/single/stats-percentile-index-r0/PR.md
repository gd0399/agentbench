# Fix #110: percentile() is off by one

branch: `fix/issue-110`

Fixes #110

## Root cause
percentile() computed the nearest rank ceil(p*n/100), which is 1-based, but used it directly as a 0-based list index. This returned the next element, and p=100 would raise IndexError.

## Change
Convert the 1-based nearest-rank to a 0-based index in percentile(). Added a repro test; the full suite passes.

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
