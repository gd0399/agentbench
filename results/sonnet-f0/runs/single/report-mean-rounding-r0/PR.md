# Fix #157: summarize() rounds the mean to an integer

branch: `fix/issue-157`

Fixes #157

## Root cause
summarize() wrapped the mean in round(), truncating it to an integer.

## Change
Removed the round() call around stats.mean in report.summarize; added a regression test. Full suite passes.

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
