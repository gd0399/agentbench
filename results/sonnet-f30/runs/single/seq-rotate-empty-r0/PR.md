# Fix #132: rotate([]) raises ZeroDivisionError

branch: `fix/issue-132`

Fixes #132

## Root cause
rotate computed `k % len(items)`, which divides by zero when items is empty.

## Change
rotate now returns an empty sequence for empty input. I added tests/test_issue_repro.py, and the full suite passes (85 tests). I didn't run the new test before making the fix.

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
