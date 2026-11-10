# Fix #128: flatten ignores tuples

branch: `fix/issue-128`

Fixes #128

## Root cause
toolkit/seq.py line 13, in flatten(): `isinstance(item, list)` only recurses into lists, so tuples are appended unflattened. The fix is to use `isinstance(item, (list, tuple))`. Strings and bytes must not be flattened, because that would recurse forever on single-character strings. There are no existing flatten tests or docstring, so nothing conflicts.

## Change
flatten() now recurses into tuples as well as lists (`isinstance(item, (list, tuple))`). Strings and bytes are left intact. I added regression tests for tuples, nested mixed input and string preservation in tests/test_toolkit.py. All 87 tests pass, including tests/test_issue_repro.py.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The fix is a one-line change in `flatten`: `isinstance(item, list)` became `isinstance(item, (list, tuple))`. It addresses the root cause, because the recursion check now covers tuples at any nesting depth. Strings and bytes are still not expanded, so there is no infinite recursion on a one-character string. All 87 tests pass. The new tests cover tuples, nested mixed input and string preservation, and no existing tests were modified.

Before merging, please make these two cleanups:
- Drop the committed `__pycache__/*.pyc` files from the diff, and add `__pycache__/` to `.gitignore` if it isn't there already.
- `tests/test_issue_repro.py` duplicates `test_flatten_tuples` from `tests/test_toolkit.py`. Keep only one copy.

Other iterables such as sets, generators and `range` are still not flattened. That is reasonable, since the issue only asks for tuples.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
