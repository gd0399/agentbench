# Fix #158: summarize() max is wrong for unsorted input

branch: `fix/issue-158`

Fixes #158

## Root cause
report.summarize used values[-1] for "max", which is only correct for sorted input.

## Change
summarize() now uses max(values) rather than the last element.

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
