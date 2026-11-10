# Fix #107: variance() raises for perfectly valid input

branch: `fix/issue-107`

Fixes #107

## Root cause
toolkit/stats.py line 37 in variance(): the guard `if n < 2 or sample:` should be `if sample and n < 2:`. Because of the `or sample`, every call with the default sample=True raises ValueError, even for valid input like [1,2,3]. Also, with sample=False and n<2 (including n==0) it raises the wrong "sample variance" message, and the later `n == 0` check is unreachable. The intended logic is: n==0 -> "empty sequence" error; sample and n<2 -> error; otherwise compute. The existing tests (population variance, variance([1]) raising) are consistent with the fix and don't conflict.

## Change
Fixed variance() guard in toolkit/stats.py: empty input raises first ("empty sequence"), then sample and n<2 raises, otherwise computes. variance([1,2,3]) now returns 1.0; all 84 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the inverted guard `if n < 2 or sample: raise`. It made every sample=True call raise, and it made the empty check unreachable. The new guard is `n == 0` first, then `sample and n < 2`. That is correct and minimal.

Checks I ran:
- variance([1,2,3]) returns 1.0.
- variance([1,2,3,4], sample=False) returns 1.25, and variance([5], sample=False) returns 0.0.
- variance([5]) raises "needs at least two values". variance([]) raises "empty sequence" for both sample modes.
- All 84 tests pass. The existing tests are untouched, and the regression test is new and sensible.

Nit: the diff includes committed __pycache__/*.pyc files. Please drop them and add them to .gitignore before merging. They are not part of the fix.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
