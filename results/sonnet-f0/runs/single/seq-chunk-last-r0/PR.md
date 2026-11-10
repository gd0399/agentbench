# Fix #127: pages() undercounts when the last page has one item

branch: `fix/issue-127`

Fixes #127

## Root cause
seq.chunk used range(0, len(items) - 1, size), which skipped the last chunk when it held a single element.

## Change
Fixed an off-by-one in seq.chunk. The range stop was len(items) - 1, so a final one-item chunk was dropped. It is now len(items). pages() uses chunk, so report.pages(list(range(5)), 2) now returns 3. I added regression tests, and the full suite passes (84 tests).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: ? / ? / component `?`
Handoffs: single agent
Recovered errors: 0
</details>

_Opened automatically by agentbench._
