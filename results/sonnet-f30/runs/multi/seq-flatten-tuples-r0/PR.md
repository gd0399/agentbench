# Fix #128: flatten ignores tuples

branch: `fix/issue-128`

Fixes #128

## Root cause
toolkit/seq.py line 13, in flatten(): `isinstance(item, list)` only recurses into lists, so tuples are appended as-is. Fix: use `isinstance(item, (list, tuple))`. Avoid treating str/bytes as iterables if the check is generalised further. flatten has no docstring, and no existing tests or docs cover it, so nothing conflicts with the requested behaviour.

## Change
flatten() now recurses into tuples as well as lists (strings and bytes stay scalar), with a docstring. Regression tests, including one for bytes, are in tests/test_toolkit.py. I removed the scratch repro file and the __pycache__ .pyc files from the index, and added a .gitignore for them. The diff now has only seq.py, test_toolkit.py and .gitignore. The full suite passes (86 tests).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The fix is a one-line change in flatten(): isinstance(item, list) becomes isinstance(item, (list, tuple)). That addresses the root cause, because tuples are now treated as containers like lists. Nothing else in the repo calls flatten, so no other callers are affected. Strings and bytes are still scalars, so there is no infinite-recursion risk, and the docstring says so. The new tests cover the issue example, mixed nesting, and strings/bytes staying whole. No existing tests were changed. The full suite passes (86 tests). The .gitignore only ignores pycache and .pyc files, which is harmless.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
