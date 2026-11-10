# Fix #123: count_vowels misses some vowels

branch: `fix/issue-123`

Fixes #123

## Root cause
toolkit/text.py line 40, count_vowels: the vowel set is "aeio", which is missing 'u'. The triage's case-sensitivity theory is wrong, because the function already calls s.lower(). 'Education' has 'u' as its only miss, so it returns 4. Fix: use "aeiou". The repro tests/test_issue_repro.py fails on current code, and 'rule' returns 1 instead of 2.

## Change
Fixed count_vowels in toolkit/text.py by changing the vowel set from "aeio" to "aeiou". It was missing 'u'. The full suite passes (85 tests), including the repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approving. The root cause is correct: the vowel set "aeio" was missing 'u', and the patch changes it to "aeiou". It is a one-line change in toolkit/text.py. 'Education' now returns 5, and the case-insensitive handling is unchanged. The full suite passes (85 tests), no existing tests were modified, and nothing else in the repo uses count_vowels. The new tests in tests/test_issue_repro.py cover the issue example plus 'rule' and 'UPSIDE', which is reasonable regression coverage.

Minor nit: the diff includes compiled __pycache__/*.pyc files. They are not in the repo file listing, so they are probably a side effect of the diff tooling. Make sure they aren't committed, and consider adding a .gitignore entry for __pycache__.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
