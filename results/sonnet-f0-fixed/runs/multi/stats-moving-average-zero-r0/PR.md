# Fix #112: moving_average(window=0) raises ZeroDivisionError instead of ValueError

branch: `fix/issue-112`

Fixes #112

## Root cause
toolkit/stats.py line 62, moving_average: the guard is `if window < 0`, which lets window == 0 through (off-by-one boundary; should be `window <= 0`, matching the "window must be positive" message). With window=0 the loop runs and line 66 divides by window, raising ZeroDivisionError. No docs or tests conflict with the requested behaviour; existing tests only use window 2 and 3.

## Change
Changed moving_average guard in toolkit/stats.py from `window < 0` to `window <= 0` so window=0 raises ValueError. Added regression tests for zero and negative windows in tests/test_toolkit.py. Full suite: 86 passed, including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is the guard `window < 0`, which let 0 through to `/ window`. Changing it to `window <= 0` fixes that for every non-positive window, not only the repro input. The change is one line and the error message already said "must be positive". I ran the suite: 86 passed. No existing tests were modified or removed, and the new tests only add coverage for window=0 and window=-1.

Cleanup to do before merging:
- The diff includes many `__pycache__/*.pyc` files. They look like build artifacts, so drop them from the commit and add `__pycache__/` to `.gitignore`.
- `tests/test_issue_repro.py` duplicates `test_moving_average_zero_window` in `tests/test_toolkit.py`. Delete the repro file and keep the test in `test_toolkit.py`.

Neither item changes behaviour.

<details><summary>Agent trail</summary>

Triage: bug / low / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
