# Fix #140: apply_discount returns the discount instead of the price

branch: `fix/issue-140`

Fixes #140

## Root cause
toolkit/money.py line 7, apply_discount: `return round(price * percent / 100, 2)` returns the discount amount (price*percent%) instead of the discounted price. It should be `round(price * (1 - percent / 100), 2)` (or price - discount). The caller report.invoice_total (toolkit/report.py:25) treats the result as the discounted subtotal, so it is also wrong whenever discount_percent is non-zero (and wrongly returns 0 with no discount). The existing test only checks bounds (ValueError for 120), so there is no conflict.

## Change
Fixed money.apply_discount to return the discounted price, round(price * (1 - percent/100), 2), instead of the discount amount. report.invoice_total already treats the result as the discounted subtotal, so I left it unchanged. All 82 tests pass, including the repro. Edge cases: percent 0 returns the full price and percent 100 returns 0.0.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and addresses the root cause. apply_discount now returns price * (1 - percent/100), rounded to 2 places. The validation is unchanged. I checked these cases:
- apply_discount(80, 25) returns 60.0.
- apply_discount(19.99, 15) returns 16.99.
- The only other caller, report.invoice_total, treats the result as the discounted subtotal. It was producing wrong totals before and is now correct: [(2, 40.0)] at 25% discount and 10% tax gives 66.0.
- All 82 tests pass, and no existing tests were modified. The new repro test is a reasonable addition.

Before merging, drop the __pycache__/*.pyc files from the diff. They are build artifacts, and adding a .gitignore entry for them would be sensible. The actual change is a one-line edit to money.py plus the new test.

<details><summary>Agent trail</summary>

Triage: bug / high / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
