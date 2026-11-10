# Fix #133: sliding_window misses the final window

branch: `fix/issue-133`

Fixes #133

## Root cause
toolkit/seq.py line 42, in sliding_window: the range bound is `range(len(items) - size)`, which is off by one. It should be `range(len(items) - size + 1)`. The last window is dropped. When size == len(items), the result is [] instead of one window. `stats.moving_average` uses the correct `+ 1` bound. No existing tests or docs contradict the expected behaviour.

## Change
Fix off-by-one in seq.sliding_window: range bound is now len(items) - size + 1, so the final window is included. All tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approving. The fix is correct and minimal. The range bound was off by one, and `len(items) - size + 1` is the right count of windows. I ran the full suite and 85 tests pass. I also checked edge cases: size == len gives one window, size > len gives [], an empty list gives [], and size 1 gives all singletons. Existing tests were not modified, and the new tests in tests/test_issue_repro.py cover the issue case and the size == len boundary.

One nit: the diff includes committed __pycache__/*.pyc files. They are build artifacts and shouldn't be in the patch. Drop them or add them to .gitignore before merging. The code change itself needs no further work.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
