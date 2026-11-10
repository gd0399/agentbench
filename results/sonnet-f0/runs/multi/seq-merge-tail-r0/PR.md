# Fix #137: merge_sorted drops trailing items

branch: `fix/issue-137`

Fixes #137

## Root cause
toolkit/seq.py, merge_sorted (line 69): after the merge loop only `out.extend(a[i:])` is called. The leftover tail of `b` (`b[j:]`) is never appended, so when `b` has remaining items after `a` is exhausted they are dropped. Fix: also add `out.extend(b[j:])`. No docs or tests contradict this.

## Change
Fixed merge_sorted in toolkit/seq.py. It now also appends the leftover tail of b (out.extend(b[j:])) after the merge loop. The full suite passes (84 tests), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line fix is correct. The merge loop stops when either input runs out, and the old code only appended the leftover tail of `a`. Adding `out.extend(b[j:])` fixes the root cause. I ran the full suite and 84 tests pass. I also checked these cases, and all give the expected output:
- the issue repro
- an empty `a`
- an empty `b`
- duplicate values across the inputs
- tuple inputs

The new tests in `tests/test_issue_repro.py` cover both the longer-`a` and longer-`b` cases. No existing tests were changed.

Before merging, drop the `__pycache__/*.pyc` files from the commit. They are build artifacts and not part of the fix. Adding `__pycache__/` to `.gitignore` would stop this recurring.

<details><summary>Agent trail</summary>

Triage: bug / high / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
