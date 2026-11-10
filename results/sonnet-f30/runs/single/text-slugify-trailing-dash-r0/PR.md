# Fix #115: slugify leaves a trailing dash

branch: `fix/issue-115`

Fixes #115

## Root cause
Trailing punctuation was converted to "-" after the whitespace strip, leaving a dash at the ends.

## Change
slugify now strips leading/trailing dashes after substitution.

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
