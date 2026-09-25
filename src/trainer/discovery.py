from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .paths import EXERCISES_DIR, TESTS_DIR


@dataclass(frozen=True)
class Exercise:
    stem: str
    asm_path: Path
    test_path: Path

    @property
    def name(self) -> str:
        return self.stem


def _natural_key(stem: str):
    match = re.match(r"^(\d+)", stem)
    num = int(match.group(1)) if match else float("inf")
    return (num, stem)


def discover_exercises() -> list[Exercise]:
    if not EXERCISES_DIR.exists():
        raise FileNotFoundError(f"Exercises directory not found: {EXERCISES_DIR}")
    if not TESTS_DIR.exists():
        raise FileNotFoundError(f"Tests directory not found: {TESTS_DIR}")

    exercises = []
    for asm_path in EXERCISES_DIR.glob("*.asm"):
        stem = asm_path.stem
        test_path = TESTS_DIR / f"{stem}.py"
        if not test_path.exists():
            continue
        exercises.append(Exercise(stem=stem, asm_path=asm_path, test_path=test_path))

    exercises.sort(key=lambda e: _natural_key(e.stem))
    return exercises
