# Fix #112: moving_average(window=0) raises ZeroDivisionError instead of ValueError

branch: `fix/issue-112`

Fixes #112

## Root cause
The guard in moving_average only checked `window < 0`, so window=0 passed it and hit a division by zero.

## Change
moving_average now rejects window <= 0 with ValueError. I added a regression test, and the full suite passes (85 tests).

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
