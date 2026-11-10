# Fix #148: invoice_total fails for tax-free invoices

branch: `fix/issue-148`

Fixes #148

## Root cause
toolkit/money.py line 31, in tax(): the guard is `if rate <= 0: raise ValueError("rate must be non-negative")`. It rejects rate == 0, although the error message says only negative rates are invalid. The guard should be `rate < 0`. report.invoice_total (toolkit/report.py:26) defaults tax_rate=0 and always calls money.tax, so every tax-free invoice raises ValueError. The existing tests only use positive rates, so nothing contradicts the fix.

## Change
In money.tax(), changed guard from `rate <= 0` to `rate < 0` so zero tax rates are allowed (negative still raises ValueError). Added test_tax_negative_rate_raises to tests/test_issue_repro.py. Full suite: 86 passed.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — This fixes the root cause. `money.tax` rejected a rate of 0 even though its error message says "must be non-negative". Changing the guard to `rate < 0` matches that message. It also fixes the default call `invoice_total(lines)`, which has `tax_rate=0` as its default and was failing before.

- I ran `invoice_total([(1, 100.0)], tax_rate=0)` and the default call. Both return 100.0.
- Negative rates still raise `ValueError`.
- The full suite passes (86 tests). The existing tests were not changed, and the new tests cover zero rate, negative rate and the issue repro.

Before merging, drop the committed `__pycache__/*.pyc` files from the diff. They are build artifacts and shouldn't be in the repo. The code change itself is fine.

<details><summary>Agent trail</summary>

Triage: bug / high / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
