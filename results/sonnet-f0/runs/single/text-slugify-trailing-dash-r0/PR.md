# Fix #115: slugify leaves a trailing dash

branch: `fix/issue-115`

Fixes #115

## Root cause
Punctuation at the string edges (after whitespace strip) was converted to '-' and never trimmed.

## Change
slugify now strips leading/trailing dashes after substitution; added repro test; all tests pass.

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
