"""Shared state for the agent graphs, and the runtime dependencies passed alongside it.

LangGraph state must be serialisable, so it holds only plain data: the issue,
each specialist's structured report, the handoff log and error log. Live
objects (workspace, model, meter, fault injector) travel in
`config["configurable"]["deps"]`.
"""
from __future__ import annotations

import operator
import random
import zlib
from dataclasses import dataclass, field
from typing import Annotated, Any, Literal, TypedDict

from .llm import ModelChain, UsageMeter
from .workspace import Workspace

Status = Literal["open", "pr_opened", "not_reproducible", "invalid", "escalated"]


class Handoff(TypedDict):
    step: int
    src: str
    dst: str
    reason: str
    instructions: str


class AgentError(TypedDict):
    agent: str
    error: str
    attempt: int
    recovered_by: str


class Triage(TypedDict, total=False):
    kind: str            # bug | feature | question
    severity: str        # low | medium | high
    component: str       # e.g. "stats"
    summary: str


class Research(TypedDict, total=False):
    reproduced: bool
    repro_test: str              # path of the repro test written by the researcher
    repro_output: str
    suspected_files: list[str]
    root_cause: str
    conflicts_with_tests: bool   # requested behaviour contradicts existing tests/docs


class Patch(TypedDict, total=False):
    summary: str
    diff: str
    files: list[str]
    attempt: int
    gave_up: bool


class Review(TypedDict, total=False):
    approved: bool
    feedback: str
    tests_passed: bool
    repro_passed: bool
    reviewer: str     # "reviewer" | "verifier" (deterministic fallback)


class PR(TypedDict, total=False):
    title: str
    body: str
    branch: str
    url: str
    diff: str


class AgentState(TypedDict, total=False):
    task_id: str
    issue: dict
    triage: Triage
    research: Research
    patch: Patch
    review: Review
    pr: PR
    status: Status
    resolution: str
    next: str
    instructions: str
    step: int
    coder_attempts: int
    rejected_patches: Annotated[list[str], operator.add]   # summaries/diffs the reviewer rejected
    failed_agents: Annotated[list[str], operator.add]
    handoffs: Annotated[list[Handoff], operator.add]
    errors: Annotated[list[AgentError], operator.add]
    trace: Annotated[list[str], operator.add]


@dataclass
class RunConfig:
    max_coder_attempts: int = 3
    max_agent_steps: int = 25         # tool-loop iterations per specialist call
    max_single_steps: int = 60        # tool-loop iterations for the single-agent baseline
    node_retries: int = 1             # re-runs of a crashed agent before its fallback kicks in
    router: Literal["llm", "rules"] = "rules"
    offline_candidate_budget: int = 60  # offline coder: candidate patches it may try per call
    open_real_pr: bool = False


class InjectedFailure(RuntimeError):
    """Raised by FaultInjector to simulate an agent crashing (timeout, malformed output, ...)."""


@dataclass
class FaultInjector:
    """Deterministic, seeded failure injection: same (seed, task, agent, call#) -> same outcome."""
    rate: float = 0.0
    seed: int = 0
    counts: dict = field(default_factory=dict)
    injected: int = 0

    def maybe_fail(self, task_id: str, agent: str) -> None:
        if self.rate <= 0:
            return
        k = (task_id, agent)
        self.counts[k] = self.counts.get(k, 0) + 1
        h = zlib.crc32(f"{self.seed}|{task_id}|{agent}|{self.counts[k]}".encode())
        if random.Random(h).random() < self.rate:
            self.injected += 1
            raise InjectedFailure(f"injected failure in {agent} (call {self.counts[k]})")


@dataclass
class Deps:
    workspace: Workspace
    meter: UsageMeter
    backend: Literal["llm", "offline"] = "offline"
    model: ModelChain | None = None
    faults: FaultInjector = field(default_factory=FaultInjector)
    cfg: RunConfig = field(default_factory=RunConfig)
    github: Any = None   # agentbench.github_pr.GitHubTarget when opening real PRs


def deps_of(config) -> Deps:
    return config["configurable"]["deps"]
