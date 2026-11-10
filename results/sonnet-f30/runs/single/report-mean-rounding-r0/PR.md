# Fix #157: summarize() rounds the mean to an integer

branch: `fix/issue-157`

Fixes #157

## Root cause
report.summarize wrapped stats.mean(values) in round(), truncating the mean to an integer.

## Change
Removed the round() call around the mean in report.summarize; added a regression test. All 83 tests pass.

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
