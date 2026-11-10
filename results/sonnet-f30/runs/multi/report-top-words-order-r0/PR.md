# Fix #159: top_words returns the least common words

branch: `fix/issue-159`

Fixes #159

## Root cause
toolkit/report.py line 19 in top_words: `sorted(counts, key=lambda w: (counts[w], w))` sorts by count ascending, so ranked[:n] returns the least common words. It should sort by count descending and keep alphabetical tie-break, e.g. key=lambda w: (-counts[w], w). The existing test test_top_words_tie_alpha ('z y x' -> ['x','y']) requires alphabetical tie-breaking, so don't use reverse=True, which would break it. text.py and stats.py are not involved.

## Change
Fix top_words sort key to (-counts[w], w) so it sorts by count descending with an alphabetical tie-break. All 85 tests pass, including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the sort key `(counts[w], w)`, which sorts ascending by count. Changing it to `(-counts[w], w)` gives count descending with an alphabetical tie-break. That fixes the general ordering, not just the repro input. The existing tie-break test (`test_top_words_tie_alpha`) still passes, and all 85 tests pass. The change is one line, and no existing tests were modified. The new tests in `tests/test_issue_repro.py` are reasonable. One of them duplicates the existing tie-break test, which is harmless.

Before merging, drop the `__pycache__/*.pyc` binaries from the diff. They are test-run artifacts, not part of the fix. Adding a `.gitignore` entry for `__pycache__` would stop this happening again. The code change itself is fine.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
