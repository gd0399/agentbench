# Fix #122: title_case keeps stray capitals

branch: `fix/issue-122`

Fixes #122

## Root cause
In title_case, non-minor words were built as w[:1].upper() + w[1:], which left the rest of the word's casing untouched.

## Change
title_case now lowercases the rest of each word, so 'hELLO wORLD' becomes 'Hello World'. I added a repro test in tests/test_issue_repro.py. The full suite passes (84 tests).

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
