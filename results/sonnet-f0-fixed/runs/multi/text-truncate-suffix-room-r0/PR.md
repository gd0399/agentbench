# Fix #118: headline() is longer than the limit

branch: `fix/issue-118`

Fixes #118

## Root cause
toolkit/text.py line 16, in truncate(): `return s[:limit] + suffix` slices to `limit` characters and then appends the suffix. The result is limit+len(suffix) characters long. The suffix length is already validated against the limit at line 12, which shows the intent that the suffix counts toward the limit. It should be `s[:limit - len(suffix)] + suffix`. report.headline (report.py:30) just delegates to text.truncate(title_case(title), limit), so fixing truncate fixes headline. With the fix, headline('the art of war', 12) returns 'The Art o...' (9 chars + '...'). No existing test covers the over-limit truncation path; the existing tests only cover short and exact-length strings, so there is no conflict.

## Change
Fix text.truncate so the suffix counts toward the limit (s[:limit - len(suffix)] + suffix); headline now returns 'The Art o...' for limit 12. Added regression tests in tests/test_toolkit.py; full suite passes (87).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. It changes `s[:limit]` to `s[:limit - len(suffix)]` in `text.truncate`, so the suffix now counts toward the limit. This is the root cause, because `headline` only delegates to `truncate`. The existing guard `limit < len(suffix)` already ensures the slice index is never negative. Edge cases hold: limit == len(suffix) gives '...', and strings at or under the limit are returned unchanged. The full suite passes (87 tests). No existing tests were modified or weakened, and the new tests assert the correct behaviour.

Before merging, please clean up two things:
- Drop the committed `__pycache__/*.pyc` files and add them to .gitignore.
- Delete `tests/test_issue_repro.py`. It duplicates the regression tests already added to `tests/test_toolkit.py`.

Neither affects the code change itself.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
