# Fix #105: mode() always returns the first element

branch: `fix/issue-105`

Fixes #105

## Root cause
toolkit/stats.py line 27 in mode(): `counts[v] = counts.get(v, 1)` never increments the count, so every value has count 1 and the selection loop never finds a count greater than that of values[0]. As a result the first element is always returned. It should be `counts.get(v, 0) + 1`. The existing tie-break test (mode([5,3,3,5]) == 5) stays consistent with the fix, since the loop uses a strict `>` comparison.

## Change
Fix mode() counting in toolkit/stats.py: counts[v] = counts.get(v, 0) + 1 (was never incrementing). Strict > keeps first-seen tie-breaking; all 85 tests pass, including the repro.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was `counts.get(v, 1)`, which never incremented the count, so every value stayed at 1 and the first element always won. `counts.get(v, 0) + 1` fixes that at the source. It is a one-line change in `mode()` and doesn't special-case the repro input.

I ran the suite and all 85 tests pass. `[1,2,2,3]` now gives 2. The strict `>` comparison keeps first-occurrence tie-breaking, and the existing `[5,3,3,5] -> 5` test still passes. No existing tests were modified. The new `tests/test_issue_repro.py` only adds coverage for the issue case and the tie case.

Minor: the diff includes `__pycache__/*.pyc` files, which are test-run artifacts. Please make sure they aren't committed, and consider adding a `.gitignore`. The repo has none. This doesn't block the merge.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
