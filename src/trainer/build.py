from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .discovery import Exercise
from .paths import BUILD_DIR


@dataclass
class BuildResult:
    ok: bool
    binary_path: Path | None
    log: str


def build_exercise(exercise: Exercise) -> BuildResult:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    object_path = BUILD_DIR / f"{exercise.stem}.o"
    binary_path = BUILD_DIR / exercise.stem

    nasm = subprocess.run(
        ["nasm", "-f", "elf64", "-g", str(exercise.asm_path), "-o", str(object_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if nasm.returncode != 0:
        return BuildResult(False, None, f"nasm error:\n{nasm.stderr.strip()}")

    ld = subprocess.run(
        ["ld", str(object_path), "-o", str(binary_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if ld.returncode != 0:
        return BuildResult(False, None, f"ld error:\n{ld.stderr.strip()}")

    return BuildResult(True, binary_path, "")
