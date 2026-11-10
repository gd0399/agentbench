"""Sandboxed view of one repository checkout, plus the tools agents get.

All paths are resolved inside the repo root (no traversal). Code execution
happens in a separate `python -I` process with a timeout, so a buggy or
hanging repository can't take the agent process down with it.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

GIT_ENV = {
    "GIT_AUTHOR_NAME": "agentbench", "GIT_AUTHOR_EMAIL": "agentbench@example.invalid",
    "GIT_COMMITTER_NAME": "agentbench", "GIT_COMMITTER_EMAIL": "agentbench@example.invalid",
}
MAX_OUT = 4000


def _clip(s: str, n: int = MAX_OUT) -> str:
    return s if len(s) <= n else s[: n // 2] + f"\n... [{len(s) - n} chars clipped] ...\n" + s[-n // 2:]


@dataclass
class TestRun:
    passed: int
    failed: int
    errors: int
    timed_out: bool
    output: str

    @property
    def ok(self) -> bool:
        return self.failed == 0 and self.errors == 0 and not self.timed_out and self.passed > 0

    def summary(self) -> str:
        head = f"passed={self.passed} failed={self.failed} errors={self.errors}" + (" TIMEOUT" if self.timed_out else "")
        return head + "\n" + _clip(self.output)


class Workspace:
    def __init__(self, root: str | Path, test_timeout: float = 60.0, exec_timeout: float = 10.0):
        self.root = Path(root).resolve()
        self.test_timeout = test_timeout
        self.exec_timeout = exec_timeout

    # -- git -------------------------------------------------------------------
    def git(self, *args: str, check: bool = True) -> str:
        env = {**os.environ, **GIT_ENV}
        p = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True, env=env)
        if check and p.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
        return p.stdout

    def init_git(self) -> None:
        if not (self.root / ".git").exists():
            self.git("init", "-q", "-b", "main")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "initial import", check=False)

    def diff(self, include_tests: bool = True) -> str:
        self.git("add", "-A")
        paths = [] if include_tests else ["--", "toolkit", ":(exclude)tests"]
        return self.git("diff", "--cached", *paths)

    def changed_files(self) -> list[str]:
        self.git("add", "-A")
        return [l for l in self.git("diff", "--cached", "--name-only").splitlines() if l]

    def reset_source(self, keep: tuple[str, ...] = ("tests/",)) -> None:
        """Undo edits outside `keep` (used when a coder retries from a clean slate)."""
        self.git("reset", "-q")
        for line in self.git("status", "--porcelain", "--untracked-files=all").splitlines():
            code, f = line[:2], line[3:]
            if f.startswith(keep):
                continue
            if code.strip() == "??":
                (self.root / f).unlink(missing_ok=True)
            else:
                self.git("checkout", "HEAD", "--", f, check=False)

    # -- paths ---------------------------------------------------------------
    def _path(self, rel: str) -> Path:
        p = (self.root / rel).resolve()
        if p != self.root and self.root not in p.parents:
            raise ValueError(f"path escapes repository: {rel}")
        if ".git" in p.relative_to(self.root).parts:
            raise ValueError("access to .git is not allowed")
        return p

    # -- read ----------------------------------------------------------------
    def list_files(self) -> list[str]:
        out = []
        for p in sorted(self.root.rglob("*")):
            rel = p.relative_to(self.root)
            if p.is_file() and ".git" not in rel.parts and "__pycache__" not in rel.parts:
                out.append(str(rel))
        return out

    def read_file(self, path: str, start: int | None = None, end: int | None = None) -> str:
        lines = self._path(path).read_text().splitlines()
        s = max(1, start or 1)
        e = min(len(lines), end or len(lines))
        return "\n".join(f"{i:>4}| {lines[i - 1]}" for i in range(s, e + 1))

    def raw(self, path: str) -> str:
        return self._path(path).read_text()

    def search(self, pattern: str, glob: str = "*.py") -> str:
        rx = re.compile(pattern)
        hits = []
        for rel in self.list_files():
            if not Path(rel).match(glob):
                continue
            for i, line in enumerate(self.raw(rel).splitlines(), 1):
                if rx.search(line):
                    hits.append(f"{rel}:{i}: {line.strip()}")
        return "\n".join(hits[:100]) or "no matches"

    # -- write ---------------------------------------------------------------
    def write_file(self, path: str, content: str) -> str:
        p = self._path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"wrote {path} ({len(content)} bytes)"

    def replace_in_file(self, path: str, old: str, new: str) -> str:
        p = self._path(path)
        src = p.read_text()
        n = src.count(old)
        if n != 1:
            raise ValueError(f"`old` must match exactly once in {path}; it matched {n} times")
        p.write_text(src.replace(old, new))
        return f"edited {path}"

    # -- execute -------------------------------------------------------------
    def run_python(self, code: str, timeout: float | None = None) -> str:
        prelude = f"import sys; sys.path.insert(0, {str(self.root)!r})\n"
        try:
            p = subprocess.run([sys.executable, "-I", "-c", prelude + code], cwd=self.root,
                               capture_output=True, text=True, timeout=timeout or self.exec_timeout)
        except subprocess.TimeoutExpired:
            return f"TIMEOUT after {timeout or self.exec_timeout}s (possible infinite loop)"
        out = (p.stdout + ("\n[stderr]\n" + p.stderr if p.stderr.strip() else "")).strip()
        return _clip(f"exit={p.returncode}\n{out}")

    def run_tests(self, target: str = "tests", per_test_timeout: int = 5) -> TestRun:
        tgt = str(self._path(target)) if target else str(self.root / "tests")
        cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--rootdir", str(self.root),
               f"--timeout={per_test_timeout}", tgt]
        try:
            p = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, timeout=self.test_timeout)
            out = p.stdout + p.stderr
            timed_out = False
        except subprocess.TimeoutExpired as e:
            out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
            timed_out = True

        def grab(word):
            m = re.search(rf"(\d+) {word}", out)
            return int(m.group(1)) if m else 0
        return TestRun(grab("passed"), grab("failed"), grab("error"), timed_out, out)
