# Fix #139: last_n(items, 0) returns everything

branch: `fix/issue-139`

Fixes #139

## Root cause
toolkit/seq.py lines 74-77, last_n: the guard is `if n < 0: return []`, so n == 0 falls through to `items[-n:]`, which is `items[0:]` (-0 == 0) and returns the whole list. Fix: change the guard to `n <= 0`. Negative n already returns [] and n > len works via slicing. The existing test only covers n=2, so nothing documents or tests the n=0 behaviour and the fix doesn't conflict with it.

## Change
Changed last_n guard in toolkit/seq.py from `n < 0` to `n <= 0` so n=0 returns [] (items[-0:] was the whole list). Added regression tests for n=0, negative n, and n>len in tests/test_issue_repro.py; full suite passes (86 passed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct. The root cause is that `items[-0:]` equals `items[0:]`, which returns the whole list. Changing the guard from `n < 0` to `n <= 0` handles that. The change is one line and the existing tests are untouched. I ran the full suite and 86 passed. I also checked the other `[-k:]` slice in the repo, in `rotate`. It is safe, because `k` is reduced modulo `len(items)` and `k == 0` still returns the right result. The new regression tests cover n=0, a negative n, and n larger than the length.

Before merging, drop the `__pycache__/*.pyc` files from the commit. They are build artifacts that showed up in the diff. Adding a `.gitignore` entry for `__pycache__/` would stop this happening again. This doesn't affect the code change itself.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
