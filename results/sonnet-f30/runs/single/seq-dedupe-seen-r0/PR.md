# Fix #130: dedupe() does not remove duplicates

branch: `fix/issue-130`

Fixes #130

## Root cause
dedupe never recorded items in the `seen` set, so nothing was filtered.

## Change
Added the missing seen.add(x) in dedupe; repro test and full suite pass.

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
