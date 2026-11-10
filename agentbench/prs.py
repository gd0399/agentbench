"""Pull-request creation and live GitHub intake.

Benchmark runs open a *local* PR: the fix is committed on a `fix/issue-<n>` branch
and the PR title/body/diff are saved with the results. With a GitHubTarget and
`open_real_pr=True` the branch is pushed and a real PR is opened with `gh`.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .state import AgentState, Deps


@dataclass
class GitHubTarget:
    repo: str            # "owner/name"
    base: str = "main"
    remote: str = "origin"


def _gh(*args: str, cwd: str | Path | None = None) -> str:
    p = subprocess.run(["gh", *args], cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {p.stderr.strip()[:500]}")
    return p.stdout


def fetch_issue(repo: str, number: int) -> dict:
    data = json.loads(_gh("issue", "view", str(number), "-R", repo, "--json", "number,title,body,author,labels"))
    return {"number": data["number"], "title": data["title"], "body": data.get("body") or "",
            "author": (data.get("author") or {}).get("login", "user"),
            "labels": [l["name"] for l in data.get("labels", [])]}


def clone(repo: str, dest: Path) -> Path:
    _gh("repo", "clone", repo, str(dest), "--", "--depth", "50")
    return dest


def render_pr(state: AgentState) -> tuple[str, str]:
    issue, research, patch = state["issue"], state.get("research") or {}, state.get("patch") or {}
    review, triage = state.get("review") or {}, state.get("triage") or {}
    title = f"Fix #{issue['number']}: {issue['title']}"
    agents = " → ".join(h["dst"] for h in state.get("handoffs", [])) or "single agent"
    body = f"""Fixes #{issue['number']}

## Root cause
{research.get('root_cause', 'n/a')}

## Change
{patch.get('summary', 'n/a')}

## Verification
- Reproduction test: `{research.get('repro_test', 'n/a')}` — {'passes' if review.get('repro_passed') else 'not run'}
- Existing test-suite: {'passes' if review.get('tests_passed') else 'not run'}
- Review: {review.get('reviewer', 'n/a')} — {review.get('feedback', '')}

<details><summary>Agent trail</summary>

Triage: {triage.get('kind', '?')} / {triage.get('severity', '?')} / component `{triage.get('component', '?')}`
Handoffs: {agents}
Recovered errors: {len(state.get('errors', []))}
</details>

_Opened automatically by agentbench._
"""
    return title, body


def open_pr(deps: Deps, state: AgentState) -> dict:
    ws = deps.workspace
    n = state["issue"]["number"]
    branch = f"fix/issue-{n}"
    title, body = render_pr(state)
    diff = ws.diff()
    ws.git("checkout", "-q", "-B", branch)
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", f"{title}\n\nFixes #{n}")
    pr = {"title": title, "body": body, "branch": branch, "diff": diff, "url": ""}
    if deps.github is not None and deps.cfg.open_real_pr:
        t: GitHubTarget = deps.github
        ws.git("push", "-u", t.remote, branch)
        pr["url"] = _gh("pr", "create", "-R", t.repo, "--base", t.base, "--head", branch,
                        "--title", title, "--body", body, cwd=ws.root).strip()
    return pr
