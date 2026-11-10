# Fix #147: format_currency has no thousands separator

branch: `fix/issue-147`

Fixes #147

## Root cause
The format spec in format_currency was ':.2f', which has no grouping option.

## Change
format_currency now uses the ',' format option, so 1234.5 gives '$1,234.50'. I added tests/test_issue_repro.py. The full suite passes (84 tests).

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
