"""Researcher, coder, reviewer and the generalist fallback.

Every specialist is a plain function (state, deps) -> partial state update.
Graph wiring (handoffs, retries, fallbacks) lives in `graph.py`.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from ..state import AgentState, Deps
from . import offline
from .base import build_tools, compact, finish_tool, issue_text, run_tool_loop

READ = {"list_files", "read_file", "search_code"}
EXEC = {"run_python", "run_tests"}
WRITE = {"write_file", "replace_in_file"}

# --------------------------------------------------------------------------- researcher

RESEARCHER_SYSTEM = """You are the RESEARCHER on a software maintenance team. A supervisor hands you a GitHub issue.
Your job: reproduce it and localise the root cause. You do NOT fix code.

1. Read the issue and find the claimed behaviour.
2. Write a minimal failing pytest at tests/test_issue_repro.py that encodes the EXPECTED behaviour, and run it.
3. If it passes on the current code, the issue does not reproduce.
4. If it fails, trace the code path (read files, run snippets) and identify the file(s) and line(s) at fault.
5. Check the docstrings and existing tests: if the requested behaviour contradicts documented/tested behaviour,
   set conflicts_with_tests=true (the report may be a misunderstanding, not a bug).
Then call submit_research. Be efficient: you have a limited number of steps."""


class ResearchOut(BaseModel):
    reproduced: bool = Field(description="True if the failing repro test fails on current code")
    repro_test: str = Field(default="tests/test_issue_repro.py")
    suspected_files: list[str] = Field(default_factory=list, description="Most likely files, best first")
    root_cause: str = Field(description="Precise explanation: file, line, what is wrong")
    conflicts_with_tests: bool = Field(default=False, description="Requested behaviour contradicts docs/tests")


def researcher(state: AgentState, deps: Deps) -> dict:
    if deps.backend == "offline":
        deps.meter.note_step("researcher")
        return {"research": offline.research(deps.workspace, state["issue"])}
    tools = build_tools(deps.workspace, READ | EXEC | {"write_file"}, write_prefix="tests/")
    user = issue_text(state["issue"]) + f"\n\nTriage: {compact(state.get('triage', {}))}"
    if state.get("instructions"):
        user += f"\n\nSupervisor instructions: {state['instructions']}"
    out = run_tool_loop(deps, "researcher", RESEARCHER_SYSTEM, user, tools,
                        finish_tool(ResearchOut, "submit_research", "Submit your research findings."),
                        deps.cfg.max_agent_steps)
    run = deps.workspace.run_tests(out["repro_test"]) if (deps.workspace.root / out["repro_test"]).exists() else None
    if run is not None:
        out["repro_output"] = run.summary()[:1500]
        out["reproduced"] = not run.ok      # trust the test run over the model's claim
    return {"research": out}


# --------------------------------------------------------------------------- coder

CODER_SYSTEM = """You are the CODER on a software maintenance team. You receive a GitHub issue plus the researcher's
findings (reproduction test and suspected root cause). Make the smallest correct source change that fixes the
root cause. Do not edit or delete existing tests; do not special-case the reproduction input.
Run the reproduction test and the full test suite before submitting. If a reviewer rejected an earlier attempt,
address their feedback. Call submit_patch when done (gave_up=true only if you truly cannot fix it)."""


class PatchOut(BaseModel):
    summary: str = Field(description="What you changed and why (1-3 sentences)")
    gave_up: bool = False


def coder(state: AgentState, deps: Deps) -> dict:
    attempt = state.get("coder_attempts", 0) + 1
    research = state.get("research") or {}
    if deps.backend == "offline":
        deps.meter.note_step("coder")
        if not research.get("_ranked"):          # degraded mode (researcher failed): research ourselves
            research = offline.research(deps.workspace, state["issue"])
            if not research.get("reproduced"):
                return {"research": research, "patch": {"gave_up": True, "attempt": attempt, "summary": "did not reproduce"},
                        "coder_attempts": attempt}
        rejected = {r.split("::", 1)[-1] for r in state.get("rejected_patches", [])}
        out = offline.code(deps.workspace, research, rejected, deps.cfg.offline_candidate_budget)
        update = {"patch": {**out, "attempt": attempt}, "coder_attempts": attempt}
        if research is not state.get("research"):
            update["research"] = research
        return update
    tools = build_tools(deps.workspace, READ | EXEC | WRITE | {"view_diff"})
    user = issue_text(state["issue"]) + "\n\nResearch:\n" + compact(
        {k: v for k, v in research.items() if not k.startswith("_")} or "researcher unavailable: investigate yourself")
    if state.get("review") and not state["review"].get("approved"):
        user += f"\n\nReviewer rejected attempt {attempt - 1}: {state['review'].get('feedback')}"
    if state.get("instructions"):
        user += f"\n\nSupervisor instructions: {state['instructions']}"
    out = run_tool_loop(deps, "coder", CODER_SYSTEM, user, tools,
                        finish_tool(PatchOut, "submit_patch", "Submit your patch."), deps.cfg.max_agent_steps)
    diff = deps.workspace.diff()
    out.update(attempt=attempt, diff=diff, files=[f for f in deps.workspace.changed_files() if not f.startswith("tests/")],
               key=f"attempt{attempt}")
    return {"patch": out, "coder_attempts": attempt}


# --------------------------------------------------------------------------- reviewer

REVIEWER_SYSTEM = """You are the REVIEWER on a software maintenance team. You review the coder's patch for a GitHub
issue. Check: (1) does it fix the root cause rather than the symptom or the specific test input, (2) is it minimal,
(3) does it break any behaviour (run the tests; probe edge cases with run_python), (4) were tests tampered with.
Approve only if you would merge it. If you reject, give concrete, actionable feedback. Call submit_review."""


class ReviewOut(BaseModel):
    approved: bool
    feedback: str


def reviewer(state: AgentState, deps: Deps) -> dict:
    research = state.get("research") or {}
    checks = offline.verify(deps.workspace, research.get("repro_test"))
    if deps.backend == "offline":
        deps.meter.note_step("reviewer")
        return {"review": {**checks, "reviewer": "reviewer", "attempt": state.get("coder_attempts", 0)}}
    tools = build_tools(deps.workspace, READ | EXEC | {"view_diff"})
    user = (issue_text(state["issue"]) + "\n\nCoder summary: " + state["patch"].get("summary", "")
            + "\n\nDiff:\n" + (state["patch"].get("diff") or "(empty)")[:6000]
            + f"\n\nAutomated checks: {checks['feedback']}")
    out = run_tool_loop(deps, "reviewer", REVIEWER_SYSTEM, user, tools,
                        finish_tool(ReviewOut, "submit_review", "Submit your review."), deps.cfg.max_agent_steps)
    # Guardrail: a reviewer can reject a green patch, but can never approve a red one.
    approved = bool(out["approved"]) and checks["approved"]
    feedback = out["feedback"] if approved == out["approved"] else f"{checks['feedback']}. {out['feedback']}"
    return {"review": {**checks, "approved": approved, "feedback": feedback, "reviewer": "reviewer",
                       "attempt": state.get("coder_attempts", 0)}}


def verifier(state: AgentState, deps: Deps) -> dict:
    """Deterministic fallback for the reviewer: no model, can't crash on model errors."""
    research = state.get("research") or {}
    return {"review": {**offline.verify(deps.workspace, research.get("repro_test")),
                       "attempt": state.get("coder_attempts", 0)}}


# --------------------------------------------------------------------------- generalist / single agent

GENERALIST_SYSTEM = """You are a software engineer resolving a GitHub issue end to end, alone.
1. Reproduce: write a failing pytest at tests/test_issue_repro.py encoding the expected behaviour; run it.
   If it passes on current code, finish with status=not_reproducible.
   If the requested behaviour contradicts documented/tested behaviour, finish with status=invalid and explain.
2. Localise the root cause (read code, run snippets).
3. Fix it with the smallest correct source change. Never edit existing tests or special-case inputs.
4. Run the reproduction test and the whole test suite; iterate until green.
5. Call submit_resolution with status=fixed (or give_up if you cannot fix it)."""


class ResolutionOut(BaseModel):
    status: Literal["fixed", "not_reproducible", "invalid", "give_up"]
    summary: str
    root_cause: str = ""
    suspected_files: list[str] = Field(default_factory=list)


def solve_alone(state: AgentState, deps: Deps, agent: str, max_steps: int) -> dict:
    """One agent does everything. Used as the single-agent baseline and as the coder fallback."""
    ws = deps.workspace
    if deps.backend == "offline":
        deps.meter.note_step(agent)
        research = state.get("research") or {}
        if not research.get("_ranked"):
            research = offline.research(ws, state["issue"])
        if not research.get("reproduced"):
            return {"research": research, "resolution": "not_reproducible"}
        rejected: set[str] = set(r.split("::", 1)[-1] for r in state.get("rejected_patches", []))
        regressions = 0
        budget = deps.cfg.offline_candidate_budget * deps.cfg.max_coder_attempts
        while budget > 0:
            out = offline.code(ws, research, rejected, budget)
            if out["gave_up"]:
                break
            budget -= out["tried"]
            check = offline.verify(ws, research.get("repro_test"))
            if check["approved"]:
                return {"research": research, "patch": {**out, "attempt": 1}, "review": check, "resolution": "fixed"}
            regressions += check["feedback"].startswith("regression")
            rejected.add(out["key"])
        ws.reset_source()
        status = "invalid" if regressions and regressions == len(rejected) else "give_up"
        return {"research": research, "resolution": status,
                "patch": {"gave_up": True, "summary": f"{len(rejected)} candidates rejected", "attempt": 1}}
    tools = build_tools(ws, READ | EXEC | WRITE | {"view_diff"})
    user = issue_text(state["issue"])
    if state.get("research"):
        user += "\n\nNotes from a colleague:\n" + compact({k: v for k, v in state["research"].items() if not k.startswith("_")})
    out = run_tool_loop(deps, agent, GENERALIST_SYSTEM, user, tools,
                        finish_tool(ResolutionOut, "submit_resolution", "Finish the task."), max_steps)
    research = {**(state.get("research") or {}), "root_cause": out["root_cause"],
                "suspected_files": out["suspected_files"],
                "reproduced": out["status"] not in ("not_reproducible",), "repro_test": "tests/test_issue_repro.py"}
    update = {"research": research, "resolution": out["status"]}
    if out["status"] == "fixed":
        check = offline.verify(ws, research["repro_test"])
        update["patch"] = {"summary": out["summary"], "diff": ws.diff(), "attempt": 1,
                           "files": [f for f in ws.changed_files() if not f.startswith("tests/")]}
        update["review"] = check
        if not check["approved"]:
            update["resolution"] = "give_up"   # claimed fixed but checks are red
    return update
