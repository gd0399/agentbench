# Fix #130: dedupe() does not remove duplicates

branch: `fix/issue-130`

Fixes #130

## Root cause
In toolkit/seq.py dedupe() (lines 20-27), the `seen` set is never updated. After `out.append(x)` on line 26 there is no `seen.add(x)`, so `x not in seen` is always True and every item is kept. The fix is to add `seen.add(x)` after the append. The docstring requires "Remove duplicates, preserving first-seen order". tests/test_toolkit.py has no dedupe test, so nothing contradicts the requested behaviour.

## Change
Fix dedupe(): add missing seen.add(x) so duplicates are dropped while preserving first-seen order. All tests pass, including the repro.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line fix is correct. `seen.add(x)` was missing, so `seen` stayed empty and nothing was ever filtered. This is the root cause, and the fix doesn't special-case the issue's input.

- The full suite passes (84 tests).
- `dedupe([3,1,3,2,1])` returns `[3,1,2]`.
- `dedupe([])` returns `[]`.
- `dedupe("aab")` returns `['a','b']`.
- Unhashable items such as lists raise TypeError. The original code did too, because it also tested membership in a set. This is outside the issue's scope.
- The new regression test in `tests/test_issue_repro.py` is reasonable, and no existing tests were changed.

Nit: the diff includes many `__pycache__/*.pyc` files. Make sure they aren't committed, and add `__pycache__/` to `.gitignore` if it isn't there already. This doesn't affect the code change.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
