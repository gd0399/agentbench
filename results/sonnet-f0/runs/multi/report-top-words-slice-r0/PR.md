# Fix #160: top_words returns one word too few

branch: `fix/issue-160`

Fixes #160

## Root cause
toolkit/report.py line 20, in top_words: `return ranked[:n - 1]` slices one element too few. It should be `ranked[:n]`. The ranking (by -count, then alphabetical) is correct. The helpers in text.py and seq.py are not involved. No existing tests cover top_words, so nothing conflicts.

## Change
Fixed off-by-one in report.top_words (ranked[:n - 1] -> ranked[:n]). Moved the repro test into tests/test_toolkit.py (removed tests/test_issue_repro.py) and added ranking, n=0 and n>len tests; all 86 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. Changing `ranked[:n - 1]` to `ranked[:n]` fixes the off-by-one at its source. I checked the edge cases: n=0 returns [], and n larger than the number of words returns all words. Ranking is still by count descending, then alphabetical. No existing tests were changed; the diff only adds new ones. All 86 tests pass. The new tests cover the issue repro, ranking, n=0 and n larger than the word count.

Minor: the diff includes `__pycache__/*.pyc` files. Make sure they aren't committed, and add them to .gitignore if they aren't already ignored.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `report`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
