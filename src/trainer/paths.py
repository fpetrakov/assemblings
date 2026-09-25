from __future__ import annotations

from pathlib import Path


def _find_project_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError(
        "Could not locate project root (no pyproject.toml found above "
        "the trainer package)."
    )


ROOT = _find_project_root()
EXERCISES_DIR = ROOT / "src" / "exercises"
TESTS_DIR = ROOT / "src" / "tests"
BUILD_DIR = ROOT / ".build"
