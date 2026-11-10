# Fix #109: percentile(…, 100) raises ValueError

branch: `fix/issue-109`

Fixes #109

## Root cause
toolkit/stats.py line 52 in percentile(): the bounds check `if p < 0 or p >= 100` is off by one and rejects p == 100, although the docstring says p is in [0, 100]. It should be `p > 100`. The rank formula on line 57 gives ceil(100*n/100) = n for p=100, so it returns the max element. The existing test (p=101 raises) still passes after the fix.

## Change
Fixed off-by-one in percentile() bounds check (p >= 100 -> p > 100) so p=100 returns the max element; full suite passes (84 tests).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The docstring says p is in [0, 100], and the old check `p >= 100` rejected the valid upper bound. The rank formula already gives ordered[n-1] at p=100, so no other change was needed.

I ran the full suite and 84 tests pass. I also probed edge cases:
- p=0, 1, 50, 99, 100 and 100.0 all return the expected values.
- p=100.5 and p=-1 still raise ValueError.
- A single-element list works at p=100.
- The existing out-of-range test (p=101) still passes.

No existing tests were modified. The coder added a regression test, tests/test_issue_repro.py.

Nit, not a blocker: the diff includes committed __pycache__/*.pyc files. Drop them from the commit and add them to .gitignore. You could also move the new test into tests/test_toolkit.py next to the other percentile tests.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
