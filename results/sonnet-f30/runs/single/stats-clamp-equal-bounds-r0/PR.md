# Fix #114: clamp() rejects lo == hi

branch: `fix/issue-114`

Fixes #114

## Root cause
The validation in stats.clamp used `>=`, which wrongly rejected lo == hi. Its own error message says "lo must be <= hi".

## Change
Changed the bounds check in clamp() from `lo >= hi` to `lo > hi`. clamp(3, 3, 3) now returns 3. Added a regression test, and the full suite passes.

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
