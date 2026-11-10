# Fix #111: moving_average drops the last window

branch: `fix/issue-111`

Fixes #111

## Root cause
toolkit/stats.py line 65 in moving_average: `for i in range(len(values) - window):` is off by one and omits the last window. It should be `range(len(values) - window + 1)`. For [2,4,6] with window 3 the range is 0 and the result is []. No existing test or doc contradicts the expected behaviour. The only existing test, test_moving_average_bad, checks window<=0 raising ValueError.

## Change
Fix off-by-one in stats.moving_average (range(len(values) - window + 1)) so the last window is included; window > len returns []. Added regression tests; full suite passes (86).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line change in `toolkit/stats.py` is right. `range(len(values) - window)` stopped one window short, and `range(len(values) - window + 1)` fixes that at the root. I checked the edge cases by reading the code, not by running them:
- `[2,4,6]` with window 3 gives `[4.0]`.
- Window equal to the length gives one window.
- Window larger than the length gives a negative range, so the result is `[]`, as before.
- Window <= 0 still raises `ValueError`.

The full suite passes (86). No existing tests were changed or weakened.

Nits, not blocking:
- `tests/test_issue_repro.py` and the new tests in `test_toolkit.py` cover the same cases. Keep one set, preferably the ones in `test_toolkit.py`.
- Drop the `__pycache__/*.pyc` files from the diff. They look like test-run artifacts, so they should be removed or gitignored.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
