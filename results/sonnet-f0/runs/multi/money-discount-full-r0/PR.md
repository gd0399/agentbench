# Fix #141: 100% discount raises ValueError

branch: `fix/issue-141`

Fixes #141

## Root cause
toolkit/money.py line 5, in apply_discount: the check `percent < 0 or percent >= 100` rejects exactly 100. It should be `percent > 100`. The error message already says "between 0 and 100", which is inclusive. The existing tests don't conflict: test_discount_bounds only checks 120 raises ValueError, and 25% is the only valid case tested. The formula on line 7 gives round(50*0.0, 2) == 0.0 for 100, so only the boundary check needs to change. report.py:25 calls apply_discount, so it gets the same fix.

## Change
In money.apply_discount, changed the bounds check from `percent >= 100` to `percent > 100`, so a 100% discount returns 0.0. Added regression tests for 100% and negative percent. The existing 120 test is unchanged. Full suite: 86 passed, including the repro test and the report tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approve. The root cause was the off-by-one bound `percent >= 100`. Changing it to `percent > 100` is the minimal correct fix. Checks:
- I ran the full suite: 86 passed.
- `apply_discount(50.0, 100)` returns 0.0, and so do the float 100.0 and a price of 0.
- `report.invoice_total` with a 100% discount returns 0.0, so the only other caller is fine.
- Values above 100 (120) and negative values still raise ValueError.
- The existing `test_discount_bounds` is unchanged, so no tests were weakened.

Nits, not blocking:
- Don't commit the `__pycache__/*.pyc` files in the diff. Remove them or add them to .gitignore.
- `tests/test_issue_repro.py` duplicates `test_discount_full` in `tests/test_toolkit.py`. Keep only one.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
