# Fix #104: median() crashes with TypeError

branch: `fix/issue-104`

Fixes #104

## Root cause
toolkit/stats.py line 15 in median(): `mid = n / 2` uses true division and yields a float. That float is then used as a list index at line 17 (`ordered[mid]`) for odd n and at line 18 (`ordered[mid - 1]`, `ordered[mid]`) for even n. This raises TypeError for every non-empty input, not just odd lengths. The fix is `mid = n // 2`. Nothing in the docs or tests conflicts with the expected behaviour, since the only existing median test covers the empty case.

## Change
In toolkit/stats.py median(), changed `mid = n / 2` to `mid = n // 2` so the list index is an int. Odd and even branches now return correct values (median([3,1,2]) == 2, median([4,1,3,2]) == 2.5). The empty-input ValueError is unchanged. The full suite passes (82 passed), including both regression tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was `mid = n / 2`, which gives a float in Python 3 and so raises TypeError when used as a list index. Changing it to `n // 2` fixes that directly. It is a one-line change and not specific to the issue's input.

I ran the full suite: 82 passed. I also probed edge cases:
- single element: `median([5]) == 5`
- two elements: `median([1, 2]) == 1.5`
- tuple input: `median((3, 1, 2)) == 2`
- float input: `median([1.5, 2.5]) == 2.0`
- empty input still raises ValueError

The coder did not modify existing tests. They added `tests/test_issue_repro.py` with odd-length and even-length regression cases, which is appropriate.

Minor point: the diff includes `__pycache__/*.pyc` files. These are build artifacts and should not be committed. Make sure they are excluded or covered by .gitignore before merging. This does not affect the correctness of the fix.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
