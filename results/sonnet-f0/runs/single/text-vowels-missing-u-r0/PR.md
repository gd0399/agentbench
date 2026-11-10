# Fix #123: count_vowels misses some vowels

branch: `fix/issue-123`

Fixes #123

## Root cause
count_vowels checked membership in "aeio", omitting 'u'.

## Change
Added the missing 'u' to the vowel set in count_vowels; added a repro test. All 84 tests pass.

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
