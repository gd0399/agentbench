# Fix #131: rotate() rotates left, docs say right

branch: `fix/issue-131`

Fixes #131

## Root cause
toolkit/seq.py line 36 in rotate(): `return items[k:] + items[:k]` performs a left rotation, but the docstring says "Rotate right by k positions". The correct right rotation is `items[-k:] + items[:-k]` (k is already reduced mod len, and k == 0 needs care, since items[-0:] is the whole list, which gives the wrong result for the +items[:-0] part). A safe form is `items[len(items)-k:] + items[:len(items)-k]`. Existing tests only cover k=0 and empty input, so they don't conflict with the fix.

## Change
Fixed rotate() in toolkit/seq.py to rotate right by k (n = len - k; items[n:] + items[:n]), which is safe for k == 0. The full suite passes (83 tests), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: verifier — all checks pass

<details><summary>Agent trail</summary>

Triage: bug / high / component `seq`
Handoffs: researcher → coder → reviewer → verifier → verifier → open_pr
Recovered errors: 3
</details>

_Opened automatically by agentbench._
