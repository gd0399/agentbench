# Fix #161: invoice tax is computed before the discount

branch: `fix/issue-161`

Fixes #161

## Root cause
toolkit/report.py line 26, in invoice_total: tax is computed on the undiscounted subtotal (`money.tax(subtotal, tax_rate)`) and added to the discounted amount. For the issue's input this gives 22.5 + 2.5 = 25.0 instead of 22.5 + 2.25 = 24.75. The fix is `money.tax(discounted, tax_rate)`, or equivalently `discounted + tax(discounted)`. money.apply_discount and money.tax are correct, and no existing test contradicts this.

## Change
In report.invoice_total, compute tax on the discounted amount instead of the undiscounted subtotal. The issue example now gives 24.75, and all 84 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line fix in `report.invoice_total` is correct. It now computes tax on the discounted amount, so the issue example gives 22.5 + 2.25 = 24.75. This fixes the cause rather than special-casing the input. `money.tax` and `money.apply_discount` are unchanged, and the discount and tax defaults of 0 still work. All 84 tests pass. The new regression test in `tests/test_issue_repro.py` matches the issue, and no existing tests were modified.

Please drop the `__pycache__/*.pyc` files from the diff before merging. They are build artifacts from running the tests. Adding a `.gitignore` for `__pycache__/` would stop this happening again. This doesn't affect the logic of the fix.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
