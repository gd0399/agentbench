# Fix #130: dedupe() does not remove duplicates

branch: `fix/issue-130`

Fixes #130

## Root cause
toolkit/seq.py dedupe() (lines 20-27): the `seen` set is never updated. There is no `seen.add(x)` after `out.append(x)` in the loop, so every element passes the `x not in seen` check and the input is returned unchanged. The fix is to add `seen.add(x)` inside the if-block. The docstring ("Remove duplicates, preserving first-seen order") agrees with the issue, so there is no conflict with docs or tests.

## Change
Fixed seq.dedupe(): added the missing `seen.add(x)` so duplicates are skipped and first-seen order is kept. Added regression tests (issue case, empty list, no duplicates). Full suite: 87 passed, including tests/test_issue_repro.py.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line fix is correct. `seen` was never populated in `dedupe`, so nothing was ever filtered. Adding `seen.add(x)` fixes that root cause and keeps first-seen order. I ran the full suite (87 passed). `dedupe([3,1,3,2,1])` now returns `[3,1,2]`, and a string input behaves sensibly. Unhashable items such as lists still raise TypeError, but that was already the case and is outside this issue.

Nits to clean up before merge, none of which block approval:
- The diff includes committed `__pycache__/*.pyc` files. Drop them from the patch and add `__pycache__/` to `.gitignore` if it isn't there already.
- `tests/test_issue_repro.py` duplicates `test_dedupe_removes_duplicates_preserving_order` from `tests/test_toolkit.py`. Keep one copy.

No existing tests were modified or removed.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
