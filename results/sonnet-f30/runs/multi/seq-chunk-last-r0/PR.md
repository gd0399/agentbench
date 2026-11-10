# Fix #127: pages() undercounts when the last page has one item

branch: `fix/issue-127`

Fixes #127

## Root cause
The bug is in toolkit/seq.py, line 7, in chunk(). It uses range(0, len(items) - 1, size), and the "- 1" is an off-by-one error. When the final chunk would hold exactly one item, the start index len(items)-1 is excluded from the range, so that item is dropped. For example, chunk([0..4], 2) returns [[0,1],[2,3]] instead of [[0,1],[2,3],[4]]. report.pages() (toolkit/report.py:34) is len(seq.chunk(items, per_page)), so it inherits the undercount. The fix is to use range(0, len(items), size). The existing test test_chunk_exact only covers exact multiples, so it doesn't catch this. The expected behaviour doesn't conflict with any docs or tests. Repro tests are in tests/test_issue_repro.py.

## Change
Fixed off-by-one in seq.chunk(): range(0, len(items) - 1, size) -> range(0, len(items), size), so a trailing single-item chunk is kept; report.pages() now returns 3 for 5 items/2 per page. Full suite passes (84); empty input and oversize chunk still behave sensibly.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was in seq.chunk(): `range(0, len(items) - 1, size)` dropped a trailing single-item chunk. The patch changes it to `range(0, len(items), size)`, which is the correct fix. It is not specific to the issue's input.

- The full suite passes (84 tests), and the existing tests were not modified.
- Edge cases I probed all behave correctly: `[]` gives `[]`, `[1]` with size 3 gives `[[1]]`, and `[1,2,3]` with size 3 gives one chunk. `[1,2,3,4]` with size 3 gives `[[1,2,3],[4]]`. `report.pages([], 2)` gives 0, and `report.pages(range(5), 2)` gives 3.
- `report.pages` is the only caller of chunk in the library code, and it is fixed by this change.
- The new regression test file covers both pages() and chunk().

Minor nit: the diff includes `__pycache__/*.pyc` files. Drop them before merging and add `__pycache__/` to `.gitignore`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
