# Fix #111: moving_average drops the last window

branch: `fix/issue-111`

Fixes #111

## Root cause
toolkit/stats.py line 65, in moving_average: `for i in range(len(values) - window):` is off by one and omits the final window. It should be `range(len(values) - window + 1)`. For [2,4,6] with window 3 the range is empty, so the result is []. No existing test or docs contradict the fix; the only existing test covers window<=0 raising ValueError.

## Change
Fix off-by-one in moving_average: range(len(values) - window + 1) so the final window is included. All tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line change to `range(len(values) - window + 1)` fixes the root cause. The loop was missing the last window. I checked these cases:
- `[2,4,6]` with window 3 gives `[4.0]`.
- A window larger than the input returns `[]`.
- An empty input returns `[]`.
- Window 1 works.
- The existing tests still pass (84 passed).

The new regression tests are reasonable, and no existing tests were changed.

Before merging, drop the committed `__pycache__/*.pyc` files from the patch and add a `.gitignore` for them. They are build artifacts and shouldn't be in the diff. This is cleanup only and doesn't affect the fix.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
