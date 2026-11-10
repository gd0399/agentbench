# Fix #139: last_n(items, 0) returns everything

branch: `fix/issue-139`

Fixes #139

## Root cause
toolkit/seq.py last_n (lines 74-77): the guard is `if n < 0: return []`, so n == 0 falls through to `items[-n:]`. That is `items[-0:]`, which equals `items[0:]`, so the whole list comes back. The guard should be `n <= 0`. The existing test only covers n=2, and nothing documents n=0 behaviour, so the expected `[]` doesn't contradict any test.

## Change
Fix last_n guard to `n <= 0` so n=0 returns [] instead of items[-0:] (the whole list). Full suite passes, including the repro.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is that `-0` equals `0`, so `items[-0:]` is `items[0:]`, which is the whole list. Changing the guard to `n <= 0` fixes that. It is a one-token change in `toolkit/seq.py`, and it keeps the existing behaviour of returning [] for negative n. The full suite passes (84 tests), and the existing tests are unmodified. The new regression test in `tests/test_issue_repro.py` covers the reported case. n=0 is the only value affected, since `items[-n:]` is correct for every n >= 1.

Nits, not blocking:
- The diff contains `__pycache__/*.pyc` files. They are test-run artifacts and shouldn't be committed. Drop them before merging, and consider adding a `.gitignore`.
- The new test could be folded into `test_last_n` in `tests/test_toolkit.py`, and could also assert n larger than len(items) and a negative n.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
