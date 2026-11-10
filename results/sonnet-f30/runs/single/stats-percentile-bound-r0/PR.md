# Fix #109: percentile(…, 100) raises ValueError

branch: `fix/issue-109`

Fixes #109

## Root cause
The bounds check used `p >= 100`, which rejected p=100 even though the docstring says p is in [0, 100].

## Change
Changed the bounds check in percentile() so p=100 is accepted. Added a repro test. The full suite passes (84 tests).

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
