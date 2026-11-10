# Fix #123: count_vowels misses some vowels

branch: `fix/issue-123`

Fixes #123

## Root cause
toolkit/text.py count_vowels used the vowel set "aeio", which has no 'u'. Input was already lowercased, so case was not the issue.

## Change
Added the missing 'u' to the vowel set in count_vowels. The repro tests and the full suite pass (85 passed).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → generalist → open_pr
Recovered errors: 2
</details>

_Opened automatically by agentbench._
