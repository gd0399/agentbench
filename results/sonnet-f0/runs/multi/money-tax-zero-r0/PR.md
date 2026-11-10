# Fix #148: invoice_total fails for tax-free invoices

branch: `fix/issue-148`

Fixes #148

## Root cause
toolkit/money.py line 31, in tax(): the guard is `if rate <= 0: raise ValueError("rate must be non-negative")`. It rejects rate == 0 even though the error message says only negative rates are invalid. report.invoice_total (toolkit/report.py:26) passes tax_rate=0, which is also its default, to money.tax, so it raises. The fix is to change the guard to `rate < 0`. No existing test expects tax(…, 0) to raise; test_tax only checks 0.08. The repro test tests/test_issue_repro.py fails with ValueError.

## Change
Fixed money.tax() guard from `rate <= 0` to `rate < 0` so a zero tax rate is allowed (negative still raises). Added tests/test_money_tax.py covering zero and negative rates; full suite (86) passes including the repro.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is the guard in money.tax(). It used `rate <= 0`, which contradicts its own error message ("must be non-negative"). It also made invoice_total fail with the default tax_rate=0. Changing it to `rate < 0` fixes that for every caller, not only the repro input. Negative rates still raise.

I read report.invoice_total and checked the other uses of tax(). Nothing else depends on the old behaviour.

The full suite passes (86 tests). The existing tests were not modified. The new tests cover zero and negative rates, plus an end-to-end repro test.

Before merging, drop the committed __pycache__/*.pyc files from the diff and consider adding a .gitignore. They are test-run artifacts and shouldn't be in the patch. The source change itself is a one-line fix.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
