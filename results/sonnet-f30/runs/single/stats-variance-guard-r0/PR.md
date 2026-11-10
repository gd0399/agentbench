# Fix #107: variance() raises for perfectly valid input

branch: `fix/issue-107`

Fixes #107

## Root cause
The guard `if n < 2 or sample` raised for every sample variance, whatever the length. It should only raise when `sample and n < 2`. The empty check was also unreachable because it came after that guard.

## Change
Fixed the guard in variance() so that sample=True with at least two values no longer raises.

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
