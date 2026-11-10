# Fix #145: compound_interest ignores periods_per_year

branch: `fix/issue-145`

Fixes #145

## Root cause
compound_interest divided the rate by periods_per_year but used only `years` as the exponent.

## Change
Exponent now years * periods_per_year; added repro test; full suite passes.

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
