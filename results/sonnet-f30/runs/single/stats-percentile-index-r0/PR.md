# Fix #110: percentile() is off by one

branch: `fix/issue-110`

Fixes #110

## Root cause
In toolkit/stats.py percentile(), ordered[int(rank)] used the 1-based nearest rank as a 0-based index.

## Change
Fixed the nearest-rank percentile index: it used the 1-based rank as a 0-based index. It now uses rank-1. This also fixes the IndexError at p=100.

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
