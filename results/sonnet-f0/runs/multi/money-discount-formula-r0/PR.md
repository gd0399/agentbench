# Fix #140: apply_discount returns the discount instead of the price

branch: `fix/issue-140`

Fixes #140

## Root cause
toolkit/money.py line 7, apply_discount: `return round(price * percent / 100, 2)` returns the discount amount, not the discounted price. It should return round(price - price*percent/100, 2) (equivalently price * (1 - percent/100)). The only existing test (test_discount_bounds) checks only the ValueError bounds, so it doesn't conflict. The caller toolkit/report.py:25 (invoice_total) treats the result as the discounted subtotal, so invoice totals are also wrong. They are currently computed on the discount amount, and the fix will correct them.

## Change
Fixed money.apply_discount to return price - discount (round(price - price*percent/100, 2)) instead of just the discount amount. Added regression tests for 25%, 0% and 100%. The full suite passes (85 tests). No existing test covers invoice_total, and report.py needed no change. It already treated the result as the discounted subtotal, so invoice totals are now correct too.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is in apply_discount, which returned the discount amount. It now returns price minus discount, rounded to 2 places. The bounds check is unchanged. The full suite passes (85 tests). I also ran the function directly. apply_discount(19.99, 15) gives 16.99, and apply_discount(80, 25) gives 60.0.

I checked the only other caller, report.invoice_total. It already treats the result as the discounted subtotal and then adds tax. invoice_total([(2,40.0)], 25, 0.1) now gives 66.0, which is correct. That function was wrong before this patch and is now fixed with no change to report.py. The coder's claim matches what I found.

No existing tests were weakened or removed. The patch only adds tests.

Nits, not blockers:
- Remove the committed __pycache__/*.pyc files from the diff, and consider adding a .gitignore.
- tests/test_issue_repro.py duplicates test_discount_returns_discounted_price in test_toolkit.py. Drop one of them.
- Consider adding an invoice_total regression test, since it was silently affected by this bug.

<details><summary>Agent trail</summary>

Triage: bug / high / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
