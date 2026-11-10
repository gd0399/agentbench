# Fix #118: headline() is longer than the limit

branch: `fix/issue-118`

Fixes #118

## Root cause
truncate sliced s[:limit] and then appended the suffix, so the output was limit + len(suffix) characters long.

## Change
text.truncate now cuts to limit - len(suffix) chars before appending the suffix, so the result never exceeds limit. headline('the art of war', 12) now returns 'The Art o...'.

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
