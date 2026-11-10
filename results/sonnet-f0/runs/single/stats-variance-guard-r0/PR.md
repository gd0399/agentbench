# Fix #107: variance() raises for perfectly valid input

branch: `fix/issue-107`

Fixes #107

## Root cause
The guard `if n < 2 or sample` raised ValueError whenever sample=True, which is the default, whatever the length. It also made the empty-input check unreachable. The condition should have been `sample and n < 2`, with the empty check first.

## Change
Fixed the guard in variance() so sample variance works for 2 or more values. variance([1,2,3]) now returns 1.0. The full suite passes (84 tests), including a new repro test.

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
