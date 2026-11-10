# Fix #117: truncate() shortens strings that already fit

branch: `fix/issue-117`

Fixes #117

## Root cause
toolkit/text.py line 14 in truncate(): the guard is `if len(s) < limit: return s`. It should be `<=`. A string whose length equals the limit falls through to `s[:limit-len(suffix)] + suffix`, which gives 'he...'. The existing tests (truncate('hello',10) and truncate('hello world',8)) don't conflict with the fix. The caller report.headline also uses truncate and gets the same fix.

## Change
Fixed off-by-one in text.truncate(): guard changed from `len(s) < limit` to `len(s) <= limit`, so strings that exactly fit are returned unchanged. Added regression tests (exact fit, and one-over-limit still truncates) to tests/test_toolkit.py. Full suite: 86 passed. report.py was not changed.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct. In `truncate`, changing `<` to `<=` fixes the root cause: a string whose length equals the limit now fits. A string one character over the limit still truncates to exactly `limit` characters. `report.headline` is the only other caller, and it benefits from the same fix. The full suite passes (86 passed), and no existing tests were changed or weakened.

Before merging, please clean up two things:
- Remove the committed `__pycache__/*.pyc` files and add them to `.gitignore`.
- Delete `tests/test_issue_repro.py`. It duplicates `test_truncate_exact_fit`, which is already in `tests/test_toolkit.py`.

Neither affects behaviour.

<details><summary>Agent trail</summary>

Triage: bug / low / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
