# Fix #106: sample variance uses the population formula

branch: `fix/issue-106`

Fixes #106

## Root cause
In stats.variance, the sample=True branch divided by n instead of n-1, so it returned the population variance.

## Change
Sample variance now divides by n-1. Added a repro test, and the full suite passes.

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
