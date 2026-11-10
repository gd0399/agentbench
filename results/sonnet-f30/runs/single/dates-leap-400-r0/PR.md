# Fix #150: is_leap_year(2000) is False

branch: `fix/issue-150`

Fixes #150

## Root cause
The century exception used `year % 400 != 0` instead of `== 0`, so years divisible by 400 (e.g. 2000) were wrongly reported as non-leap.

## Change
Fixed the leap year condition in is_leap_year. Added a repro test and the full suite passes.

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
