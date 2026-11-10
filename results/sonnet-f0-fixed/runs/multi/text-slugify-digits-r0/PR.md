# Fix #116: slugify strips numbers

branch: `fix/issue-116`

Fixes #116

## Root cause
toolkit/text.py line 7, in slugify: re.sub(r"[^a-z]+", "-", s) treats digits as non-slug characters and replaces them with "-". The character class should be [^a-z0-9]+. The existing test (test_slugify, 'Hello, World!') has no digits and is unaffected, so there is no conflict with the tests or docs.

## Change
Fixed slugify in toolkit/text.py by changing the regex from [^a-z]+ to [^a-z0-9]+, so digits are kept. 'Top 10 Tips' now gives 'top-10-tips'. The full suite passes (84 passed), including the repro test and the existing 'Hello, World!' test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line regex change from [^a-z] to [^a-z0-9] fixes the root cause. Digits were being treated as separators, and no other code uses this pattern. The existing 'Hello, World!' test still passes, and so does the new repro test. The full suite is 84 passed. The new test is a separate file, and no existing tests were modified. Before merging, drop the committed __pycache__/*.pyc files from the diff. They are build artifacts and should be gitignored. You could also move the repro test into tests/test_toolkit.py next to test_slugify, but that is optional.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
