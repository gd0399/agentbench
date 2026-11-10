# Fix #118: headline() is longer than the limit

branch: `fix/issue-118`

Fixes #118

## Root cause
truncate() sliced s[:limit] and then appended the suffix, so output length was limit+len(suffix).

## Change
text.truncate now keeps limit-len(suffix) characters before the suffix, so the result never exceeds limit. headline('the art of war', 12) returns 'The Art o...'. Added tests/test_issue_repro.py; full suite passes.

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
