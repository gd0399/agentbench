# Fix #120: is_palindrome is case-sensitive

branch: `fix/issue-120`

Fixes #120

## Root cause
is_palindrome compared characters without case normalization.

## Change
is_palindrome now lowercases alphanumeric characters before comparing. 'Racecar' returns True. Added a repro test; the full suite passes.

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
