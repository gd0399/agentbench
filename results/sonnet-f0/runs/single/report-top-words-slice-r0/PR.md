# Fix #160: top_words returns one word too few

branch: `fix/issue-160`

Fixes #160

## Root cause
Off-by-one slice in top_words dropped the last requested word.

## Change
Changed the slice in top_words from ranked[:n - 1] to ranked[:n]. Added a repro test. The full suite passes.

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
