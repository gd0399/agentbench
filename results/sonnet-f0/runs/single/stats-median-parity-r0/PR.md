# Fix #103: median of odd-length list is wrong

branch: `fix/issue-103`

Fixes #103

## Root cause
The parity check in median() was inverted. For even n it returned ordered[mid], and for odd n it averaged the two neighbouring elements.

## Change
Swapped the odd/even branches in stats.median. Odd lengths now return the middle element and even lengths return the mean of the two middle elements. I added a repro test in tests/test_issue_repro.py, and the full suite passes.

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
