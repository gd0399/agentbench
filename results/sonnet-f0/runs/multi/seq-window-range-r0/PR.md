# Fix #133: sliding_window misses the final window

branch: `fix/issue-133`

Fixes #133

## Root cause
toolkit/seq.py line 42, sliding_window: off-by-one in range bound. It uses range(len(items) - size) but should be range(len(items) - size + 1). This drops the last window; when len(items) == size it returns [] instead of one window. stats.moving_average uses the correct +1 bound. There is no existing test or doc for sliding_window, so nothing conflicts. The repro tests are in tests/test_issue_repro.py.

## Change
Fixed off-by-one in seq.sliding_window (range(len(items) - size + 1)), so the final window is included. size > len returns [] and size <= 0 still raises ValueError. Moved the repro tests into tests/test_toolkit.py, added too-large and bad-size cases, and deleted tests/test_issue_repro.py. All 87 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The fix changes `range(len(items) - size)` to `range(len(items) - size + 1)`, which is the root cause (an off-by-one) and a one-line change.

- The full suite passes (87 tests).
- Edge cases behave correctly: an exact-size window returns one window, size > len returns [], an empty list returns [], size 1 works, and strings work.
- size <= 0 still raises ValueError.
- No existing tests were modified or weakened. The coder only added new tests. The deleted tests/test_issue_repro.py was the coder's own scratch file, and it isn't in the repo now.

Nit: the diff includes committed `__pycache__/*.pyc` files. Please drop them from the commit and add a `.gitignore` for them. This doesn't block merging.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
