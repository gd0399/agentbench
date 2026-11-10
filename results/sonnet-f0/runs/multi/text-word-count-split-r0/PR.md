# Fix #119: word_count counts extra words with repeated spaces

branch: `fix/issue-119`

Fixes #119

## Root cause
toolkit/text.py line 20, word_count returns len(s.split(" ")). Splitting on a single literal space yields empty strings for leading, trailing and repeated spaces, so '  the quick  brown fox ' gives ['', '', 'the', 'quick', '', 'brown', 'fox', ''], which is 8 items. It also returns 1 for '' instead of 0. Fix: use len(s.split()), which splits on any run of whitespace. No existing tests or docs cover word_count, so nothing conflicts with the requested behaviour.

## Change
word_count now uses len(s.split()) so runs of whitespace and leading/trailing spaces are ignored; '' returns 0. All 84 tests pass, including the repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was `s.split(" ")`, which yields empty strings for leading, trailing and repeated spaces. `s.split()` fixes this for all whitespace, including tabs and newlines. The repro input now returns 4 and '' returns 0. All 84 tests pass. No existing tests were modified, and the new tests are in a separate file. `word_count` has no other callers. The source change is a single line.

Nit: the diff includes committed `__pycache__/*.pyc` files. Drop them and add `__pycache__/` to `.gitignore` before merging. This is hygiene only and doesn't affect behaviour.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
