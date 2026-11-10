"""Exercise the LLM code path (tool loop, bind_tools, metering, model fallback,
reviewer guardrail) with a scripted chat model, so it is tested without an API key."""
import json
import shutil
from pathlib import Path

import pytest
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from agentbench.graph import build_multi_agent_graph, build_single_agent_graph, run_graph
from agentbench.llm import ModelChain, UsageMeter
from agentbench.state import Deps, RunConfig
from agentbench.workspace import Workspace

TASK = "stats-median-parity"
FIX = ("if n % 2 == 0:", "if n % 2 == 1:")
REPRO = "from toolkit import stats\n\ndef test_issue_repro():\n    assert stats.median([3, 1, 2]) == 2\n"


def call(name, args, i=0):
    return {"name": name, "args": args, "id": f"c{i}", "type": "tool_call"}


SCRIPTS = {
    "RESEARCHER": [
        [call("write_file", {"path": "tests/test_issue_repro.py", "content": REPRO})],
        [call("run_tests", {"target": "tests/test_issue_repro.py"})],
        [call("submit_research", {"reproduced": True, "suspected_files": ["toolkit/stats.py"],
                                  "root_cause": "parity check inverted in median()"})],
    ],
    "CODER": [
        [call("replace_in_file", {"path": "toolkit/stats.py", "old": FIX[0], "new": FIX[1]})],
        [call("submit_patch", {"summary": "fix inverted parity check"})],
    ],
    "REVIEWER": [[call("submit_review", {"approved": True, "feedback": "LGTM"})]],
    "SUPERVISOR": [[call("submit_triage", {"kind": "bug", "severity": "medium", "component": "stats",
                                           "summary": "median parity"})]],
    "software engineer": [
        [call("write_file", {"path": "tests/test_issue_repro.py", "content": REPRO})],
        [call("replace_in_file", {"path": "toolkit/stats.py", "old": FIX[0], "new": FIX[1]})],
        [call("submit_resolution", {"status": "fixed", "summary": "fixed parity", "root_cause": "inverted check",
                                    "suspected_files": ["toolkit/stats.py"]})],
    ],
}


class ScriptedModel(BaseChatModel):
    fail: bool = False
    approve: bool = True

    @property
    def _llm_type(self):
        return "scripted"

    def bind_tools(self, tools, **kw):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kw):
        if self.fail:
            raise RuntimeError("503 overloaded")
        system = messages[0].content
        role = next(k for k in SCRIPTS if k in system)
        step = sum(1 for m in messages if isinstance(m, AIMessage))
        script = SCRIPTS[role]
        calls = script[min(step, len(script) - 1)]
        if role == "REVIEWER" and not self.approve:
            calls = [call("submit_review", {"approved": False, "feedback": "nope"})]
        msg = AIMessage(content="", tool_calls=calls,
                        usage_metadata={"input_tokens": 1000, "output_tokens": 100, "total_tokens": 1100})
        return ChatResult(generations=[ChatGeneration(message=msg)])


@pytest.fixture
def ws(tmp_path, tasks_dir):
    shutil.copytree(tasks_dir / TASK / "repo", tmp_path / "repo")
    w = Workspace(tmp_path / "repo")
    w.init_git()
    return w


def chain(primary_fails=False, approve=True):
    def factory(spec):
        return ScriptedModel(fail=primary_fails and "sonnet" in spec, approve=approve)
    return ModelChain("anthropic:claude-sonnet-5-5", ["anthropic:claude-haiku-5-5"], retries=1, backoff=0.01,
                      factory=factory)


def issue(tasks_dir):
    return json.loads((tasks_dir / TASK / "issue.json").read_text())


def test_multi_agent_llm_path(ws, tasks_dir):
    deps = Deps(workspace=ws, meter=UsageMeter(), backend="llm", model=chain())
    final, _ = run_graph(build_multi_agent_graph(), issue(tasks_dir), TASK, deps)
    assert final["status"] == "pr_opened"
    assert [h["dst"] for h in final["handoffs"]] == ["researcher", "coder", "reviewer", "open_pr"]
    assert "Fixes #" in final["pr"]["body"] and FIX[1] in final["pr"]["diff"]
    t = deps.meter.totals()
    assert t["llm_calls"] == 7 and t["input_tokens"] == 7000
    assert t["cost_usd"] == pytest.approx(7 * (1000 * 2 + 100 * 10) / 1e6)


def test_model_fallback_chain(ws, tasks_dir):
    deps = Deps(workspace=ws, meter=UsageMeter(), backend="llm", model=chain(primary_fails=True))
    final, _ = run_graph(build_multi_agent_graph(), issue(tasks_dir), TASK, deps)
    assert final["status"] == "pr_opened"
    t = deps.meter.totals()
    assert t["model_fallbacks"] == t["llm_calls"] > 0
    assert t["cost_usd"] == pytest.approx(t["llm_calls"] * (1000 * 0.10 + 100 * 0.50) / 1e6)  # billed at Haiku


def test_reviewer_rejection_loops_then_escalates(ws, tasks_dir):
    deps = Deps(workspace=ws, meter=UsageMeter(), backend="llm", model=chain(approve=False),
                cfg=RunConfig(max_coder_attempts=2))
    final, _ = run_graph(build_multi_agent_graph(), issue(tasks_dir), TASK, deps)
    assert final["status"] == "escalated"
    assert [h["dst"] for h in final["handoffs"]].count("coder") == 2


def test_single_agent_llm_path(ws, tasks_dir):
    deps = Deps(workspace=ws, meter=UsageMeter(), backend="llm", model=chain())
    final, _ = run_graph(build_single_agent_graph(), issue(tasks_dir), TASK, deps)
    assert final["status"] == "pr_opened"
    assert deps.meter.totals()["by_agent"]["single"]["calls"] == 3


def test_budget_cap_escalates(ws, tasks_dir):
    deps = Deps(workspace=ws, meter=UsageMeter(budget_usd=0.002), backend="llm", model=chain())
    final, _ = run_graph(build_multi_agent_graph(), issue(tasks_dir), TASK, deps)
    assert final["status"] == "escalated"
    assert any("budget" in e["error"] for e in final["errors"])
