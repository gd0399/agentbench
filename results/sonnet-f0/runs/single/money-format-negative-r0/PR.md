# Fix #146: negative amounts get a double minus sign

branch: `fix/issue-146`

Fixes #146

## Root cause
The sign was prepended manually and the amount was also formatted with its own minus sign.

## Change
format_currency now formats abs(amount), so negatives give '-$5.00'.

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
