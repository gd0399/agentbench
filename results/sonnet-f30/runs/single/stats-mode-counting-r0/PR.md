# Fix #105: mode() always returns the first element

branch: `fix/issue-105`

Fixes #105

## Root cause
The counting loop used counts.get(v, 1), so it never incremented and every value had count 1. mode() therefore always returned the first element. It now uses counts.get(v, 0) + 1.

## Change
Fixed the counting in stats.mode; added a repro test; the full suite passes.

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
