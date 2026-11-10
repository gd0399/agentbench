# Fix #140: apply_discount returns the discount instead of the price

branch: `fix/issue-140`

Fixes #140

## Root cause
apply_discount computed price * percent / 100, which is the discount amount, not the price after the discount. report.invoice_total also calls it expecting the discounted price, so it gets the same fix.

## Change
apply_discount now returns the discounted price, price * (1 - percent/100). I added a repro test in tests/test_issue_repro.py. The full suite passes (82 tests).

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
