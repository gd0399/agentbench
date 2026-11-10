"""Deterministic, no-LLM implementations of each role.

This backend exists so the whole graph + harness runs end-to-end without an
API key (CI, smoke tests, fault-injection experiments). It is a classical
automated-program-repair pipeline, not a language model:

  triage    -> keyword rules on the issue text
  research  -> parse the reproduction out of the issue, write a failing test,
               then spectrum-based fault localisation (Ochiai) using the visible
               test-suite as passing runs and the reproduction as the failing run
  coder     -> mutation search (operator / boundary / builtin swaps) over the
               most suspicious lines, checked against the reproduction
  reviewer  -> run visible tests + reproduction test (same as the `verifier`)

Its numbers say nothing about how LLM agents compare; they validate plumbing.
It is also limited to the shape of this benchmark (a `toolkit` package and
issues that quote a reproduction in backticks).
"""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import tempfile
import tokenize
from pathlib import Path

from ..tasks.generator import evaluate, matches
from ..workspace import Workspace

REPRO_TEST = "tests/test_issue_repro.py"
MODULES = ("stats", "text", "seq", "money", "dates", "report")

# ----------------------------------------------------------------------------- triage / parsing


def parse_issue(issue: dict) -> tuple[str | None, str | None]:
    body = issue["body"]
    snippets = re.findall(r"`([^`\n]+)`", body)
    expr = next((s for s in snippets if "(" in s and s.split(".")[0] in MODULES), None)
    expected = None
    m = re.search(r"should raise `(\w+)`", body)
    if m:
        expected = f"raise {m.group(1)}"
    else:
        m = re.search(r"[Ee]xpected:?\s*`([^`]+)`", body) or re.search(r"should return `([^`]+)`", body)
        if m:
            expected = m.group(1)
    return expr, expected


def triage(issue: dict) -> dict:
    expr, _ = parse_issue(issue)
    body = (issue["title"] + " " + issue["body"]).lower()
    severity = "high" if any(w in body for w in ("hang", "crash", "raises", "production")) else "medium"
    kind = "question" if expr is None else "bug"
    return {"kind": kind, "severity": severity, "component": expr.split(".")[0] if expr else "unknown",
            "summary": issue["title"]}


# ----------------------------------------------------------------------------- reproduction


def write_repro(ws: Workspace, expr: str, expected: str) -> str:
    imports = "import pytest\nfrom toolkit import " + ", ".join(MODULES) + "\n\n\n"
    if expected.startswith("raise "):
        body = f"    with pytest.raises({expected.split()[1]}):\n        {expr}\n"
    else:
        body = f"    assert {expr} == {expected}\n"
    ws.write_file(REPRO_TEST, imports + "def test_issue_repro():\n" + body)
    return REPRO_TEST


TRACE_HELPER = r'''
import importlib.util, json, math, os, signal, sys
repo, expr = sys.argv[1], sys.argv[2]
sys.path.insert(0, repo)
pkg = os.path.join(repo, "toolkit") + os.sep
cur = set()
def tracer(frame, event, arg):
    fn = frame.f_code.co_filename
    if not fn.startswith(pkg):
        return None
    if event == "line":
        cur.add((os.path.relpath(fn, repo), frame.f_lineno))
    return tracer
def traced(fn):
    global cur
    cur = set()
    signal.alarm(3)
    sys.settrace(tracer)
    try:
        fn()
        ok = True
    except BaseException:
        ok = False
    finally:
        sys.settrace(None)
        signal.alarm(0)
    return ok, cur
signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(TimeoutError()))
passed = {}
n_pass = 0
tf = os.path.join(repo, "tests", "test_toolkit.py")
if os.path.exists(tf):
    spec = importlib.util.spec_from_file_location("visible_tests", tf)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    for name in dir(mod):
        if name.startswith("test_"):
            ok, lines = traced(getattr(mod, name))
            if ok:
                n_pass += 1
                for l in lines:
                    passed[l] = passed.get(l, 0) + 1
ns = {}
exec("from toolkit import stats, text, seq, money, dates, report", ns)
_, failing = traced(lambda: eval(expr, ns))
scores = []
for l in failing:
    p = passed.get(l, 0)
    scores.append((l[0], l[1], 1.0 / math.sqrt(1 + p)))
scores.sort(key=lambda t: (-t[2], t[0], t[1]))
print(json.dumps(scores))
'''


def localize(ws: Workspace, expr: str) -> list[tuple[str, int, float]]:
    with tempfile.TemporaryDirectory() as td:
        helper = Path(td) / "sbfl_helper.py"
        helper.write_text(TRACE_HELPER)
        try:
            p = subprocess.run([sys.executable, "-I", str(helper), str(ws.root), expr],
                               capture_output=True, text=True, timeout=60)
            return [tuple(x) for x in json.loads(p.stdout.strip().splitlines()[-1])]
        except Exception:
            return []


def research(ws: Workspace, issue: dict) -> dict:
    expr, expected = parse_issue(issue)
    if not expr or not expected:
        return {"reproduced": False, "root_cause": "could not extract a reproduction from the issue",
                "suspected_files": []}
    path = write_repro(ws, expr, expected)
    run = ws.run_tests(path)
    if run.ok:
        return {"reproduced": False, "repro_test": path, "repro_output": run.summary()[:1500],
                "root_cause": "reproduction passes on main", "suspected_files": []}
    ranked = localize(ws, expr)
    files = []
    for f, _, _ in ranked:
        if f not in files:
            files.append(f)
    top = ", ".join(f"{f}:{ln} ({s:.2f})" for f, ln, s in ranked[:5])
    return {"reproduced": True, "repro_test": path, "repro_output": run.summary()[:1500],
            "suspected_files": files[:3], "root_cause": f"SBFL suspicious lines: {top}",
            "_ranked": ranked, "_expr": expr, "_expected": expected}


# ----------------------------------------------------------------------------- mutation search

OP_SWAPS = {"<": ["<=", ">"], "<=": ["<", ">="], ">": [">=", "<"], ">=": [">", "<="], "==": ["!="], "!=": ["=="],
            "+": ["-"], "-": ["+"], "*": ["/"], "/": ["//", "*"], "//": ["/"]}
NAME_SWAPS = {"and": ["or"], "or": ["and"], "min": ["max"], "max": ["min"], "True": ["False"], "False": ["True"],
              "lower": ["upper"], "upper": ["lower"]}


def line_mutants(line: str) -> list[str]:
    out: list[str] = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(line.strip() + "\n").readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        toks = []
    indent = line[: len(line) - len(line.lstrip())]
    body = line.strip()
    for t in toks:
        (_, c0), (_, c1) = t.start, t.end
        reps: list[str] = []
        if t.type == tokenize.OP:
            reps = OP_SWAPS.get(t.string, [])
        elif t.type == tokenize.NAME:
            reps = NAME_SWAPS.get(t.string, [])
        elif t.type == tokenize.NUMBER and t.string.isdigit():
            n = int(t.string)
            reps = [str(n + 1)] + ([str(n - 1)] if n > 0 else [])
        for r in reps:
            out.append(indent + body[:c0] + r + body[c1:])
    # boundary edits: drop / add "+ 1" / "- 1", and around len(...)
    for m in re.finditer(r"\s*[+-]\s*1\b", body):
        out.append(indent + body[: m.start()] + body[m.end():])
    for m in re.finditer(r"len\([^()]*\)", body):
        for d in (" - 1", " + 1"):
            out.append(indent + body[: m.end()] + d + body[m.end():])
    for a, b in (("[0]", "[-1]"), ("[-1]", "[0]"), ("not ", "")):
        i = body.find(a)
        while i != -1:
            out.append(indent + body[:i] + b + body[i + len(a):])
            i = body.find(a, i + 1)
    seen, uniq = set(), []
    for m in out:
        if m != line and m not in seen:
            seen.add(m)
            uniq.append(m)
    return uniq


def candidates(ws: Workspace, ranked: list[tuple[str, int, float]], max_lines: int = 12):
    """Yield (file, lineno, new_line, key) in order of suspiciousness."""
    for f, ln, _ in ranked[:max_lines]:
        lines = ws.raw(f).splitlines()
        if ln < 1 or ln > len(lines):
            continue
        for new in line_mutants(lines[ln - 1]):
            yield f, ln, new, f"{f}|{ln}|{new.strip()}"


def apply_line(ws: Workspace, f: str, ln: int, new: str) -> None:
    src = ws.raw(f).split("\n")
    src[ln - 1] = new
    ws.write_file(f, "\n".join(src))


def code(ws: Workspace, research_report: dict, rejected: set[str], budget: int) -> dict:
    """Search mutants until one makes the reproduction pass. Leaves the winning edit applied."""
    ranked = research_report.get("_ranked") or []
    expr, expected = research_report.get("_expr"), research_report.get("_expected")
    if not ranked or not expr:
        return {"gave_up": True, "summary": "no localisation available", "files": []}
    tried = 0
    for f, ln, new, key in candidates(ws, ranked):
        if key in rejected:
            continue
        if tried >= budget:
            break
        tried += 1
        ws.reset_source()
        apply_line(ws, f, ln, new)
        if matches(evaluate(ws.root, expr, timeout=3.0), expected):
            return {"gave_up": False, "key": key, "files": [f], "tried": tried,
                    "summary": f"{f}:{ln}: `{new.strip()}` (mutation search, {tried} candidates tried)",
                    "diff": ws.diff()}
    ws.reset_source()
    return {"gave_up": True, "summary": f"no candidate fixed the reproduction ({tried} tried)", "files": [],
            "tried": tried}


def verify(ws: Workspace, repro_test: str | None) -> dict:
    """Deterministic review: visible tests + reproduction must pass and source must have changed."""
    suite = ws.run_tests("tests/test_toolkit.py") if (ws.root / "tests/test_toolkit.py").exists() else None
    repro = ws.run_tests(repro_test) if repro_test and (ws.root / repro_test).exists() else None
    changed = [f for f in ws.changed_files() if not f.startswith("tests/")]
    tests_ok = suite is None or suite.ok
    repro_ok = repro is None or repro.ok
    problems = []
    if not changed:
        problems.append("no source change")
    if not tests_ok:
        fails = re.findall(r"FAILED \S*::(\w+)", suite.output) if suite else []
        problems.append("regression: existing tests fail " + (", ".join(fails[:5]) or suite.summary()[:200]))
    if not repro_ok:
        problems.append("reproduction still fails")
    return {"approved": not problems, "tests_passed": tests_ok, "repro_passed": repro_ok,
            "feedback": "; ".join(problems) or "all checks pass", "reviewer": "verifier"}
