# Fix #112: moving_average(window=0) raises ZeroDivisionError instead of ValueError

branch: `fix/issue-112`

Fixes #112

## Root cause
toolkit/stats.py line 62, moving_average(): the guard is `if window < 0`, so window == 0 passes validation. The loop then computes `/ window` with window=0 (line 66) and raises ZeroDivisionError. The error message says "window must be positive", so the guard should be `window <= 0`. No existing tests or docs conflict: tests only use windows 2 and 3.

## Change
Changed moving_average guard from `window < 0` to `window <= 0` so window=0 raises ValueError instead of ZeroDivisionError. Full suite passes (84), including the repro.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The guard in `moving_average` was `window < 0`, so 0 got past it and hit `/ window`. Changing it to `window <= 0` fixes that cause directly. It is not special-cased to the repro input. All 84 tests pass, and the existing tests were not changed. The new regression test in tests/test_issue_repro.py is reasonable. Valid windows behave as before, and a window larger than the sequence still returns [].

Nit: the diff includes committed __pycache__/*.pyc files. Drop them before merging, and consider adding a .gitignore. They don't affect behaviour.

<details><summary>Agent trail</summary>

Triage: bug / low / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
