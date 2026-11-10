# Fix #101: mean() gives the wrong average

branch: `fix/issue-101`

Fixes #101

## Root cause
Off-by-one in the denominator in toolkit/stats.py mean().

## Change
Fixed mean() to divide by len(values) instead of len(values)-1; added a regression test. The full suite passes.

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
