# Fix #138: merge_sorted raises IndexError

branch: `fix/issue-138`

Fixes #138

## Root cause
toolkit/seq.py line 62, merge_sorted: the loop condition uses `or` (`while i < len(a) or j < len(b)`). Once one list is exhausted, the loop body still evaluates a[i] <= b[j] with an out-of-range index, which raises IndexError. For [1],[2,3]: after taking 1, i=1 is out of range for a. The fix is to use `and` (`while i < len(a) and j < len(b)`). The trailing `out.extend(a[i:])` and `out.extend(b[j:])` already handle the leftovers. Empty inputs fail the same way. No docs or tests contradict the expected behaviour.

## Change
Fixed merge_sorted loop condition from `or` to `and` in toolkit/seq.py so indexing stops once either list is exhausted; the trailing extends append leftovers. Full suite passes (84), including repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the `or` loop condition. It let `a[i]` or `b[j]` be indexed after one list was exhausted. Changing it to `and` is correct, and the two `extend` calls after the loop already append the leftovers. I ran the repro and edge cases: `([1],[2,3])`, `([2,3],[1])`, `([],[])` and `([1,3],[1,2])` all give correct sorted output. The full suite passes (84). No existing tests were modified. The new tests in `tests/test_issue_repro.py` cover the issue case and the empty-list cases. One cleanup before merge: the diff includes `__pycache__/*.pyc` files. They are not in the repo file listing, so they look like test-run artifacts. Don't commit them, and consider adding a `.gitignore`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
