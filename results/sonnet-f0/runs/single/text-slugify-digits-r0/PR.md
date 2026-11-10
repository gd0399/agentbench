# Fix #116: slugify strips numbers

branch: `fix/issue-116`

Fixes #116

## Root cause
slugify used re.sub(r"[^a-z]+", "-", ...), which treated digits as separators and removed them.

## Change
Changed the slugify regex to keep digits. I added a repro test, and the full suite passes (84 tests).

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
