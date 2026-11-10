# Fix #121: title_case lowercases the first word

branch: `fix/issue-121`

Fixes #121

## Root cause
toolkit/text.py title_case (lines 31-35): the loop enumerates `i` but never uses it. Line 32 `if w.lower() in minor:` lowercases any minor word, including the first word at i == 0. The fix is to change the condition to `if i > 0 and w.lower() in minor:`. The existing test test_title_case_mixed ('hELLO wORLD') is unaffected. Caller toolkit/report.py:30 also uses title_case, so its output changes the same way for titles that start with a minor word. No conflict with docs or tests.

## Change
Fixed title_case in toolkit/text.py so the first word is always capitalized, using `if i > 0 and w.lower() in minor`. Added regression test test_title_case_first_word_minor in tests/test_toolkit.py. The full suite passes (83 tests), including the repro test and test_title_case_mixed. No report tests depend on a lowercase leading minor word.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The change `if i > 0 and w.lower() in minor` fixes the root cause: the first word is now always capitalized, and minor words in later positions are still lowercased. It isn't special-cased to the issue's input. The only caller outside the tests is report.py, which passes the result to truncate, so its behaviour only changes when a title starts with a minor word. That is the intended fix. The full suite passes (83 tests), and no existing tests were modified or removed.

Nits to clean up before merging:
- The diff includes __pycache__/*.pyc files. They look like artifacts of running the tests, but please don't commit them. Adding a .gitignore would help.
- tests/test_issue_repro.py and test_title_case_first_word_minor in tests/test_toolkit.py assert the same thing. Keep only the one in test_toolkit.py.

<details><summary>Agent trail</summary>

Triage: bug / low / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
