# Fix #166: word_count treats hyphenated words as one

branch: `fix/issue-166`

Fixes #166

## Root cause
toolkit/text.py line 19-20: word_count is `len(s.split())`, which splits only on whitespace, so 'state-of-the-art design' gives 2. Fix: split on hyphens too (e.g. `len(re.findall(r"[^\s-]+", s))` or `re.split(r"[\s-]+", s.strip())` with empty filtering). Existing tests (whitespace-only cases and empty string) don't conflict. No docs say hyphenated words count as one. Note that report.top_words uses its own s.split() and is separate. Standalone hyphens like ' - ' should not count as words.

## Change
word_count now splits on whitespace and hyphens (regex [^\s-]+), so 'state-of-the-art design' returns 5; standalone hyphens aren't counted. All tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. `word_count` now uses `re.findall(r"[^\s-]+", s)`, so hyphens act as separators like whitespace. That fixes the root cause rather than the one input in the issue. `re` was already imported.

I checked the behaviour by reading the code, not by running edge-case inputs:
- 'state-of-the-art design' gives 5.
- Standalone or doubled hyphens ('a - b', 'a--b') give 2 and are not counted as words.
- Empty strings and extra whitespace still give the old results.

All 85 tests pass, including the two existing word_count tests, and nothing existing was modified. The new regression test in tests/test_issue_repro.py is appropriate. You could move it into test_toolkit.py to match the repo layout.

Before merging, drop the committed `__pycache__/*.pyc` files from the diff and add them to .gitignore. They are build artifacts and shouldn't be in the patch.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
