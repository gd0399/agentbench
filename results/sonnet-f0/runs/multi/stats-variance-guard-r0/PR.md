# Fix #107: variance() raises for perfectly valid input

branch: `fix/issue-107`

Fixes #107

## Root cause
toolkit/stats.py line 37, in variance(): the guard `if n < 2 or sample:` is wrong. With the default sample=True it always raises "sample variance needs at least two values", whatever the input length. The triage guess of an off-by-one length check is not accurate. The `or sample` is a logic bug. The guard should be `if sample and n < 2:`. Also, the `n == 0` check below it is unreachable for the population case. Population variance of an empty list currently raises the wrong message, and population variance of a single value currently raises, although it should return 0. The existing tests pass: test_variance_population uses sample=False, and test_variance_too_small uses [1] with the default sample=True, which still raises after the fix. A suggested fix is to check n == 0 first, then `if sample and n < 2`. No conflict with the docs or tests.

## Change
Fixed variance() guard in toolkit/stats.py: check empty input first, then raise only `if sample and n < 2` (previously `n < 2 or sample` always raised for sample=True). Added tests for population variance of a single value and empty input; full suite passes (87).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approving. The root cause was the guard `n < 2 or sample`, which always raised for sample=True. The patch changes it to `sample and n < 2` and moves the empty check first. That is the correct fix and it is minimal.

I checked these cases:
- variance([1,2,3]) returns 1.0.
- variance([1,2,3], sample=False) returns 0.667.
- variance([5], sample=False) returns 0.0.
- variance([5]) still raises the "at least two values" error.
- variance([]) raises the "empty" error for both sample settings.

All 87 tests pass. The existing tests were not changed. The new tests in tests/test_issue_repro.py are reasonable and cover the issue plus the edge cases.

Nit: the diff includes committed __pycache__/*.pyc files. Drop them from the commit and add them to .gitignore. This doesn't affect behaviour.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
