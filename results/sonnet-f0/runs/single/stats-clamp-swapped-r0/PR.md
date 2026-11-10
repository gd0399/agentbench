# Fix #113: clamp() returns the lower bound for in-range values

branch: `fix/issue-113`

Fixes #113

## Root cause
clamp computed min(lo, max(x, hi)) instead of min(hi, max(x, lo)), so it always returned lo for in-range values.

## Change
Fixed clamp() by swapping the min/max bounds; added repro test; full suite passes.

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
