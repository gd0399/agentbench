# Fix #115: slugify leaves a trailing dash

branch: `fix/issue-115`

Fixes #115

## Root cause
toolkit/text.py slugify (lines 5-8): the input is stripped of whitespace first, then re.sub(r"[^a-z0-9]+", "-", s) turns trailing punctuation ("!") into a "-". Leading or trailing punctuation therefore becomes a leading or trailing dash, e.g. 'hello-world-'. The fix is to strip "-" after the substitution, with s.strip("-"). This doesn't conflict with the existing test, 'Top 10 Tips' -> 'top-10-tips'.

## Change
slugify now strips leading/trailing dashes after the substitution (s.strip("-")), so '  Hello, World! ' -> 'hello-world'. Full suite passes (84 passed), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is that the regex substitution turns trailing or leading punctuation into "-". Stripping "-" after the substitution fixes that for any input, not just the repro string. Leading dashes are covered too, for example "!Hi" and "...a". The change is one line, and the full suite passes (84 tests). The new regression test is reasonable, and no existing tests were changed. Before merging, drop the committed __pycache__/*.pyc files from the diff. They are build artifacts and should be gitignored.

<details><summary>Agent trail</summary>

Triage: bug / low / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
