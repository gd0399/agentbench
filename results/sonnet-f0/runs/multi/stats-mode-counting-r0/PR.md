# Fix #105: mode() always returns the first element

branch: `fix/issue-105`

Fixes #105

## Root cause
toolkit/stats.py line 27 in mode(): `counts[v] = counts.get(v, 1)` never increments the count, so every value has count 1 and the first element always wins. It should be `counts.get(v, 0) + 1`. The tie-break loop (strict `>`, starting from values[0]) is correct and matches the existing test test_mode_tie_first.

## Change
Fix mode() counting in toolkit/stats.py: `counts.get(v, 0) + 1` so counts actually increment. Tie-break loop unchanged. Full suite passes (85), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix addresses the root cause. The counting line `counts.get(v, 1)` never incremented, so every count stayed at 1 and mode() always returned values[0]. `counts.get(v, 0) + 1` is the correct one-line change. The tie-break loop uses a strict `>`, so ties still resolve to the first occurrence. `[5,3,3,5]` returns 5, which the existing test in tests/test_toolkit.py also covers. The full suite passes (85), no existing tests were modified, and the new tests in tests/test_issue_repro.py are reasonable regression tests.

Nit, not blocking: the diff includes many committed `__pycache__/*.pyc` files. Please drop them from the commit and add `__pycache__/` to .gitignore if it isn't there already. The source change itself is minimal and correct.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
