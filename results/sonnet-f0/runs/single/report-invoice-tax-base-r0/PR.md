# Fix #161: invoice tax is computed before the discount

branch: `fix/issue-161`

Fixes #161

## Root cause
In report.invoice_total, tax was computed on the pre-discount subtotal (money.tax(subtotal, ...)) instead of the discounted amount.

## Change
invoice_total now computes tax on the discounted amount. The issue's example returns 24.75, and the full suite passes (84 tests), including the new repro test.

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
