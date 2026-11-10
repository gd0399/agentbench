# Fix #160: top_words returns one word too few

branch: `fix/issue-160`

Fixes #160

## Root cause
Off-by-one slice in report.top_words.

## Change
Changed ranked[:n - 1] to ranked[:n] in top_words. I added a repro test, and the full suite passes (83 tests).

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
