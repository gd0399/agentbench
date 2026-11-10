# Fix #126: camel_to_snake adds a leading underscore

branch: `fix/issue-126`

Fixes #126

## Root cause
In toolkit/text.py, camel_to_snake (lines 48-54) adds "_" before every uppercase character, including the one at index 0. The loop enumerates i but never uses it. A leading capital such as 'Value' therefore becomes '_value'. The fix is to add the underscore only when i > 0. The existing test, 'parseHttpResponse', has no leading capital, so it doesn't conflict with the requested behaviour.

## Change
camel_to_snake now only inserts "_" before an uppercase char when i > 0, so 'Value' -> 'value'; 'parseHttpResponse' unchanged. Full suite passes (84), including the repro test.

## Verification
- Reproduction test: `tests/test_issue_repro.py` — passes
- Existing test-suite: passes
- Review: reviewer — Approved. The fix changes the condition to `c.isupper() and i > 0`. This addresses the root cause, which was an underscore being emitted before the first character. It is not special-cased to the 'Value' input. I ran the full suite and 84 tests pass. The existing test was not modified, and the new regression test is a reasonable addition. Probes:
- 'Value' -> 'value'.
- 'parseHttpResponse' -> 'parse_http_response' (unchanged).
- 'X' -> 'x', and '' -> ''.

Some behaviours are still odd but were already there and are outside this issue: 'HTTPResponse' -> 'h_t_t_p_response', and '_Value' -> '__value'. Open a separate issue if you want to handle them.

Please drop the committed `__pycache__/*.pyc` files before merging. They are build artifacts that came from running tests, and a `.gitignore` entry would keep them out. The real change is only `toolkit/text.py` and `tests/test_issue_repro.py`.

<details><summary>Agent trail</summary>

Triage: bug / medium / component `text`
Handoffs: researcher → coder → reviewer → open_pr
Recovered errors: 1
</details>

_Opened automatically by agentbench._
