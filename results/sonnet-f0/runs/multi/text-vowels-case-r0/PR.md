# Fix #124: count_vowels ignores capital vowels

branch: `fix/issue-124`

Fixes #124

## Root cause
toolkit/text.py line 40, count_vowels: `sum(1 for c in s if c in "aeiou")` only matches lowercase vowels, so uppercase vowels are skipped ('Education' -> 4). Fix: use `c in "aeiouAEIOU"` or `c.lower() in "aeiou"`. There is no docstring or existing test for count_vowels that contradicts the case-insensitive behaviour.

## Change
count_vowels now counts uppercase vowels (checks against "aeiouAEIOU"). I added regression tests in tests/test_toolkit.py for 'Education' == 5, 'AEIOU' == 5 and '' == 0. The full suite passes (87 tests), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The one-line fix in `toolkit/text.py` is correct and minimal. `count_vowels` now matches "aeiouAEIOU", which fixes the root cause of the case-sensitivity bug. It does not just special-case the 'Education' input. `count_vowels` has no other callers, so nothing else is affected. The full suite passes (87 tests), and no existing tests were changed or removed.

Nits, not blocking:
- The diff includes committed `__pycache__/*.pyc` files. Please keep these out of the commit, and add `__pycache__/` to `.gitignore` if it isn't there already.
- The regression tests are duplicated between `tests/test_issue_repro.py` and `tests/test_toolkit.py`. One copy is enough.
- `c.lower() in "aeiou"` would be a slightly cleaner way to write the check.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
