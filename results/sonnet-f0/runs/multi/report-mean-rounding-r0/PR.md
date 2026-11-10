# Fix #157: summarize() rounds the mean to an integer

branch: `fix/issue-157`

Fixes #157

## Root cause
toolkit/report.py line 8, in summarize(): `"mean": round(stats.mean(values))` wraps the mean in round() with no ndigits, so 2.5 becomes 2 (banker's rounding). stats.mean (toolkit/stats.py:7) is correct (sum/len, true division). Fix: drop the round() and use stats.mean(values). No existing tests or docstrings cover summarize, so there is no conflict.

## Change
Removed the round() around stats.mean(values) in report.summarize so the mean is no longer rounded to an integer. The repro test and the full suite pass (83 tests).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the `round()` in `report.summarize`. `stats.mean` already returns the true mean, and its existing tests pass. Removing the `round()` is the minimal fix. It doesn't special-case the input from the issue. `summarize` has no other callers, so nothing else depends on the rounded value. The full suite passes (83 tests). The new regression test in `tests/test_issue_repro.py` is reasonable, and no existing tests were changed. Before merging, drop the `__pycache__/*.pyc` files from the diff and add `__pycache__/` to `.gitignore` if it isn't already there. They are build artifacts and don't belong in the patch.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
