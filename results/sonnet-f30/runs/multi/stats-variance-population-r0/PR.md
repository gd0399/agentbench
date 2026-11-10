# Fix #106: sample variance uses the population formula

branch: `fix/issue-106`

Fixes #106

## Root cause
toolkit/stats.py, variance(), lines 43-45: the `if sample:` branch returns `total / n` — identical to the population branch. It should return `total / (n - 1)`. The population path (sample=False) is correct and tested by test_variance_population; the guards (n<2) are fine.

## Change
Fixed variance() sample branch in toolkit/stats.py to divide by (n - 1) instead of n. Full suite passes (84), including the repro and test_variance_population. No other callers of variance exist (no stdev in repo), so the only behavior change is that sample variance (the default) now returns the correct, larger value.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — The change is correct and minimal. The sample branch of variance() now divides by (n - 1). That is the root cause, and the population branch is unchanged. The n < 2 guard runs before the division, so there is no divide-by-zero. I ran the suite and all 84 tests pass. I searched for callers: report.py doesn't use variance, so nothing else is affected. The existing test_variance_population is untouched, and the new regression test (tests/test_issue_repro.py) checks the exact value from the issue, 4.5714.... No existing tests were modified.

Nit: the diff includes committed __pycache__/*.pyc files. Please drop them from the patch and add __pycache__/ to .gitignore if it isn't there already. This is only hygiene and doesn't block the merge.

<details><summary>Agent trail</summary>

Triage: bug / high / component `stats`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
