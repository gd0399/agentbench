# Fix #108: percentile() rounds the rank down instead of up

branch: `fix/issue-108`

Fixes #108

## Root cause
toolkit/stats.py line 57 in percentile(): `rank = p * len(ordered) // 100` uses floor division, so the nearest-rank rank is floored instead of ceil'd. For p=30, n=5: 150//100 = 1 -> ordered[0] = 15; it should be ceil(1.5) = 2 -> ordered[1] = 20. Fix: use ceiling, e.g. `rank = math.ceil(p * len(ordered) / 100)` or `-(-p * len(ordered) // 100)` (avoid float issues for integer p). Existing tests (p=0, 40, 100, bounds) remain compatible, since they hit exact integer ranks.

## Change
percentile() now computes the nearest-rank rank with ceiling division instead of floor division, so percentile([15,20,35,40,50], 30) returns 20. The full suite passes (84 tests), including the reproduction test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The change fixes the root cause. Nearest-rank percentile is ceil(p*n/100), and the old code used floor. The new ceiling division gives that rank. I checked it on [15,20,35,40,50]:

| p | result |
|---|---|
| 0 | 15 |
| 1 | 15 |
| 20 | 15 |
| 25 | 20 |
| 30 | 20 |
| 40 | 20 |
| 50 | 35 |
| 99 | 50 |
| 100 | 50 |
| 101 | ValueError (unchanged) |

A single-element list and a float p (25.5) also work. All 84 tests pass. No existing tests were changed. The new test only adds a regression test for the issue.

Minor nits, none blocking:
- `max(int(rank), 1)` is redundant, because p > 0 already gives rank >= 1 after the ceiling.
- The diff contains committed `__pycache__/*.pyc` files. Please make sure they are not included in the merge, or add them to `.gitignore`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
