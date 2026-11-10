# Fix #130: dedupe() does not remove duplicates

branch: `fix/issue-130`

Fixes #130

## Root cause
dedupe() checked `x not in seen` but never added items to `seen`, so nothing was filtered.

## Change
Added the missing `seen.add(x)` in dedupe(). I added a repro test, and the full suite passes (84 tests).

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
