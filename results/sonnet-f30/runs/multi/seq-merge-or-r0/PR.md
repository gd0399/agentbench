# Fix #138: merge_sorted raises IndexError

branch: `fix/issue-138`

Fixes #138

## Root cause
toolkit/seq.py line 62, merge_sorted: the loop condition is `while i < len(a) or j < len(b)`. It should be `and`. With `or`, the body still runs after one list is exhausted and indexes a[i] or b[j] out of range, which raises IndexError. Even equal-length inputs like [1,3],[2,4] fail, because one list runs out first. Changing the condition to `and` fixes it, since the trailing `out.extend(a[i:])` and `out.extend(b[j:])` already handle the leftovers. The repro test, tests/test_issue_repro.py, covers unequal, empty and equal-length inputs. All 5 cases fail on the current code. The existing tests do not cover merge_sorted, so nothing contradicts the requested behaviour.

## Change
Fixed merge_sorted in toolkit/seq.py: the loop condition is now `while i < len(a) and j < len(b)` (it was `or`). The existing trailing extends still append the leftovers. I added the 5 regression cases to tests/test_toolkit.py as test_merge_sorted. The full suite passes (92 passed, 0 failed), including all 5 repro cases. I left tests/test_issue_repro.py in place because I have no tool to delete files, so those 5 cases now exist in both files.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. It changes `or` to `and` in the `merge_sorted` loop. The old condition indexed `a[i]` or `b[j]` after one list was exhausted, which caused the IndexError. The existing `out.extend(a[i:])` and `out.extend(b[j:])` already append the leftovers. I ran the full suite and 92 tests passed. The new `test_merge_sorted` in tests/test_toolkit.py covers the issue case, the reversed case, either side empty, and interleaved input. No existing tests were modified or removed.

Please clean up before merging:
- Delete tests/test_issue_repro.py. It duplicates `test_merge_sorted` in tests/test_toolkit.py.
- Drop the `__pycache__/*.pyc` files from the diff and add `__pycache__/` to .gitignore if it isn't there already.

Neither affects behaviour, so I'm approving.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
