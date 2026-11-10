# Fix #157: summarize() rounds the mean to an integer

branch: `fix/issue-157`

Fixes #157

## Root cause
toolkit/report.py line 8, in summarize(): `"mean": round(stats.mean(values))` wraps the mean in round() with no ndigits, which rounds to an int (2.5 -> 2 via banker's rounding). stats.mean (toolkit/stats.py:4-7) is correct, returns sum/len = 2.5, and is tested. The fix is to drop the round() call: `"mean": stats.mean(values)`. No existing tests cover summarize, and nothing documents the rounding.

## Change
Removed the round() call around stats.mean(values) in report.summarize so the mean is no longer rounded to an int. The full suite passes (83 tests), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is the `round()` call in `report.summarize`. `stats.mean` already returns the correct float, and the patch removes only that call. Nothing else in the repo uses `summarize`. `stats.mean` is untouched and its existing tests still pass. The new regression test matches the issue's repro. The full suite passes (83 tests), and no existing tests were modified.

Before merging, drop the `__pycache__/*.pyc` files from the diff. They are build artifacts from running the tests, and a `.gitignore` entry would prevent this. They don't affect behaviour.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
