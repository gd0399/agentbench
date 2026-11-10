# Fix #116: slugify strips numbers

branch: `fix/issue-116`

Fixes #116

## Root cause
toolkit/text.py line 7, in slugify: re.sub(r"[^a-z]+", "-", s) treats every non-letter, digits included, as a separator. Because of this, "10" is replaced by "-" and then collapsed. The character class should be [^a-z0-9]+. The existing test only covers 'Hello, World!', so it doesn't conflict with the requested behaviour.

## Change
Fixed slugify in toolkit/text.py to keep digits by changing the regex from [^a-z]+ to [^a-z0-9]+. Added a regression test in tests/test_toolkit.py. All 85 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line regex change from [^a-z]+ to [^a-z0-9]+ fixes the root cause. Digits were being treated as separators. All 85 tests pass, and the existing slugify test is untouched. The regression test is added to tests/test_toolkit.py.

Nits to clean up before merge:
- tests/test_issue_repro.py duplicates the test added to test_toolkit.py. Delete it.
- The diff contains __pycache__/*.pyc files. Remove them from the patch and add __pycache__/ to .gitignore.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
