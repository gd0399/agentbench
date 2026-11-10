# Fix #117: truncate() shortens strings that already fit

branch: `fix/issue-117`

Fixes #117

## Root cause
Off-by-one in the length check in truncate().

## Change
Changed `<` to `<=` in truncate() so strings whose length equals the limit are returned unchanged. All 84 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → generalist → open_pr
Recovered errors: 3
</details>

_Opened automatically by agentbench._
