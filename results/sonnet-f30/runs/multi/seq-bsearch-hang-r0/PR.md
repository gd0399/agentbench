# Fix #136: binary_search hangs forever on a missing value

branch: `fix/issue-136`

Fixes #136

## Root cause
toolkit/seq.py binary_search, line 53: when items[mid] < target it sets `lo = mid` instead of `lo = mid + 1`. For [1,3,5] searching 4: lo=0,hi=2 → mid=1 (3<4) → lo=1; then mid=(1+2)//2=1 again, so lo stays 1 and the loop `while lo <= hi` never terminates. Fix: `lo = mid + 1`. The docstring ("Index of target in sorted items, or -1") agrees with the expected -1, so no conflict with the docs or tests.

## Change
Fix binary_search infinite loop: use `lo = mid + 1` when items[mid] < target (hi branch was already `mid - 1`). Full suite passes (68), and present values, empty list and missing values behave correctly.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / high / component `seq`
Handoffs: researcher → coder → reviewer → verifier → open_pr
Recovered errors: 2
</details>

_Opened automatically by agentbench._
