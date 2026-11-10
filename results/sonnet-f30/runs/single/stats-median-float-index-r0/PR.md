# Fix #104: median() crashes with TypeError

branch: `fix/issue-104`

Fixes #104

## Root cause
`median` computed the middle index with true division, which gives a float. Indexing a list with a float raises TypeError.

## Change
Changed `mid = n / 2` to `n // 2` in `stats.median`. Added tests/test_issue_repro.py. The full suite passes (82 tests).

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
