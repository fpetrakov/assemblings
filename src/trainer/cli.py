from __future__ import annotations

import shutil
import sys
import time

from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn

from .discovery import Exercise, discover_exercises
from .state import hash_file
from .testrunner import run_exercise_test

console = Console()
POLL_INTERVAL = 0.5


def check_dependencies() -> None:
    missing = [tool for tool in ("nasm", "ld", "gdb") if shutil.which(tool) is None]
    if missing:
        console.print(
            f"[bold red]Missing required tool(s): {', '.join(missing)}[/bold red]"
        )
        console.print(
            "Install them, e.g. on Debian/Ubuntu: [cyan]sudo apt install nasm gdb binutils[/cyan]"
        )
        sys.exit(1)


def find_current(exercises: list[Exercise]) -> tuple[int, int]:
    passed_count = 0
    for i, ex in enumerate(exercises):
        console.print(f"[dim]checking {ex.name}...[/dim]", end="\r")
        result = run_exercise_test(ex)
        console.print(" " * 40, end="\r")
        if not result.passed:
            return i, passed_count
        passed_count += 1
    return len(exercises), passed_count


def show_progress(done: int, total: int) -> None:
    with Progress(
        TextColumn("[bold green]Progress"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total} exercises"),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("progress", total=total, completed=done)
        progress.update(task, completed=done)
        time.sleep(0.5)


def print_result(exercise: Exercise, log: str, passed: bool) -> None:
    if passed:
        console.print(f"[bold green]\u2714 PASS[/bold green]  {exercise.name}")
    else:
        console.print(f"[bold red]\u2718 FAIL[/bold red]  {exercise.name}")
    if log:
        console.print(f"[dim]{log}[/dim]")


def watch_and_run(exercise: Exercise) -> None:
    console.rule(f"[bold cyan]{exercise.name}[/bold cyan]")
    console.print(f"[dim]Editing: {exercise.asm_path}[/dim]")
    console.print(
        "[dim]Save the file to rerun the test automatically. Ctrl+C to quit.[/dim]\n"
    )

    last_hash = hash_file(exercise.asm_path)
    result = run_exercise_test(exercise)
    print_result(exercise, result.log, result.passed)

    while not result.passed:
        time.sleep(POLL_INTERVAL)
        current_hash = hash_file(exercise.asm_path)
        if current_hash == last_hash:
            continue
        last_hash = current_hash
        console.print(
            f"\n[yellow]Change detected \u2014 rerunning {exercise.name}...[/yellow]"
        )
        result = run_exercise_test(exercise)
        print_result(exercise, result.log, result.passed)


def main() -> None:
    check_dependencies()
    console.print("[bold]Assemblings![/bold]\n")
    exercises = discover_exercises()
    if not exercises:
        console.print(
            "[red]No exercise/test pairs found under src/exercises and src/tests.[/red]"
        )
        sys.exit(1)
    total = len(exercises)

    try:
        while True:
            idx, done = find_current(exercises)

            if done == total:
                show_progress(total, total)
                console.print(
                    "\n[bold green]\U0001f389 All exercises complete![/bold green]"
                )
                return

            show_progress(done, total)
            watch_and_run(exercises[idx])
    except KeyboardInterrupt:
        console.print("\n[dim]Bye.[/dim]")


if __name__ == "__main__":
    main()
