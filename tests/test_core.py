import json
import shutil

import pytest

from agentbench.agents import offline
from agentbench.bench.report import mcnemar_exact, wilson
from agentbench.graph import build_multi_agent_graph, legal_moves, run_graph
from agentbench.llm import UsageMeter, price
from agentbench.state import Deps, FaultInjector, InjectedFailure, RunConfig
from agentbench.workspace import Workspace


def make_ws(tmp_path, tasks_dir, task):
    shutil.copytree(tasks_dir / task / "repo", tmp_path / "repo")
    ws = Workspace(tmp_path / "repo")
    ws.init_git()
    return ws


def test_workspace_sandbox(tmp_path, tasks_dir):
    ws = make_ws(tmp_path, tasks_dir, "stats-median-parity")
    with pytest.raises(ValueError):
        ws.read_file("../../etc/passwd")
    with pytest.raises(ValueError):
        ws.write_file(".git/config", "x")
    with pytest.raises(ValueError):
        ws.replace_in_file("toolkit/stats.py", "return", "yield")   # ambiguous match
    assert "TIMEOUT" in ws.run_python("while True: pass", timeout=1)


def test_reset_source_keeps_tests(tmp_path, tasks_dir):
    ws = make_ws(tmp_path, tasks_dir, "stats-median-parity")
    ws.write_file("tests/test_new.py", "def test_x(): pass\n")
    ws.replace_in_file("toolkit/stats.py", "if n % 2 == 0:", "if n % 2 == 1:")
    ws.write_file("toolkit/scratch.py", "x = 1\n")
    ws.reset_source()
    assert ws.changed_files() == ["tests/test_new.py"]


def test_parse_issue(tasks_dir):
    for task in ("stats-median-parity", "seq-chunk-last"):
        meta = json.loads((tasks_dir / task / "meta.json").read_text())
        expr, expected = offline.parse_issue(json.loads((tasks_dir / task / "issue.json").read_text()))
        assert (expr, expected) == (meta["expr"], meta["expected"])


def test_fault_injector_is_deterministic():
    seen = []
    for _ in range(2):
        f = FaultInjector(rate=0.5, seed=7)
        outcome = []
        for i in range(20):
            try:
                f.maybe_fail("t", "coder")
                outcome.append(0)
            except InjectedFailure:
                outcome.append(1)
        seen.append(outcome)
    assert seen[0] == seen[1] and 0 < sum(seen[0]) < 20


@pytest.mark.parametrize("dead,expected_fallback", [
    ("researcher", "coder"), ("coder", "generalist"), ("reviewer", "verifier")])
def test_fallback_routes(tmp_path, tasks_dir, dead, expected_fallback):
    """Kill one specialist permanently; the run must still finish via its fallback."""
    class KillOne(FaultInjector):
        def maybe_fail(self, task_id, agent):
            if agent == dead:
                raise InjectedFailure(f"{agent} is down")

    ws = make_ws(tmp_path, tasks_dir, "stats-median-parity")
    deps = Deps(workspace=ws, meter=UsageMeter(), faults=KillOne(), cfg=RunConfig(node_retries=1))
    issue = json.loads((tasks_dir / "stats-median-parity" / "issue.json").read_text())
    final, _ = run_graph(build_multi_agent_graph(), issue, "stats-median-parity", deps)
    path = [h["dst"] for h in final["handoffs"]]
    assert expected_fallback in path and final["status"] in ("pr_opened", "invalid", "escalated")
    assert final["errors"][0]["agent"] == dead and final["errors"][0]["recovered_by"] == expected_fallback
    assert deps.meter.retries >= 1


def test_legal_moves_terminal_logic():
    base = {"research": {"reproduced": True}, "coder_attempts": 3,
            "patch": {"attempt": 3, "key": "k"}, "review": {"approved": False, "attempt": 3},
            "rejected_patches": ["regression::a", "regression::b", "regression::k"]}
    assert legal_moves(base, 3)[0][0] == "close_invalid"
    assert legal_moves({**base, "rejected_patches": ["review::a"]}, 3)[0][0] == "escalate"
    assert legal_moves({**base, "review": {"approved": True, "attempt": 3}}, 3)[0][0] == "open_pr"
    assert legal_moves({"research": {"reproduced": False}, "handoffs": []}, 3)[0][0] == "close_not_reproducible"


def test_stats_helpers():
    lo, hi = wilson(30, 60)
    assert lo < 0.5 < hi and hi - lo < 0.3
    assert mcnemar_exact(0, 0) == 1.0
    assert mcnemar_exact(10, 0) < 0.01
    assert price("anthropic:claude-sonnet-5-5", 1_000_000, 0) == 2.0
