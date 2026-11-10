# Fix #119: word_count counts extra words with repeated spaces

branch: `fix/issue-119`

Fixes #119

## Root cause
word_count used s.split(" "), which yields empty strings for consecutive, leading and trailing spaces.

## Change
word_count now uses s.split() so runs of whitespace and leading/trailing spaces are ignored. Added a repro test; the full suite passes.

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
