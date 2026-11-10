# Fix #118: headline() is longer than the limit

branch: `fix/issue-118`

Fixes #118

## Root cause
toolkit/text.py line 16, in truncate(): `return s[:limit] + suffix` keeps `limit` characters and then appends the suffix, so the result is limit+len(suffix) long. It should be `s[:limit - len(suffix)] + suffix`. The guard `limit < len(suffix)` on line 12 already shows the limit is meant to include the suffix. report.headline (report.py:30) just calls text.truncate(title_case(title), limit), so the fix belongs in text.truncate. The expected 'The Art o...' is 12 chars, not 11 as the triage says, which matches limit=12. Existing tests only cover the no-truncation cases (short and exact), so none contradict this.

## Change
Fixed text.truncate to keep limit - len(suffix) characters before the suffix, so the result never exceeds limit. headline('the art of war', 12) now returns 'The Art o...'. Added edge-case tests (limit == len(suffix), len == limit). All 86 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was in text.truncate, which sliced `s[:limit]` and then appended the suffix. That made the result `limit + len(suffix)` characters long. The fix slices `s[:limit - len(suffix)]`, so the result never exceeds `limit`. headline() calls truncate, so it is fixed too.

I checked the edge cases:
- `limit == len(suffix)` gives just the suffix.
- An empty suffix still works.
- `len(s) <= limit` returns the string unchanged.
- `limit < len(suffix)` still raises ValueError.

All 86 tests pass. No existing tests were modified, and the new tests cover the issue and the boundaries.

Nit: the diff includes committed `__pycache__/*.pyc` files. Drop them and add `__pycache__/` to `.gitignore` before merging. This doesn't affect the code change.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
