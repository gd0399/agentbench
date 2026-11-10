# Fix #126: camel_to_snake adds a leading underscore

branch: `fix/issue-126`

Fixes #126

## Root cause
camel_to_snake prepended "_" to every uppercase character, including the first one.

## Change
camel_to_snake now only inserts an underscore before an uppercase letter that isn't the first character. I added tests/test_issue_repro.py and the full suite passes.

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
