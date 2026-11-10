# Fix #137: merge_sorted drops trailing items

branch: `fix/issue-137`

Fixes #137

## Root cause
toolkit/seq.py merge_sorted (lines 59-70): after the main merge loop, only the leftover of `a` is appended (`out.extend(a[i:])` at line 69). The leftover of `b` (`b[j:]`) is never appended, so when `b` has remaining items, such as 7 and 8 in the issue example, they are dropped. The fix is to also add `out.extend(b[j:])`.

## Change
merge_sorted now also appends the leftover of b (out.extend(b[j:])) after the merge loop, so trailing items are no longer dropped. All 84 tests pass, including the repro.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The bug was in the merge loop. It copied the leftover of `a` but never the leftover of `b`. The one-line `out.extend(b[j:])` fixes that root cause and is minimal. It isn't tailored to the issue's input. I checked the issue repro, an empty `a`, an empty `b`, duplicates, and trailing items from `a`. All gave correct results. The full suite passes (84 tests). The existing tests were not modified. The new tests in tests/test_issue_repro.py cover trailing items from both `a` and `b`. Minor: the diff includes `__pycache__/*.pyc` files. Those are test-run artifacts and should not be committed. Please drop them before merging, or add a .gitignore.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 2
</details>

_Opened automatically by agentbench._
