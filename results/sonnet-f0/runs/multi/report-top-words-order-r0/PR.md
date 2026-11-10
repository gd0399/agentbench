# Fix #159: top_words returns the least common words

branch: `fix/issue-159`

Fixes #159

## Root cause
toolkit/report.py line 19 in top_words: `ranked = sorted(counts, key=lambda w: (counts[w], w))` sorts by count ascending, so ranked[:n] gives the least common words. It should sort by descending count with alphabetical tie-break, e.g. key=lambda w: (-counts[w], w). The existing test test_top_words_tie_alpha ('z y x' -> ['x','y']) still holds with that key. The helpers in text.py and stats.py are not involved.

## Change
Fix top_words in toolkit/report.py: sort key changed to (-counts[w], w) so the most common words come first, with an alphabetical tie-break. The full suite passes (84 tests), including the repro test and test_top_words_tie_alpha.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause was the ascending sort on count. Changing the key to (-counts[w], w) puts the most common words first and keeps the alphabetical tie-break. The one-line change is minimal. All 84 tests pass, including the existing test_top_words_tie_alpha. The new regression test matches the issue's repro, and no existing tests were modified.

Before merging, drop the committed __pycache__/*.pyc files from the diff. They are artifacts of running the tests, and the repo has no .gitignore. Adding a .gitignore for them would also be fine.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
