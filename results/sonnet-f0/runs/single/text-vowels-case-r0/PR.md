# Fix #124: count_vowels ignores capital vowels

branch: `fix/issue-124`

Fixes #124

## Root cause
count_vowels only checked membership in lowercase "aeiou".

## Change
count_vowels now counts uppercase vowels; added a repro test and the full suite passes.

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
