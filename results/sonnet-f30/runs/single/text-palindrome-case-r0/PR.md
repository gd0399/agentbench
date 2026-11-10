# Fix #120: is_palindrome is case-sensitive

branch: `fix/issue-120`

Fixes #120

## Root cause
is_palindrome compared characters without normalising case.

## Change
is_palindrome now lowercases the alphanumeric characters before comparing, so 'Racecar' returns True. I added tests/test_issue_repro.py, and the full suite passes (84 tests). I wrote the repro test and the fix together and ran the tests once afterwards, so I never saw the repro fail on the old code.

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
