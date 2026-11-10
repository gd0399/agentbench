# Fix #148: invoice_total fails for tax-free invoices

branch: `fix/issue-148`

Fixes #148

## Root cause
money.tax used `rate <= 0` as its validity check, which rejected zero even though the error message says "non-negative".

## Change
money.tax now accepts a rate of 0; only negative rates raise ValueError. Added repro tests; full suite passes.

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
