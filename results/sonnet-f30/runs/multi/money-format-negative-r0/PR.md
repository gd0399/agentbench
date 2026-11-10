# Fix #146: negative amounts get a double minus sign

branch: `fix/issue-146`

Fixes #146

## Root cause
format_currency prefixed a sign and also formatted the signed amount, producing two minus signs.

## Change
format_currency now formats abs(amount), so -5 gives '-$5.00'. All 84 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / medium / component `money`
Handoffs: researcher → coder → generalist → open_pr
Recovered errors: 2
</details>

_Opened automatically by agentbench._
