# Fix #136: binary_search hangs forever on a missing value

branch: `fix/issue-136`

Fixes #136

## Root cause
In the items[mid] < target branch, lo was set to mid instead of mid + 1, so the search range stopped shrinking and the loop never ended when the target was missing.

## Change
Fixed the infinite loop in binary_search by setting lo = mid + 1 when items[mid] < target. Added a repro test; the full suite passes.

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
