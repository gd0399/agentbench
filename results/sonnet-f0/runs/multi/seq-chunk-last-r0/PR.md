# Fix #127: pages() undercounts when the last page has one item

branch: `fix/issue-127`

Fixes #127

## Root cause
The bug is in toolkit/seq.py line 7, in `chunk`, not in `report.pages`. `report.pages` (report.py:34) returns `len(seq.chunk(items, per_page))`, which is fine. `chunk` uses `range(0, len(items) - 1, size)`, and the `- 1` is an off-by-one. When the last chunk holds a single item, its start index is `len(items) - 1`, which is excluded from the range, so that item is dropped. For example, `chunk([0,1,2,3,4], 2)` returns `[[0,1],[2,3]]` and is missing `[4]`. The fix is `range(0, len(items), size)`. The triage guess of floor division in `pages` is wrong. Changing `pages` to use ceiling division would hide the bug and leave `chunk` still dropping items. Existing tests only cover `chunk` with an exact multiple, so none of them conflict with the fix. The repro tests in tests/test_issue_repro.py fail on the current code: `test_pages_partial_last_page` and `test_chunk_keeps_single_item_last_chunk`.

## Change
Fixed off-by-one in seq.chunk (range(0, len(items) - 1, size) -> range(0, len(items), size)), which dropped a single-item last chunk and made report.pages undercount. Added a regression test for empty, exact-multiple and single-item cases. All 85 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is in seq.chunk, where range(0, len(items) - 1, size) skips the last item whenever it would start its own chunk. Changing it to range(0, len(items), size) fixes that. report.pages is correct and just calls chunk, so it didn't need changes. chunk is only used by report.pages and the tests. I ran the full suite and all 85 tests pass. The new tests cover the issue case, an empty list, an exact multiple, and a single item, and the existing tests are unchanged. One nit: the diff includes committed __pycache__/*.pyc files. Please drop them and add them to .gitignore before merging. They are build artifacts, not part of the fix.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
