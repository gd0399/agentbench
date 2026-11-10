"""Tool factory and the tool-calling loop shared by every LLM-backed agent."""
from __future__ import annotations

import json
from typing import Callable

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel

from ..state import Deps
from ..workspace import Workspace


class AgentGaveUp(RuntimeError):
    """The agent hit its step limit without calling its finish tool."""


def build_tools(ws: Workspace, allow: set[str], write_prefix: str | None = None) -> list[StructuredTool]:
    """Workspace tools, filtered by `allow`. `write_prefix` restricts writes (e.g. researcher -> tests/)."""

    def guard(path: str) -> None:
        if write_prefix and not path.startswith(write_prefix):
            raise PermissionError(f"this agent may only write under {write_prefix}")

    def list_files() -> str:
        """List all files in the repository."""
        return "\n".join(ws.list_files())

    def read_file(path: str, start: int = 1, end: int = 0) -> str:
        """Read a file with line numbers. Optionally restrict to lines start..end."""
        return ws.read_file(path, start, end or None)

    def search_code(pattern: str) -> str:
        """Regex search over the repository's Python files. Returns path:line: text."""
        return ws.search(pattern)

    def run_python(code: str) -> str:
        """Run a Python snippet with the repo importable (e.g. `from toolkit import stats`). 10s timeout."""
        return ws.run_python(code)

    def run_tests(target: str = "tests") -> str:
        """Run pytest on a file or directory (default: tests). Returns counts and output."""
        return ws.run_tests(target).summary()

    def write_file(path: str, content: str) -> str:
        """Create or overwrite a file with the given content."""
        guard(path)
        return ws.write_file(path, content)

    def replace_in_file(path: str, old: str, new: str) -> str:
        """Replace an exact snippet (must occur exactly once) in a file. Include enough context to be unique."""
        guard(path)
        return ws.replace_in_file(path, old, new)

    def view_diff() -> str:
        """Show the current uncommitted diff against the original repository."""
        return ws.diff() or "(no changes)"

    fns: dict[str, Callable] = {f.__name__: f for f in (
        list_files, read_file, search_code, run_python, run_tests, write_file, replace_in_file, view_diff)}
    return [StructuredTool.from_function(fns[n]) for n in fns if n in allow]


def finish_tool(model: type[BaseModel], name: str, description: str) -> StructuredTool:
    def _finish(**kwargs):
        return "recorded"
    return StructuredTool.from_function(_finish, name=name, description=description, args_schema=model)


def run_tool_loop(deps: Deps, agent: str, system: str, user: str, tools: list[StructuredTool],
                  finish: StructuredTool, max_steps: int) -> dict:
    """ReAct-style loop. Returns the finish tool's arguments. Raises AgentGaveUp on step exhaustion."""
    assert deps.model is not None, "LLM backend requires a model"
    by_name = {t.name: t for t in tools}
    messages: list = [SystemMessage(system), HumanMessage(user)]
    nudges = 0
    for _ in range(max_steps):
        ai: AIMessage = deps.model.invoke(messages, tools=[*tools, finish], agent=agent, meter=deps.meter)
        messages.append(ai)
        if not ai.tool_calls:
            nudges += 1
            if nudges > 2:
                raise AgentGaveUp(f"{agent} stopped calling tools")
            messages.append(HumanMessage(f"Use a tool to continue, or call `{finish.name}` to finish."))
            continue
        for call in ai.tool_calls:
            if call["name"] == finish.name:
                try:
                    return finish.args_schema(**call["args"]).model_dump()
                except Exception as e:  # malformed structured output -> tell the model and continue
                    messages.append(ToolMessage(f"invalid arguments: {e}", tool_call_id=call["id"]))
                    continue
            tool = by_name.get(call["name"])
            if tool is None:
                out = f"unknown tool {call['name']!r}"
            else:
                try:
                    out = tool.invoke(call["args"])
                except Exception as e:
                    out = f"ERROR: {type(e).__name__}: {e}"
            messages.append(ToolMessage(str(out)[:8000], tool_call_id=call["id"]))
    raise AgentGaveUp(f"{agent} exceeded {max_steps} steps")


def issue_text(issue: dict) -> str:
    return f"Issue #{issue['number']}: {issue['title']}\n(opened by @{issue.get('author', 'user')})\n\n{issue['body']}"


def compact(obj) -> str:
    return json.dumps(obj, indent=1, default=str)[:6000]
