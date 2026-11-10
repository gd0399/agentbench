# Fix #122: title_case keeps stray capitals

branch: `fix/issue-122`

Fixes #122

## Root cause
title_case uppercased only the first letter of each word and left the remaining characters unchanged (w[:1].upper() + w[1:]), so stray capitals survived.

## Change
title_case now lowercases the rest of each word, so 'hELLO wORLD' gives 'Hello World'. I added a repro test, and the full suite passes (84 tests).

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
