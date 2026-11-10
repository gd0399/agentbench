# Fix #129: flatten only flattens one level

branch: `fix/issue-129`

Fixes #129

## Root cause
toolkit/seq.py flatten() (lines 10-17): for list/tuple items it calls `out.extend(item)` (line 14), which adds the sub-elements without recursing, so only one nesting level is flattened. Nested lists/tuples deeper than that remain. The fix is to recurse into list/tuple items, e.g. `out.extend(flatten(item))`. flatten has no docstring, no tests and no README mention, so nothing documents one-level behaviour.

## Change
Made seq.flatten recurse into nested lists/tuples (out.extend(flatten(item))) so it flattens all levels. Repro and full suite pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct. `flatten` now recurses into nested lists and tuples. The old code only called `extend(item)` one level down. The change is a single line and fixes the root cause, not just the example in the issue. Strings are not split, because only list and tuple are recursed into. Empty nested lists are handled. The full suite passes (85 tests). The new tests in tests/test_issue_repro.py cover deep lists and mixed tuple/list nesting, and no existing tests were changed.

Before merging, please drop the committed `__pycache__/*.pyc` files from the diff and add them to .gitignore. They are build artifacts. You could also move the new tests into tests/test_toolkit.py instead of a separate "repro" file. Neither is a blocker.

<details><summary>Agent trail</summary>

Triage: bug / high / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 2
</details>

_Opened automatically by agentbench._
