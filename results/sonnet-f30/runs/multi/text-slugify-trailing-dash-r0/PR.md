# Fix #115: slugify leaves a trailing dash

branch: `fix/issue-115`

Fixes #115

## Root cause
toolkit/text.py slugify (lines 5-8): after s.strip().lower(), re.sub(r"[^a-z0-9]+", "-", s) turns trailing punctuation ("!") into "-" and nothing strips leading/trailing dashes afterwards. The whitespace strip happens before punctuation replacement, so "hello, world! " -> "hello-world!" -> "hello-world-". Fix: strip "-" from the result after the re.sub (e.g. return s.strip("-")). This doesn't conflict with the existing test (test_slugify_digits).

## Change
slugify now strips leading/trailing dashes after the regex substitution (return s.strip("-")). Added regression test in tests/test_toolkit.py. Full suite: 85 passed.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. `s.strip("-")` after the regex substitution addresses the root cause. The regex turns leading and trailing punctuation into dashes, and the old code returned them unstripped. I ran the full suite and 85 tests pass. Edge cases also behave sensibly:
- '!!!' returns '' and '' returns ''.
- '--a--' returns 'a'.
- 'a  b' returns 'a-b'.
- The existing 'Top 10 Tips' test is unaffected.

No existing tests were modified. The only change to tests/test_toolkit.py is the added regression test.

Cleanup before merge:
- Drop the committed `__pycache__/*.pyc` files and don't commit them.
- Delete tests/test_issue_repro.py. It duplicates the regression test already added to tests/test_toolkit.py.

Neither point affects the correctness of the change.

<details><summary>Agent trail</summary>

Triage: bug / low / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
