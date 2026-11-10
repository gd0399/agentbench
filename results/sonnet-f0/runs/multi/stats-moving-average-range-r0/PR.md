# Fix #111: moving_average drops the last window

branch: `fix/issue-111`

Fixes #111

## Root cause
toolkit/stats.py line 65, in moving_average: `for i in range(len(values) - window)` is off by one. It should be `range(len(values) - window + 1)`. The last valid window starting at index len-window is never reached. [2,4,6],3 gives [] and [1,2,3,4],2 gives [1.5,2.5] with 3.5 missing. The existing tests only check the window<=0 ValueError, so there is no conflict.

## Change
Fixed the off-by-one in stats.moving_average (range(len(values) - window + 1)) so the last window is included. A window larger than the input still returns [] and window<=0 still raises ValueError. Added three regression tests to tests/test_toolkit.py. The full suite passes (87 passed), including the repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. `range(len(values) - window)` becomes `range(len(values) - window + 1)`, which is the root cause of the dropped last window.

I ran the suite: 87 passed. I also probed edge cases:
- `[2,4,6], 3` returns `[4.0]`.
- `[1,2], 3` returns `[]`.
- `[]` with window 1 returns `[]`.
- `[5]` with window 1 returns `[5.0]`.
- `[1,2,3,4], 2` returns `[1.5, 2.5, 3.5]`.
- The `window <= 0` ValueError is unchanged.

No existing tests were modified or weakened. The new tests were only added.

Before merging, please clean up two things:
- Drop the `__pycache__/*.pyc` files from the diff. They are build artifacts and should not be committed.
- Delete `tests/test_issue_repro.py`. Its two tests duplicate `test_moving_average_last_window_included` and `test_moving_average_all_windows`, which you already added to `tests/test_toolkit.py`.

Neither of these blocks the approval.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
