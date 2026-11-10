# Fix #117: truncate() shortens strings that already fit

branch: `fix/issue-117`

Fixes #117

## Root cause
toolkit/text.py line 14 in truncate(): the guard `if len(s) < limit: return s` is off by one. A string whose length equals limit falls through to `s[:limit-len(suffix)] + suffix`, giving 'he...'. It should be `len(s) <= limit`. Existing tests (truncate('hello',10), truncate('hello world',8)) are unaffected and don't conflict. The caller report.py:30 also uses truncate, so it gets the same fix.

## Change
Fixed off-by-one in text.truncate(): the guard is now `len(s) <= limit`, so strings that exactly fit are returned unchanged. Full suite passes (84 tests), including the repro test tests/test_issue_repro.py and the existing truncate tests. report.py is untouched.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the `<` guard in truncate(), which treated a string of exactly `limit` characters as too long. Changing it to `<=` fixes that. The output length never exceeds `limit`. I checked these cases: ('hello',5) returns 'hello', ('hello!',5) returns 'he...', and ('abc',3) and ('abcd',3) behave correctly. The only other caller, report.headline, just passes through, so it is unaffected. The existing truncate tests are untouched and all 84 tests pass. The new regression test is appropriate.

Nit: the diff includes committed `__pycache__/*.pyc` files. Please drop them and add `__pycache__/` to .gitignore before merging. They don't affect behaviour.

<details><summary>Agent trail</summary>

Triage: bug / low / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
