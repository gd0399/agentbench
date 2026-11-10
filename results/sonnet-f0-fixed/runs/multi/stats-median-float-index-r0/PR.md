# Fix #104: median() crashes with TypeError

branch: `fix/issue-104`

Fixes #104

## Root cause
toolkit/stats.py line 15 in median(): `mid = n / 2` uses true division and yields a float (e.g. 1.5). It is then used as a list index at line 17 (`ordered[mid]`) and line 18 (`ordered[mid - 1]`, `ordered[mid]`), which raises TypeError. It should be `mid = n // 2`. For odd n, ordered[n//2] is the median. For even n, the existing formula with the integer mid is correct. No test or doc conflicts with the expected behaviour. The existing 80 tests pass, and the new repro test fails.

## Change
Fix median(): use integer division (`mid = n // 2`) so the index is an int, which fixes the TypeError. I also added an even-length test, median([4,1,3,2]) == 2.5, to tests/test_issue_repro.py. All 82 tests pass: the 80 existing ones plus the repro test and the new even-length test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. The root cause was `mid = n / 2`, which gives a float, and a float can't be used as a list index. Changing it to `n // 2` fixes that for both odd and even lengths. I ran median on [3,1,2], [4,1,3,2], [5], [1,2] and a tuple, and all gave the expected results. All 82 tests pass. No existing tests were modified. The two new tests are a reasonable regression test for the issue, and the even-length one is a useful extra.

Nit: the diff includes compiled `__pycache__/*.pyc` files. These look like by-products of running the tests, and the repo has no .gitignore. Please drop them from the commit and consider adding a .gitignore. This doesn't change my approval.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
