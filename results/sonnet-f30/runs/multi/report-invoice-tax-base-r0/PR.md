# Fix #161: invoice tax is computed before the discount

branch: `fix/issue-161`

Fixes #161

## Root cause
toolkit/report.py line 26, invoice_total: tax is computed on the pre-discount `subtotal` (`money.tax(subtotal, tax_rate)`) instead of on `discounted`. For the issue's example, 22.5 + 2.5 = 25.0 instead of 22.5 + 2.25 = 24.75. The fix is `round(discounted + money.tax(discounted, tax_rate), 2)`. money.apply_discount and money.tax are correct. No existing tests or docs cover invoice_total, so there is no conflict.

## Change
invoice_total now computes tax on the discounted amount instead of the subtotal. Full suite passes (84), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. It changes `money.tax(subtotal, ...)` to `money.tax(discounted, ...)` in `invoice_total`, which is the root cause. The issue's repro now returns 24.75 (25 → 22.5 after discount → 2.25 tax). With no discount the result is unchanged (27.5), and an empty invoice returns 0.0. All 84 tests pass. The new regression test is additive, and no existing tests were modified.

One nit: the diff includes `__pycache__/*.pyc` files. These are build artifacts and shouldn't be committed. The repository file listing doesn't show them, so they are probably leftovers from the test run. Make sure they are excluded or gitignored before merging.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
