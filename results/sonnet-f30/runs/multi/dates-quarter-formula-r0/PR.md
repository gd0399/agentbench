# Fix #153: March is reported as Q2

branch: `fix/issue-153`

Fixes #153

## Root cause
toolkit/dates.py line 21, in quarter_of: `return month // 3 + 1` is off by one for months 3, 6, 9 and 12. Those return 2, 3, 4 and 5, so December gives an invalid Q5. The correct formula is `(month - 1) // 3 + 1`. The repro at tests/test_issue_repro.py covers all 12 months, and 4 of the 12 fail (months 3, 6, 9, 12). quarter_of has no existing tests and no docs that contradict the expected behaviour.

## Change
Fixed off-by-one in dates.quarter_of: now `(month - 1) // 3 + 1`, so March→Q1, June→Q2, Sept→Q3, Dec→Q4. The repro test (all 12 months) passes and the full suite passes (95 passed). quarter_of already raises ValueError for months outside 1..12, so I left that unchanged. The repro test stays in tests/test_issue_repro.py as the regression test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / medium / component `dates`
Handoffs: researcher → coder → reviewer → verifier → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
