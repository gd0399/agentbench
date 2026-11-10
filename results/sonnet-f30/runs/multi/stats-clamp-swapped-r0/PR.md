# Fix #113: clamp() returns the lower bound for in-range values

branch: `fix/issue-113`

Fixes #113

## Root cause
toolkit/stats.py line 73, clamp(): `return min(lo, max(x, hi))` has min and max swapped. max(x, hi) is always >= hi, and min(lo, ...) is then always lo (since lo <= hi), so it always returns lo. For example, clamp(15, 0, 10) also returns 0, not 10. The fix is `return max(lo, min(x, hi))`. The existing tests only cover x below lo, equal bounds and lo > hi, so none of them caught this. The requested behaviour does not conflict with any tests or docs.

## Change
Fixed swapped min/max in stats.clamp (toolkit/stats.py): now `max(lo, min(x, hi))`. The ValueError for lo > hi and the equal-bounds behaviour are unchanged. Kept tests/test_issue_repro.py as regression tests (in-range, below, above). Full suite: 84 passed, 0 failed.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The fix corrects the swapped min/max in clamp(), which was the root cause: `max(lo, min(x, hi))` is the standard form. I checked in-range, below, above, both boundaries, equal bounds and floats, and all gave the expected values. The `lo > hi` ValueError is unchanged. The full suite passes (84 tests), and the existing tests in test_toolkit.py were not modified. The new regression tests in test_issue_repro.py cover the reported case. Nit: the diff includes committed __pycache__/*.pyc files. Drop them or add them to .gitignore before merging. They are build artifacts and do not affect the fix.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
