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
SRC_DIR = ROOT / "src"
EXERCISES_DIR = SRC_DIR / "exercises"
TESTS_DIR = SRC_DIR / "tests"
BUILD_DIR = ROOT / ".build"
paths = [
    str(TESTS_DIR),
    str(BUILD_DIR),
    str(EXERCISES_DIR),
    str(SRC_DIR),
    str(ROOT),
]
