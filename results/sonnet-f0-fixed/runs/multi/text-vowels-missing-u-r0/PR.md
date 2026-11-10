# Fix #123: count_vowels misses some vowels

branch: `fix/issue-123`

Fixes #123

## Root cause
toolkit/text.py line 40, count_vowels: `sum(1 for c in s.lower() if c in "aeio")`. The vowel set string is missing "u" (it should be "aeiou"). The input is already lowercased, so the triage's case-sensitivity theory is wrong. 'Education' loses its 'u' and returns 4. 'u' alone returns 0. No existing tests or docs contradict the expected behaviour.

## Change
Fixed count_vowels in toolkit/text.py: the vowel set "aeio" was missing "u", so it is now "aeiou". Casing logic is unchanged. Added regression test test_count_vowels_includes_u to tests/test_toolkit.py, covering 'Education', 'u' and 'U'. Full suite: 86 passed, 0 failed, including both tests in tests/test_issue_repro.py.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → verifier → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
