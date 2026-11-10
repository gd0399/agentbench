# Fix #109: percentile(…, 100) raises ValueError

branch: `fix/issue-109`

Fixes #109

## Root cause
Off-by-one in validation: `p >= 100` rejected 100 although the docstring says p is in [0, 100].

## Change
Changed bounds check in stats.percentile to allow p == 100. Added repro test; full suite passes.

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
