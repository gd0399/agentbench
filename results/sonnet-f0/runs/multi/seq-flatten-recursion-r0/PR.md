# Fix #129: flatten only flattens one level

branch: `fix/issue-129`

Fixes #129

## Root cause
toolkit/seq.py flatten() (lines 10-17): for list/tuple items it calls `out.extend(item)`, which only splices one level and doesn't recurse into nested lists/tuples. Fix: recurse (e.g. `out.extend(flatten(item))`) or use an iterative stack. No docstring, README or existing tests specify one-level behavior, and no other code uses flatten.

## Change
flatten() now recurses into nested lists/tuples (out.extend(flatten(item))), so arbitrary depth is flattened; strings/bytes are untouched and empty nested lists work. Added a test for empty nesting and strings. Full suite passes (86).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The one-line change to `out.extend(flatten(item))` fixes the root cause, which was that nested items were extended without recursing. `flatten([1, [2, [3]]])` now returns `[1, 2, 3]`. Strings and bytes are not flattened, because only list and tuple are checked. Empty nested lists work. The full suite passes (86 tests), and no existing tests were modified. The new tests are in `tests/test_issue_repro.py`, and they cover the issue example, mixed tuple/list nesting, empty nesting, and strings.

Minor notes, not blockers:
- The diff includes `__pycache__/*.pyc` files. Please make sure they are not committed, and add them to `.gitignore` if needed.
- A self-referential list would now recurse until `RecursionError`. That is an acceptable edge case.
- You could rename `test_issue_repro.py` or move its tests into `test_toolkit.py` to match the existing layout.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
