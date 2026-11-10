# Fix #124: count_vowels ignores capital vowels

branch: `fix/issue-124`

Fixes #124

## Root cause
The vowel check only matched lowercase "aeiou".

## Change
count_vowels now counts uppercase vowels too.

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
