# Fix #158: summarize() max is wrong for unsorted input

branch: `fix/issue-158`

Fixes #158

## Root cause
toolkit/report.py line 10, in summarize(): `"max": values[-1]` returns the last element, not the maximum. It is only correct for sorted input. The fix is `max(values)`. The triage's suggestion to look in stats.py is not needed, because summarize doesn't delegate for max. Mean and median are correct. The existing test test_summarize uses sorted input, so it doesn't catch this. Repro test: tests/test_issue_repro.py.

## Change
In report.summarize(), replaced `values[-1]` with `max(values)` so max is correct for unsorted input. Full suite passes (84), including the repro test. Empty input still raises the same ValueError from stats.mean.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was that `summarize` assumed sorted input by using `values[-1]`. Replacing it with `max(values)` fixes that for any ordering. It isn't tailored to the issue's example input.

- The full suite passes (84 tests).
- I probed `[3,9,2]`, all-negative input, a single element and empty input. All give correct results, and empty input still raises the same `ValueError` from `stats.mean`.
- `stats.median` sorts a copy, so it doesn't mutate the input or depend on order.
- No other `[-1]` indexing exists in the repo, so there are no sibling instances of this bug.
- No existing tests were modified. The new regression test in `tests/test_issue_repro.py` is appropriate. You could fold it into `test_toolkit.py` to match the existing layout.

Nit: the diff includes committed `__pycache__/*.pyc` files. Please drop them and add `__pycache__/` to `.gitignore` before merging. They don't affect behaviour.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
