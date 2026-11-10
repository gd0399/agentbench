# Fix #119: word_count counts extra words with repeated spaces

branch: `fix/issue-119`

Fixes #119

## Root cause
toolkit/text.py line 20, word_count does `len(s.split(" "))`. Splitting on a single space gives an empty string for each extra, leading or trailing space, and those get counted as words. '  the quick  brown fox ' splits into 8 pieces. The empty string also returns 1 instead of 0. Using `s.split()` (any run of whitespace) fixes both cases. word_count has no docstring and no existing tests, so nothing contradicts the requested behaviour.

## Change
word_count in toolkit/text.py now uses s.split() instead of s.split(" "). Repeated, leading and trailing whitespace no longer count as words, and '' returns 0. The repro tests in tests/test_issue_repro.py are kept as the regression tests. The full suite passes (84 passed, 0 failed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was split(" "), which produces empty strings for repeated, leading and trailing spaces. Changing it to split() fixes that. The change is one line and matches how title_case and initials already tokenize.

I ran the issue input and it returns 4. '' and whitespace-only strings return 0. Tabs and newlines are handled. All 84 tests pass. No existing tests were modified. The only test change is the new tests/test_issue_repro.py, which covers the issue input and the empty string.

Before merging, please drop the committed __pycache__/*.pyc files from the diff. They are build artifacts, and a .gitignore entry for __pycache__/ would stop them coming back. They don't affect behaviour. Optionally, move the new tests into test_toolkit.py to match the existing layout.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
