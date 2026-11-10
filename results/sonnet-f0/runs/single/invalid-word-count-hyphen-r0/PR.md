# Fix #166: word_count treats hyphenated words as one

branch: `fix/issue-166`

Fixes #166

## Root cause
word_count used str.split(), which only splits on whitespace, so hyphenated words stayed together as one word.

## Change
word_count now splits on whitespace and hyphens, so 'state-of-the-art design' returns 5. Stray hyphens on their own are not counted as words. I added tests/test_issue_repro.py, and the full suite passes (86 tests).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: ? / ? / component `?`
Handoffs: single agent
Recovered errors: 0
</details>

_Opened automatically by agentbench._
