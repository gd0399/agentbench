# Fix #121: title_case lowercases the first word

branch: `fix/issue-121`

Fixes #121

## Root cause
The minor-word check in title_case ignored word position, so a leading "the" was lowercased.

## Change
title_case now capitalises the first word even if it is a minor word. I added a regression test, and the full suite passes.

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
