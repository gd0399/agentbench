from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def tasks_dir(tmp_path_factory) -> Path:
    """Use the generated suite if present; otherwise generate the few tasks the tests need."""
    existing = ROOT / "tasks_data"
    if (existing / "index.json").exists():
        return existing
    from agentbench.tasks.generator import generate
    out = tmp_path_factory.mktemp("tasks")
    generate(out, only=["stats-median-parity", "invalid-median-lower", "seq-chunk-last"], log=lambda *a: None)
    return out
