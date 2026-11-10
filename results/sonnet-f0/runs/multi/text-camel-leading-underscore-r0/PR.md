# Fix #126: camel_to_snake adds a leading underscore

branch: `fix/issue-126`

Fixes #126

## Root cause
toolkit/text.py camel_to_snake (lines 48-54): the loop appends "_" for every uppercase char, including index 0, so 'Value' becomes '_value'. It should only add "_" when i > 0. The existing test only covers lowerCamel input, so it does not conflict.

## Change
camel_to_snake no longer prefixes an underscore when the first character is uppercase (`c.isupper() and i > 0`) in toolkit/text.py. I added a regression test to tests/test_toolkit.py and a .gitignore for __pycache__/ and *.pyc. I removed the scratch repro test and all .pyc files from the diff. All 84 tests pass. The new test keeps one blank line before it, matching the file's existing style, since the surrounding tests use one rather than two.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. `c.isupper() and i > 0` addresses the root cause, which is that the underscore was added at index 0. 'Value' now gives 'value', and 'A', '' and 'FooBar' behave correctly. All 84 tests pass, and the existing test is unchanged. The new regression test covers the issue case.

Two small notes, neither blocking:
- The `.gitignore` is unrelated to the issue. It's harmless, but it would be cleaner as a separate commit.
- Acronyms such as 'HTTPResponse' still give 'h_t_t_p_response'. That behaviour was already there and is outside this issue.

<details><summary>Agent trail</summary>

Triage: bug / low / component `text`
Handoffs: researcher → coder → reviewer → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
