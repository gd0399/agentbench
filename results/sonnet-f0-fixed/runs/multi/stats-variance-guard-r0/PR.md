# Fix #107: variance() raises for perfectly valid input

branch: `fix/issue-107`

Fixes #107

## Root cause
toolkit/stats.py line 37, in variance(): the guard `if n < 2 or sample:` is wrong. It raises whenever sample=True (the default), whatever the length, so variance([1,2,3]) always raises. It should be `if sample and n < 2:`. The empty-input check on line 39 (`n == 0`) is unreachable because `n < 2` catches it first. With the intended guard, sample=False works for n>=1, and the empty case needs to be checked first or handled. Existing tests are consistent with the fix: test_variance_population uses sample=False, and test_variance_too_small expects variance([1]) to raise under the default sample=True. The issue's expected value is right: the sample variance of [1,2,3] is 1.0. Repro at tests/test_issue_repro.py. test_sample_variance_valid_input is the issue's own case. test_population_variance_single_value is an extra check I added, which also fails today.

## Change
Fixed variance() guard in toolkit/stats.py: empty input is checked first, and the "at least two values" error is raised only when `sample and n < 2` (it used to raise whenever sample=True). Added regression test test_variance_sample_default. All 86 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — I'd merge this. The root cause was the guard `if n < 2 or sample`, which raised for every sample=True call. The new guard is `sample and n < 2`, and the empty-input check now runs first. I ran these cases:
- variance([1,2,3]) returns 1.0.
- variance([5], sample=False) returns 0.0.
- The population variance case returns 4.0.
- [] raises the "empty" error with either sample setting.
- [1] with sample=True raises the "at least two values" error.

All 86 tests pass. The existing test_variance_too_small is unchanged, so no tests were weakened.

Nits, not blocking:
- The diff includes committed __pycache__/*.pyc files. Drop them from the commit and add them to .gitignore.
- tests/test_issue_repro.py duplicates the regression test the coder added to test_toolkit.py. Keep only one. The population single-value case in it is worth moving into test_toolkit.py.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
