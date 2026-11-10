# Fix #103: median of odd-length list is wrong

branch: `fix/issue-103`

Fixes #103

## Root cause
The odd and even branches in median() were inverted. The check was `n % 2 == 0`, so even-length lists returned a single element and odd-length lists averaged two neighbours.

## Change
Swapped the parity branches in stats.median so odd-length lists return the middle element and even-length lists average the two middle elements. Added tests/test_issue_repro.py; the full suite passes (82 tests). I wrote the repro tests together with the fix and did not run them against the original code first.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: ? / ? / component `?`
Handoffs: single agent
Recovered errors: 0
</details>

_Opened automatically by agentbench._
