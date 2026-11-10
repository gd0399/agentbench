# Fix #125: initials() are not capitalised

branch: `fix/issue-125`

Fixes #125

## Root cause
toolkit/text.py line 45, in initials(): `"".join(p[0] for p in parts)` takes the first character of each word as-is and never uppercases it. Fix: use `p[0].upper()`. No docstring, README entry or existing test covers initials(), so the requested behaviour doesn't conflict with anything.

## Change
initials() now uppercases the first character of each word (p[0].upper()). The full suite passes, including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The fix is correct and minimal. It is a one-line change in toolkit/text.py, `p[0].upper()` in initials(), and it addresses the root cause rather than the repro input. The full suite passes (84 tests), and the existing tests were not modified. The new tests/test_issue_repro.py is a sensible regression test.

Edge cases I checked: leading/trailing whitespace, hyphenated names, the empty string and accented characters all behave sensibly. The one oddity is that `'ß'.upper()` gives 'SS', so a name starting with ß yields two letters. That is a very rare case and not worth blocking on.

Before merging, drop the committed __pycache__/*.pyc files from the diff. They are build artifacts and shouldn't be in the patch. Adding `__pycache__/` to .gitignore would stop it happening again.

<details><summary>Agent trail</summary>

Triage: bug / low / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
