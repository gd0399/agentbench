# Fix #117: truncate() shortens strings that already fit

branch: `fix/issue-117`

Fixes #117

## Root cause
Off-by-one in toolkit/text.py truncate(): `len(s) < limit` treated strings that exactly fit as needing truncation.

## Change
Changed the length check in truncate() from `<` to `<=`, so strings whose length equals the limit are returned unchanged. Added tests/test_issue_repro.py; the full suite passes.

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
