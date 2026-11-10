# Fix #147: format_currency has no thousands separator

branch: `fix/issue-147`

Fixes #147

## Root cause
toolkit/money.py line 27, in format_currency: f"{sign}{symbol}{abs(amount):.2f}" uses the ".2f" format spec without the "," grouping option, so no thousands separators are inserted. Changing it to {abs(amount):,.2f} fixes it. The sign handling is already separate, so negatives give '-$1,234.50'. The existing test test_format_currency_negative (-5 -> '-$5.00') is unaffected, and nothing documented contradicts the request.

## Change
Added the ',' grouping option to the format spec in format_currency, so 1234.5 gives '$1,234.50'. Negative amounts keep their sign handling. The full suite passes (85 tests), including the repro tests.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The fix is a one-character change in format_currency, from `:.2f` to `:,.2f`. It addresses the root cause, because the format spec was missing the grouping option. It isn't special-cased to the issue's input. I ran the full suite and all 85 tests pass. The existing negative test `-5 -> '-$5.00'` is unchanged, and no existing tests were edited. The new tests in tests/test_issue_repro.py are additive and reasonable.

I also probed these inputs by hand:
- 1234.5 gives `$1,234.50`.
- -1234567.891 gives `-$1,234,567.89`.
- 0 gives `$0.00`.
- 999.999 gives `$1,000.00`.
- 1e15 groups correctly.

One quirk remains: -0.001 gives `-$0.00`. This behaviour was already there and is outside this issue.

Before merging, drop the `__pycache__/*.pyc` files from the diff. They are build artifacts and should not be committed. Consider adding `__pycache__/` to .gitignore. The source change itself is fine.

<details><summary>Agent trail</summary>

Triage: bug / low / component `money`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
