# Fix #122: title_case keeps stray capitals

branch: `fix/issue-122`

Fixes #122

## Root cause
toolkit/text.py line 35, in title_case: `out.append(w[:1].upper() + w[1:])` uppercases the first letter but leaves the rest of the word unchanged, so 'hELLO' becomes 'HELLO'. The tail should be lowercased: `w[:1].upper() + w[1:].lower()`. Minor words (line 33) are already lowercased. Existing tests only use all-lowercase input, so they don't conflict with the fix. One possible side effect: acronyms such as 'NASA' would become 'Nasa'. The existing tests don't cover that case.

## Change
title_case now lowercases the tail of each non-minor word (`w[1:].lower()`), so 'hELLO wORLD' -> 'Hello World'. Added a regression test in tests/test_toolkit.py; all 85 tests pass. Side effect for reviewer: acronyms like 'NASA' now become 'Nasa' (no existing tests cover this; no special-casing added). Note that report.py's title formatting uses title_case, so it is affected too.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The one-line change in `title_case` (`w[1:].lower()`) fixes the root cause: non-minor words were never normalised past their first letter. It is minimal. All 85 tests pass, and no existing tests were changed. `report.py` only passes titles through `title_case`, so it gets the same corrected behaviour.

Before merging:
- Remove the committed `__pycache__/*.pyc` files from the diff, and add them to `.gitignore` if they aren't already ignored.
- `tests/test_issue_repro.py` duplicates the regression test already added to `tests/test_toolkit.py`. Delete the new file.

Behaviour change to note in the changelog: acronyms such as 'NASA' now become 'Nasa'. This follows directly from the issue's expected output, and it matches Python's `str.title`. Users who need acronyms preserved will need a separate option.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
