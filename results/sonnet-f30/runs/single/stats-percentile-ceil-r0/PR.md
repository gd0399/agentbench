# Fix #108: percentile() rounds the rank down instead of up

branch: `fix/issue-108`

Fixes #108

## Root cause
The rank was computed with floor division (p * n // 100). Nearest-rank percentile requires rounding up.

## Change
percentile() now computes the nearest rank as ceil(p*n/100) instead of using floor division. percentile([15,20,35,40,50], 30) now returns 20. I added a repro test, and the full suite passes (84 tests).

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
