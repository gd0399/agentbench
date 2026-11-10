# Fix #143: tip is applied as a multiplier, not a percent

branch: `fix/issue-143`

Fixes #143

## Root cause
toolkit/money.py line 13 in split_bill: `with_tip = total * (1 + tip_percent)` uses tip_percent as a raw multiplier. With tip_percent=20 this gives 100*21/4 = 525.0. It should be `total * (1 + tip_percent / 100)`, consistent with apply_discount in the same file, which divides percent by 100. The existing tests only cover tip_percent=0, so they don't conflict with the fix.

## Change
Fixed split_bill to treat tip_percent as a percentage (tip_percent / 100), matching apply_discount; added regression test in tests/test_toolkit.py. Full suite passes (85).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix in toolkit/money.py is correct and minimal. `split_bill` now computes `total * (1 + tip_percent / 100)`. That fixes the cause, which was the unit, and isn't special-cased to the issue's inputs. `split_bill(100, 4, tip_percent=20)` returns 30.0. The default `tip_percent=0` behaves as before. I found no other callers of `split_bill` that pass a fractional tip. The full suite passes (85), and the existing tests were not changed or weakened.

Please clean up before merging:
- Remove the committed `__pycache__/*.pyc` files. Consider adding a `.gitignore`.
- Delete `tests/test_issue_repro.py`. It duplicates the regression test you added to `tests/test_toolkit.py`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
