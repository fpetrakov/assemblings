from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass

from .build import build_exercise
from .discovery import Exercise
from .exceptions import CheckError
from .paths import ROOT, paths


@dataclass
class TestResult:
    passed: bool
    log: str


def run_exercise_test(exercise: Exercise, timeout: int = 15) -> TestResult:
    build = build_exercise(exercise)
    if not build.ok:
        return TestResult(False, build.log)

    cmd = [
        "gdb",
        "-q",  # no version banner
        "--nx",  # ignore system/home .gdbinit, so runs are reproducible
        # across machines regardless of personal gdb config
    ]

    # Explicitly (re-)opt in to a project-level .gdbinit, if present, instead
    # of relying on gdb's own auto-discovery (which --nx disables). This is
    # sourced before the test script, so `set` options, pretty-printers, etc.
    # defined there are active when the test runs.
    project_gdbinit = ROOT / ".gdbinit"
    if project_gdbinit.exists():
        cmd += ["-x", str(project_gdbinit)]

    # gdb needs those to resolve imports inside python tests
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        paths + env.get("PYTHONPATH", "").split(os.pathsep)
    )

    cmd += [
        "--batch",  # run script(s) and exit, no interactive prompt
        "-x",
        str(exercise.test_path),
        "--args",
        str(build.binary_path),
    ]

    try:
        gdb = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return TestResult(False, f"Test timed out after {timeout}s (infinite loop?).")
    except CheckError as error:
        return TestResult(False, str(error))

    success = gdb.returncode == 0
    if success:
        print(f"{exercise.test_path}: ALL TESTS PASSED")
    log = (gdb.stdout + gdb.stderr).strip()
    return TestResult(success, log)
