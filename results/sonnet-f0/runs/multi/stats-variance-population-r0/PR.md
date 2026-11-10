# Fix #106: sample variance uses the population formula

branch: `fix/issue-106`

Fixes #106

## Root cause
toolkit/stats.py, variance() lines 43-45: the `if sample:` branch returns `total / n`, identical to the population branch. It should return `total / (n - 1)`. The function already defaults to sample=True and already raises ValueError for n<2 when sample=True (line 37-38), so no extra edge-case handling is needed. The existing tests don't conflict: test_variance_population uses sample=False (expects 4), and test_variance_too_small expects ValueError for [1]. report.py doesn't call variance, so no callers are affected. The repro tests are in tests/test_issue_repro.py.

## Change
Fixed variance() in toolkit/stats.py so the sample branch divides by (n - 1) instead of n. The full suite passes (85 tests), including the repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The one-line change in `variance()` is the root cause: the sample branch divided by n, and it now divides by n-1. The population branch is unchanged. The two-value guard for sample variance was already in place.

I ran the full suite and 85 tests pass. The existing `test_variance_population` and `test_variance_too_small` are untouched, so no tests were tampered with. I also probed edge cases by hand:
- `variance([2,4,4,4,5,5,7,9])` returns 4.5714…, matching the issue.
- `variance([1,3])` returns 2.0 and `variance([1,3], sample=False)` returns 1.0.
- `variance([5], sample=False)` returns 0.0.
- `variance([1])` still raises `ValueError`.

Nothing else in the repo calls `variance`, so there are no other callers to break.

Non-blocking: the diff includes `__pycache__/*.pyc` files. They are test-run artifacts, so please leave them out of the commit. The repo has no `.gitignore`, so consider adding one. The new `tests/test_issue_repro.py` is fine, but you could fold those two tests into `test_toolkit.py`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
