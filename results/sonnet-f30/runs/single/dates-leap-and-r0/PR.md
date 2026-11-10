# Fix #149: 2024 is not treated as a leap year

branch: `fix/issue-149`

Fixes #149

## Root cause
The leap-year condition was `year%4==0 and (year%100!=0 and year%400==0)`. That is only true for years divisible by 400. The correct rule is `year%100!=0 or year%400==0`.

## Change
Changed `and` to `or` in the century clause of is_leap_year. Added a repro test. The full suite passes.

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
