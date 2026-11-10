# Fix #114: clamp() rejects lo == hi

branch: `fix/issue-114`

Fixes #114

## Root cause
Off-by-one in validation: `lo >= hi` rejected equal bounds, contradicting the error message "lo must be <= hi".

## Change
Changed the bounds check in clamp from `lo >= hi` to `lo > hi`. Added a repro test. Full suite passes.

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
