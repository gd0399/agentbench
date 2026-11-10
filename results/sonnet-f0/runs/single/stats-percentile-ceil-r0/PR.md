# Fix #108: percentile() rounds the rank down instead of up

branch: `fix/issue-108`

Fixes #108

## Root cause
The rank was computed with floor division (p*n//100). Nearest-rank percentile needs ceiling, so p=30 on 5 values gave rank 1 instead of 2.

## Change
percentile() now uses ceil(p*n/100) for the nearest rank. I added tests/test_issue_repro.py. The full suite passes, 84 tests.

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
