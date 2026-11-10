# Fix #136: binary_search hangs forever on a missing value

branch: `fix/issue-136`

Fixes #136

## Root cause
When items[mid] < target, lo was set to mid instead of mid + 1, so lo/hi stopped converging (e.g. lo=1, hi=2, mid=1) and the loop never ended.

## Change
Changed `lo = mid` to `lo = mid + 1` in binary_search; added repro test; full suite passes.

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
