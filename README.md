# Assemblings

⚙️ Small exercises to get you used to reading and writing assembly! This project is inspired by [Rustlings](https://github.com/rust-lang/rustlings) and [Ziglings](https://codeberg.org/ziglings/exercises). 

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
