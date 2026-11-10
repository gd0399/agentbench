# Fix #104: median() crashes with TypeError

branch: `fix/issue-104`

Fixes #104

## Root cause
toolkit/stats.py line 15 in median(): `mid = n / 2` uses true division, which gives a float. It is then used as a list index on line 17 (`ordered[mid]`) and on line 18 (`ordered[mid - 1]`, `ordered[mid]`), which raises TypeError. It should be `mid = n // 2`. Every non-empty input fails, odd or even length, not only the issue's [3, 1, 2]. Sorting is fine. The repro tests in tests/test_issue_repro.py cover odd and even lengths and both fail. The only existing median test checks that empty input raises ValueError, so nothing contradicts the expected behaviour.

## Change
Fix median(): use integer division (mid = n // 2) so list indices are ints. Repro and full suite pass (82 passed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and addresses the root cause. `mid = n / 2` produced a float, which can't be used as a list index. Changing it to `n // 2` fixes both the odd and even branches.

I ran the full suite and it passes (82 passed). I also checked these cases by hand:
- `[3,1,2]` returns 2.
- `[4,1,3,2]` returns 2.5.
- `[5]` returns 5.
- `[1,2]` returns 1.5.
- `[]` still raises ValueError.
- A tuple input works.

The new tests in `tests/test_issue_repro.py` cover the issue and the even-length case. No existing tests were changed.

One cleanup before merge: the diff includes many `__pycache__/*.pyc` files. These are build artifacts, so please drop them from the commit and consider adding `__pycache__/` to `.gitignore`. The source change is a one-line fix and is otherwise minimal.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
