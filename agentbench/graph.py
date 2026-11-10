"""LangGraph wiring: supervisor + specialists (multi-agent) and the single-agent baseline.

Multi-agent topology (every specialist hands control back to the supervisor):

          ┌────────────── supervisor ───────────────┐
          │   (triage, routing, fallback policy)    │
   researcher   coder   reviewer   generalist*   verifier*
          └──── open_pr | close_not_reproducible | close_invalid | escalate ──> END

   * fallbacks: coder -> generalist, reviewer -> verifier (deterministic),
     researcher -> coder works from the raw issue, generalist -> escalate to a human.

Handoffs use `Command(goto=..., update=...)`; each one is logged in state["handoffs"].
"""
from __future__ import annotations

import time
from typing import Callable

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from pydantic import BaseModel, Field

from .agents import offline
from .agents.base import compact, finish_tool, issue_text, run_tool_loop
from .agents.specialists import coder, researcher, reviewer, solve_alone, verifier
from .llm import BudgetExceeded
from .prs import open_pr
from .state import AgentState, Deps, deps_of

SPECIALISTS = ("researcher", "coder", "reviewer", "generalist")
FALLBACK_FOR = {"researcher": "coder", "coder": "generalist", "reviewer": "verifier", "generalist": "escalate"}
TERMINALS = ("open_pr", "close_not_reproducible", "close_invalid", "escalate")


# --------------------------------------------------------------------------- resilience

def resilient(name: str, fn: Callable[[AgentState, Deps], dict], goto: str = "supervisor"):
    """Wrap an agent: inject faults, retry crashes, and on final failure report to the supervisor
    (which picks the fallback) instead of letting the exception kill the run."""

    def node(state: AgentState, config) -> Command:
        deps = deps_of(config)
        last = ""
        for attempt in range(deps.cfg.node_retries + 1):
            try:
                deps.faults.maybe_fail(state["task_id"], name)
                update = fn(state, deps)
                return Command(goto=goto, update={**update, "trace": [f"{name}: ok"]})
            except BudgetExceeded as e:
                return Command(goto="escalate", update={
                    "errors": [{"agent": name, "error": str(e), "attempt": attempt, "recovered_by": "escalate"}],
                    "resolution": f"budget exceeded in {name}"})
            except Exception as e:  # crash, model outage, step limit, malformed output, injected failure
                last = f"{type(e).__name__}: {e}"[:300]
                if attempt < deps.cfg.node_retries:
                    deps.meter.retries += 1
                    continue
        if name in ("coder", "generalist", "single"):
            deps.workspace.reset_source()       # don't let a half-applied edit leak into the fallback
        fb = FALLBACK_FOR.get(name, "escalate")
        return Command(goto=goto if goto == "supervisor" else "escalate", update={
            "failed_agents": [name],
            "errors": [{"agent": name, "error": last, "attempt": deps.cfg.node_retries + 1, "recovered_by": fb}],
            "trace": [f"{name}: FAILED -> {fb}"]})

    node.__name__ = name
    return node


# --------------------------------------------------------------------------- supervisor

def legal_moves(state: AgentState, max_attempts: int) -> list[tuple[str, str]]:
    """Valid next steps given the state; the first entry is the rule-based default."""
    failed = set(state.get("failed_agents", []))
    research = state.get("research")
    patch, review = state.get("patch"), state.get("review")
    attempts = state.get("coder_attempts", 0)

    res = state.get("resolution")
    if res and "generalist" in [h["dst"] for h in state.get("handoffs", [])] and res in (
            "fixed", "not_reproducible", "invalid", "give_up"):
        return [{"fixed": ("open_pr", "generalist fixed the issue and checks pass"),
                 "not_reproducible": ("close_not_reproducible", "generalist could not reproduce"),
                 "invalid": ("close_invalid", "generalist found the report contradicts intended behaviour"),
                 "give_up": ("escalate", "generalist could not fix it")}[res]]

    if research is None:
        if "researcher" in failed:
            worker = "generalist" if "coder" in failed else "coder"
            return [(worker, "researcher unavailable: work directly from the issue")]
        return [("researcher", "reproduce the issue and localise the root cause")]

    if not research.get("reproduced"):
        moves = [("close_not_reproducible", "reproduction passes on main")]
        n_research = sum(h["dst"] == "researcher" for h in state.get("handoffs", []))
        if n_research < 2 and "researcher" not in failed:
            moves.append(("researcher", "retry reproduction with a different approach"))
        return moves

    if research.get("conflicts_with_tests") and patch is None:
        return [("close_invalid", "researcher: requested behaviour contradicts documented/tested behaviour"),
                ("coder", "attempt a fix anyway"), ("escalate", "ask a human")]

    worker = "generalist" if "coder" in failed else "coder"
    if worker == "generalist" and "generalist" in failed:
        return [("escalate", "coder and generalist both failed")]

    needs_code = patch is None or (review is not None and not review.get("approved")
                                   and review.get("attempt") == patch.get("attempt"))
    if patch and patch.get("gave_up"):
        rejected = state.get("rejected_patches", [])
        if research.get("conflicts_with_tests") or (rejected and all(r.startswith("regression") for r in rejected)):
            return [("close_invalid", "every fix contradicts existing tested behaviour"),
                    ("escalate", "coder gave up")]
        return [("escalate", "coder gave up")]
    if needs_code:
        if attempts >= max_attempts:
            rejected = state.get("rejected_patches", [])
            if rejected and all(r.startswith("regression") for r in rejected):
                return [("close_invalid", f"all {attempts} fixes contradict existing tested behaviour"),
                        ("escalate", f"{attempts} patches rejected")]
            return [("escalate", f"{attempts} patches rejected")]
        why = "write a fix" if patch is None else f"address review feedback: {review.get('feedback', '')[:300]}"
        return [(worker, why), ("escalate", "stop and hand to a human")]
    if review is None or review.get("attempt") != patch.get("attempt"):
        return [("verifier" if "reviewer" in failed else "reviewer", "review the patch")]
    if review.get("approved"):
        return [("open_pr", "patch approved")]
    return [("escalate", "unexpected state")]


class Route(BaseModel):
    next: str = Field(description="One of the allowed next steps")
    reason: str
    instructions: str = Field(default="", description="Concrete guidance for the next agent")


class TriageOut(BaseModel):
    kind: str = Field(description="bug | feature | question")
    severity: str = Field(description="low | medium | high")
    component: str = Field(description="Module most likely affected, e.g. 'stats'")
    summary: str


SUPERVISOR_SYSTEM = """You are the SUPERVISOR of a maintenance team (researcher, coder, reviewer). You never edit
code. You decide who works next and give them precise instructions. Choose ONLY from the allowed moves.
Prefer the default unless the state clearly justifies another move."""


def supervisor(state: AgentState, config) -> Command:
    deps = deps_of(config)
    step = state.get("step", 0) + 1
    update: dict = {"step": step}
    src = state["trace"][-1].split(":")[0] if state.get("trace") else "start"

    if "triage" not in state:
        tri = None
        if deps.backend == "llm":
            try:
                deps.faults.maybe_fail(state["task_id"], "supervisor")
                tri = run_tool_loop(deps, "supervisor", SUPERVISOR_SYSTEM + "\nFirst, triage this issue.",
                                    issue_text(state["issue"]) + "\n\nFiles:\n" + "\n".join(deps.workspace.list_files()),
                                    [], finish_tool(TriageOut, "submit_triage", "Record triage."), 3)
            except BudgetExceeded:
                raise
            except Exception as e:
                update["errors"] = [{"agent": "supervisor", "error": str(e)[:300], "attempt": 1,
                                     "recovered_by": "rule-based triage"}]
        update["triage"] = tri or offline.triage(state["issue"])
        state = {**state, **update}

    moves = legal_moves(state, deps.cfg.max_coder_attempts)
    dst, reason = moves[0]
    instructions = ""
    if deps.backend == "llm" and deps.cfg.router == "llm" and len(moves) > 1:
        try:
            deps.faults.maybe_fail(state["task_id"], "supervisor")
            summary = {k: state.get(k) for k in ("triage", "research", "patch", "review", "coder_attempts",
                                                  "failed_agents", "rejected_patches")}
            r = run_tool_loop(deps, "supervisor", SUPERVISOR_SYSTEM,
                              issue_text(state["issue"]) + "\n\nState:\n" + compact(summary)
                              + "\n\nAllowed moves:\n" + "\n".join(f"- {d}: {why}" for d, why in moves),
                              [], finish_tool(Route, "route", "Choose the next step."), 3)
            if r["next"] in {d for d, _ in moves}:
                dst, reason, instructions = r["next"], r["reason"], r["instructions"]
            else:
                update.setdefault("errors", []).append({"agent": "supervisor", "error": f"illegal move {r['next']!r}",
                                                        "attempt": 1, "recovered_by": "rule-based routing"})
        except BudgetExceeded:
            raise
        except Exception as e:
            update.setdefault("errors", []).append({"agent": "supervisor", "error": str(e)[:300], "attempt": 1,
                                                    "recovered_by": "rule-based routing"})
    if state.get("research") is None and dst in ("coder", "generalist"):
        # researcher is down: hand over in degraded mode so the next agent investigates itself
        update["research"] = {"reproduced": True, "degraded": True, "suspected_files": [],
                              "root_cause": "researcher unavailable; not yet investigated"}
        instructions = instructions or "The researcher is unavailable: reproduce and localise the bug yourself first."
    update.update(next=dst, instructions=instructions,
                  handoffs=[{"step": step, "src": src, "dst": dst, "reason": reason, "instructions": instructions}])
    return Command(goto=dst, update=update)


# --------------------------------------------------------------------------- terminal nodes

def _close(status: str, msg: str):
    def node(state: AgentState, config) -> dict:
        deps_of(config).workspace.reset_source()
        return {"status": status, "resolution": state.get("resolution") or msg, "trace": [f"close: {status}"]}
    return node


def pr_node(state: AgentState, config) -> dict:
    deps = deps_of(config)
    try:
        pr = open_pr(deps, state)
    except Exception as e:  # PR creation failing must not lose the fix: escalate with the diff attached
        return {"status": "escalated", "resolution": f"fix ready but PR failed: {e}",
                "pr": {"diff": deps.workspace.diff()}, "trace": ["open_pr: FAILED"]}
    return {"status": "pr_opened", "pr": pr, "trace": ["open_pr: ok"]}


def _reviewed(fn):
    """Record rejected patches so the coder doesn't resubmit them."""
    def wrapped(state: AgentState, deps: Deps) -> dict:
        out = fn(state, deps)
        rv, patch = out["review"], state.get("patch") or {}
        if not rv["approved"] and patch.get("key"):
            tag = "regression" if rv["feedback"].startswith("regression") else "review"
            out["rejected_patches"] = [f"{tag}::{patch['key']}"]
        return out
    return wrapped


def _add_terminals(g: StateGraph) -> None:
    g.add_node("open_pr", pr_node)
    g.add_node("close_not_reproducible", _close("not_reproducible", "could not reproduce"))
    g.add_node("close_invalid", _close("invalid", "reported behaviour is intended"))
    g.add_node("escalate", _close("escalated", "needs a human"))
    for t in TERMINALS:
        g.add_edge(t, END)


def build_multi_agent_graph():
    g = StateGraph(AgentState)
    g.add_node("supervisor", supervisor, destinations=(*SPECIALISTS, "verifier", *TERMINALS))
    g.add_node("researcher", resilient("researcher", researcher), destinations=("supervisor",))
    g.add_node("coder", resilient("coder", coder), destinations=("supervisor",))
    g.add_node("reviewer", resilient("reviewer", _reviewed(reviewer)), destinations=("supervisor",))
    g.add_node("verifier", resilient("verifier", _reviewed(verifier)), destinations=("supervisor",))
    g.add_node("generalist", resilient(
        "generalist", lambda s, d: solve_alone(s, d, "generalist", d.cfg.max_single_steps)),
        destinations=("supervisor",))
    _add_terminals(g)
    g.add_edge(START, "supervisor")
    return g.compile()


def _single_router(state: AgentState) -> str:
    if state.get("failed_agents"):
        return "escalate"
    return {"fixed": "open_pr", "not_reproducible": "close_not_reproducible",
            "invalid": "close_invalid"}.get(state.get("resolution", ""), "escalate")


def build_single_agent_graph():
    g = StateGraph(AgentState)
    g.add_node("single", resilient("single", lambda s, d: solve_alone(s, d, "single", d.cfg.max_single_steps),
                                   goto="route"), destinations=("route", "escalate"))
    g.add_node("route", lambda s: {})
    _add_terminals(g)
    g.add_edge(START, "single")
    g.add_conditional_edges("route", _single_router, list(TERMINALS))
    return g.compile()


def run_graph(graph, issue: dict, task_id: str, deps: Deps, recursion_limit: int = 80) -> tuple[dict, float]:
    t0 = time.perf_counter()
    final = graph.invoke({"task_id": task_id, "issue": issue, "status": "open"},
                         config={"configurable": {"deps": deps}, "recursion_limit": recursion_limit})
    return final, time.perf_counter() - t0
