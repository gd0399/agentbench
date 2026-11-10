# Fix #122: title_case keeps stray capitals

branch: `fix/issue-122`

Fixes #122

## Root cause
toolkit/text.py line 35 in title_case: `out.append(w[:1].upper() + w[1:])` uppercases only the first character and keeps the rest of the word as is, so stray capitals survive ('hELLO' -> 'HELLO'). The remainder should be lowercased: `w[:1].upper() + w[1:].lower()`. Minor words are already lowercased (line 33). The existing tests ('the lord of the rings', 'a tale of two cities') are all lowercase input and stay compatible with the fix. Side effect to note: toolkit/report.py:30 calls title_case, so acronyms in titles would also be lowercased.

## Change
title_case now lowercases the rest of each non-minor word (`w[:1].upper() + w[1:].lower()` in toolkit/text.py), so 'hELLO wORLD' gives 'Hello World'. I added a regression test to tests/test_toolkit.py. All 85 tests pass, including the existing report.headline test. Side effect for the reviewer: report.headline (report.py:30) calls title_case, so acronyms in titles such as 'NASA' will now become 'Nasa'. I left tests/test_issue_repro.py in place instead of deleting it, since the rules say not to delete tests. It now duplicates the new regression test and can be removed if you prefer.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → verifier → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
