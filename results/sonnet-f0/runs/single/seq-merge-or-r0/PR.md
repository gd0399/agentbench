# Fix #138: merge_sorted raises IndexError

branch: `fix/issue-138`

Fixes #138

## Root cause
The loop ran while either list had items left, so it indexed past the end of the shorter list.

## Change
Changed the merge loop condition from `or` to `and` in merge_sorted. The leftover tails are already appended by the extend calls after the loop.

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
