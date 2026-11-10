# Fix #166: word_count treats hyphenated words as one

branch: `fix/issue-166`

Fixes #166

## Root cause
toolkit/text.py line 19-20: word_count is `len(s.split())`, which splits only on whitespace, so 'state-of-the-art design' gives 2. Fix: split on whitespace and hyphens, e.g. `len([w for w in re.split(r"[\s-]+", s) if w])`. The filter on empty strings keeps '' -> 0 and handles leading/trailing hyphens and standalone dashes (a standalone '-' would count 0). The existing tests (test_word_count: '  the quick  brown fox ' == 4, and the empty-string test) are still satisfied. The README and docstrings say nothing about hyphens, so there is no documented conflict. report.top_words also uses s.split(), but the issue doesn't mention it.

## Change
word_count now splits on whitespace and hyphens (filtering empty pieces), so 'state-of-the-art design' returns 5; empty string still 0. Full suite passes (85 passed), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The fix is in the right place: `word_count` now splits on `[\s-]+` and drops empty pieces. That is the actual cause, not a special case for the repro input. It is a one-line change. All 85 tests pass, and I did not see any edits to the existing tests.

I probed edge cases:
- 'well-known' gives 2.
- 'a--b' gives 2.
- 'foo-' gives 1.
- '' gives 0.
- '--' gives 0.
- 'a - b' gives 2. It was 3 before, so a standalone hyphen is no longer counted as a word. That seems right, but it is a small behaviour change.
- An en dash, as in 'a–b', still counts as 1. That is out of scope for this issue.

Non-blocking notes:
1. The diff includes `__pycache__/*.pyc` files. Please make sure they are not committed, and consider adding a `.gitignore`.
2. The new test sits in a separate `tests/test_issue_repro.py`. It would fit better in `tests/test_toolkit.py` next to the other `word_count` tests. A case for 'a - b' or a trailing hyphen would also be useful.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
