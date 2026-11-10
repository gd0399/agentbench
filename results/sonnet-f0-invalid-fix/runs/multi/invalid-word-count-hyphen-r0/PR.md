# Fix #166: word_count treats hyphenated words as one

branch: `fix/issue-166`

Fixes #166

## Root cause
toolkit/text.py line 19-20: word_count is `len(s.split())`, which splits only on whitespace, so 'state-of-the-art design' gives 2. Hyphens are not treated as separators. A fix would split on whitespace and hyphens, e.g. `len([w for w in re.split(r"[\s-]+", s) if w])`. Empty tokens must be filtered so the existing tests still pass: '' -> 0 and '  the quick  brown fox ' -> 4. The issue does not contradict existing tests or docs. word_count has no docstring, and no test covers hyphens. Repro test is tests/test_issue_repro.py, which fails with 2 != 5; the other 84 tests pass. top_words in report.py also uses s.split() but is not part of this issue.

## Change
word_count now splits on whitespace and hyphens, drops empty tokens, and has a docstring. Added edge-case tests (leading/trailing hyphen, 'a--b', lone '-') to tests/test_issue_repro.py. All 88 tests pass.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and it addresses the root cause. word_count now splits on `[\s-]+` and drops empty tokens, so 'state-of-the-art design' gives 5. Leading and trailing hyphens, 'a--b' and a lone '-' (or a spaced ' - ') are all handled without inflating the count. Existing behaviour is unchanged: the original whitespace and empty-string tests still pass, and the full suite is 88/88. No existing tests were edited. The new tests only add edge cases in a new file. word_count has no other callers in the repo.

Nit: the diff includes __pycache__/*.pyc files. They look like test-run artifacts, and you should leave them out of the commit or add them to .gitignore. This doesn't block the merge.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
