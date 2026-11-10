# Fix #142: split_bill loses cents

branch: `fix/issue-142`

Fixes #142

## Root cause
toolkit/money.py line 14, in split_bill: `round(with_tip // people, 2)` uses floor division (`//`) instead of true division (`/`). So 100 // 3 = 33.0 and the cents are lost before rounding. The fix is `round(with_tip / people, 2)`. Existing tests (100/4 = 25.0, and 100 with 20% tip over 4 = 30.0) divide evenly, so they pass with either operator and don't contradict the fix. The repro test tests/test_issue_repro.py fails on the current code (33.0 != 33.33); the other 83 tests pass.

## Change
Fixed split_bill by changing `//` to `/` in toolkit/money.py. Kept the regression test in tests/test_issue_repro.py. Removed all __pycache__/.pyc files from the tree and added a .gitignore for them. The full suite passed (84 tests) before cleanup. I didn't re-run it afterwards, to avoid regenerating the .pyc files. The diff now has no binary files.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / medium / component `money`
Handoffs: researcher → coder → reviewer → coder → reviewer → verifier → open_pr
Recovered errors: 2
</details>

_Opened automatically by agentbench._
