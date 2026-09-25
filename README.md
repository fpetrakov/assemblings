# Assemblings

Interactive x86-64 NASM exercise trainer. Each exercise is a `.asm` file under
`src/exercises/` paired with a GDB-scripted test of the same name under
`src/tests/`.

## Requirements

System tools (not installable via `uv`/`pip`):

```
sudo apt install nasm gdb binutils
```

## Run

```
uv run start
```

This will:

1. Recompute progress by rebuilding and running tests for all exercises in
   order, stopping at the first incomplete one.
2. Show a progress bar for exercises already completed.
3. Watch the current exercise's `.asm` file and automatically rebuild + rerun
   just its test whenever you save a change.
4. Once it passes, move on to the next exercise and repeat.

Progress is never written to disk — it's always recomputed by re-running the
tests, so the source of truth is always "does the code actually pass."

## Adding exercises

Add `src/exercises/NN_name.asm` and `src/tests/NN_name.py` with a matching
`NN_name` stem. Exercises are ordered by the leading number in the filename.
Test files use the GDB Python API (`gdb.Breakpoint`, `gdb.execute`,
`gdb.parse_and_eval`); print `"ALL TESTS PASSED"` and exit 0 on success, or
call `sys.exit(1)` on failure.
