# Fix #126: camel_to_snake adds a leading underscore

branch: `fix/issue-126`

Fixes #126

## Root cause
The function added "_" before every uppercase character, including the one at index 0.

## Change
camel_to_snake no longer prefixes an underscore when the first character is uppercase.

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
