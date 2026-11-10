# Fix #121: title_case lowercases the first word

branch: `fix/issue-121`

Fixes #121

## Root cause
toolkit/text.py title_case (lines 31-35): the loop enumerates words but never uses the index `i`. The condition `if w.lower() in minor` lowercases minor words, including the first word. It should be `if i > 0 and w.lower() in minor`. The existing test test_title_case_mixed ('hELLO wORLD') is unaffected. The same function is used by report.py:30.

## Change
In text.title_case, only lowercase minor words when i > 0, so the first word is always capitalized. Added a regression test in tests/test_toolkit.py. The full suite passes (83 tests), including test_title_case_mixed and the report tests that go through report.py:30. I left tests/test_issue_repro.py in place; it's now redundant but harmless.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / low / component `text`
Handoffs: researcher → coder → reviewer → verifier → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
