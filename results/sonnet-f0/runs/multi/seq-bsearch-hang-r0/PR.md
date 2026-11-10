# Fix #136: binary_search hangs forever on a missing value

branch: `fix/issue-136`

Fixes #136

## Root cause
toolkit/seq.py line 53, in binary_search: when items[mid] < target the code does `lo = mid` instead of `lo = mid + 1`. With [1,3,5] and target 4, lo=1, hi=2 gives mid=1, items[1]=3<4, so lo stays 1 and the loop never ends (lo<=hi forever). The else branch (`hi = mid - 1`) is correct. Fix: `lo = mid + 1`. Does not conflict with docs or tests; the docstring says it returns the index or -1.

## Change
Fixed binary_search in toolkit/seq.py by changing `lo = mid` to `lo = mid + 1`, which stops the infinite loop when the target is missing. I added regression tests to tests/test_toolkit.py for [1,3,5] with targets 4, 0, 6, 5, 1 and 3, plus an empty-list case. The full suite passes (75 tests, including tests/test_issue_repro.py).

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The root cause is `lo = mid` failing to advance the lower bound. Changing it to `lo = mid + 1` is the standard one-line fix, and it is minimal.

Checks I ran:
- The full suite passes (75 tests).
- I compared `binary_search` against `list.index` for every target, including out-of-range ones, on sorted lists of length 0–7. All results matched.
- The new parametrized tests in `tests/test_toolkit.py` cover missing, present, boundary and empty cases. No existing tests were modified.

Optional nits, not blocking:
- `tests/test_issue_repro.py` duplicates the coverage in `test_toolkit.py`. It does use a subprocess with a timeout, which is a reasonable way to catch a hang, so keep it or fold it in as you prefer.
- The diff includes `__pycache__/*.pyc` files. These look like build artifacts and should not be committed. Drop them from the commit or add them to `.gitignore`.

<details><summary>Agent trail</summary>

Triage: bug / high / component `seq`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 0
</details>

_Opened automatically by agentbench._
