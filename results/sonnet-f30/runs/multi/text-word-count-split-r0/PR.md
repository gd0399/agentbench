# Fix #119: word_count counts extra words with repeated spaces

branch: `fix/issue-119`

Fixes #119

## Root cause
toolkit/text.py line 20, word_count uses `len(s.split(" "))`. Splitting on a literal single space yields an empty string for every leading, trailing or repeated space, and those empty strings are counted as words. The input '  the quick  brown fox ' splits into 8 items. The same bug makes word_count('') return 1 instead of 0. The fix is to use `s.split()` with no argument, which splits on runs of whitespace and drops empty strings. No docs or tests contradict this: no existing test covers word_count, and it has no docstring.

## Change
word_count now uses s.split() instead of s.split(" "), so leading, trailing and repeated whitespace is ignored. word_count('') now returns 0. Full suite passes (84 tests), including both repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was `split(" ")`, which yields empty strings for leading, trailing and repeated spaces. `split()` with no argument is the correct fix. It also handles tabs and newlines, and returns 0 for '' and for whitespace-only strings. The change is one line. It matches how `title_case` and `report.py` already tokenize. The full suite passes (84 tests) and no existing tests were modified. The new tests in tests/test_issue_repro.py cover the issue's repro and the empty-string case. Before merging, drop the committed `__pycache__/*.pyc` files from the diff. They are build artifacts and shouldn't be tracked, so add them to .gitignore if they aren't already ignored. This doesn't affect the fix. You could also move the new tests into test_toolkit.py instead of a separate "issue_repro" file.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
