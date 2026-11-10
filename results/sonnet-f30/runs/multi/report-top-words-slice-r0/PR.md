# Fix #160: top_words returns one word too few

branch: `fix/issue-160`

Fixes #160

## Root cause
toolkit/report.py line 20, in top_words: `return ranked[:n - 1]` slices one element too few. It should be `ranked[:n]`. Ranking by (-count, word) is correct. Note that n=0 would give ranked[:-1], which returns almost everything, so the fix also corrects that case.

## Change
Fixed off-by-one in report.top_words: slice is now ranked[:max(n, 0)] instead of ranked[:n - 1], so n=0 or negative n returns an empty list. All 83 tests pass, including the repro. I didn't add a separate n=0 test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and addresses the root cause. `ranked[:n - 1]` was an off-by-one, and `ranked[:max(n, 0)]` fixes it. I ran the tests and probed edge cases:
- `top_words('z y x', 2)` returns `['x', 'y']`.
- n=0 and n=-1 return `[]`.
- An empty string returns `[]`.
- `top_words('a a b', 1)` returns `['a']`.
- All 83 tests pass.

The `max(n, 0)` clamp is a small addition beyond the minimal change. Without it, a negative n would slice off the tail, so I think it's justified. The new test in `tests/test_issue_repro.py` is a legitimate regression test, and no existing tests were modified.

Nits that shouldn't block the merge:
- The diff contains `__pycache__/*.pyc` files. Please don't commit them, and consider adding a `.gitignore`.
- Add an n=0 test, since you changed that behaviour. Consider moving the repro test into `test_toolkit.py`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
