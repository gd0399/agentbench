# Fix #141: 100% discount raises ValueError

branch: `fix/issue-141`

Fixes #141

## Root cause
toolkit/money.py line 5, in apply_discount: the validation `percent < 0 or percent >= 100` rejects 100. The boundary should be `percent > 100`. The message and the issue both say 100 is valid. The existing test_discount_bounds only checks 120, so it still passes after the fix. The formula on line 7 already returns 0.0 for 100. report.invoice_total calls apply_discount, so it is affected too.

## Change
Allow 100% discount in money.apply_discount (validation now `percent < 0 or percent > 100`). Added regression tests for 100, 0, negative, and invoice_total with a full discount. All 87 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / medium / component `money`
Handoffs: researcher → coder → reviewer → verifier → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
