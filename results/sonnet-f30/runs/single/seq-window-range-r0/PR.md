# Fix #133: sliding_window misses the final window

branch: `fix/issue-133`

Fixes #133

## Root cause
range(len(items) - size) omitted the last window start index; it should be range(len(items) - size + 1).

## Change
Fixed the off-by-one in sliding_window's range bound and added regression tests. The full suite passes (85 tests).

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
