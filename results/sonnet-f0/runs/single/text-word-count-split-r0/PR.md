# Fix #119: word_count counts extra words with repeated spaces

branch: `fix/issue-119`

Fixes #119

## Root cause
word_count used s.split(" "), which yields empty strings for consecutive, leading and trailing spaces. Those empty strings were counted as words.

## Change
word_count now uses s.split() so runs of whitespace and leading/trailing spaces are ignored. I added tests/test_issue_repro.py. I did not run it against the unfixed code, so I never saw it fail first. The full suite passes (83 tests).

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
