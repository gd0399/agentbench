# Fix #159: top_words returns the least common words

branch: `fix/issue-159`

Fixes #159

## Root cause
top_words sorted by ascending count, returning the least common words.

## Change
Sort by descending count (alphabetical tiebreak kept) in top_words.

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
