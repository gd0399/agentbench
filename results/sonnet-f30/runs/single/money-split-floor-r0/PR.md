# Fix #142: split_bill loses cents

branch: `fix/issue-142`

Fixes #142

## Root cause
split_bill used // (floor division) instead of /, dropping the fractional cents before rounding.

## Change
Changed floor division to true division in split_bill; added repro test; full suite passes.

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
