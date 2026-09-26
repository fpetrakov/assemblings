from __future__ import annotations

from trainer.exceptions import CheckError


def eq(name, actual, expected):
    if actual != expected:
        raise CheckError(name, actual, expected)
    print(f"PASS: {name} = {actual}")
