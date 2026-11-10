# Fix #142: split_bill loses cents

branch: `fix/issue-142`

Fixes #142

## Root cause
toolkit/money.py line 14, in split_bill: `round(with_tip // people, 2)` uses floor division (`//`) instead of true division (`/`), so the per-person share is floored to a whole number (100 // 3 = 33.0) before rounding to cents. Fix: `round(with_tip / people, 2)`. Existing tests (100/4 = 25.0, with 20% tip = 30.0) divide evenly and still pass, so they don't conflict with the fix.

## Change
In toolkit/money.py split_bill, replaced floor division (//) with true division (/) so the per-person share keeps cents (100, 3 -> 33.33). Full suite passes (84 passed), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was `//` (floor division) in split_bill, and changing it to `/` fixes it. It is a one-token change.

- I ran the full suite: 84 passed. The existing tests were not modified. The only test change is the new regression test `tests/test_issue_repro.py`.
- Edge cases behave correctly: (100,3) gives 33.33, (100,3,15) gives 38.33, (10,3) gives 3.33, and (0,3) gives 0.0.
- The `people <= 0` guard is untouched.

Before merging, drop the `__pycache__/*.pyc` files from the diff. They are build artifacts and shouldn't be committed. Adding `__pycache__/` to `.gitignore` would stop this recurring. This doesn't affect the code change.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
