import sys

import gdb


def eq(name, actual, expected):
    if actual != expected:
        print(f"FAIL: {name} = {actual}, expected {expected}")
        sys.exit(1)
    print(f"PASS: {name} = {actual}")


def call_and_check(func_name, rdi_val, rsi_val, expected_rax):
    bp = gdb.Breakpoint(func_name)
    gdb.execute("run")

    gdb.execute(f"set $rdi = {rdi_val}")
    gdb.execute(f"set $rsi = {rsi_val}")

    gdb.execute("finish")
    rax = int(gdb.parse_and_eval("$rax"))
    eq(f"{func_name}({rdi_val},{rsi_val}) -> rax", rax, expected_rax)

    bp.delete()
    gdb.execute("kill")


call_and_check("add_and_double", 5, 10, 30)
call_and_check("add_and_double", 0, 0, 0)
call_and_check("add_and_double", -1, 1, 0)

print("ALL TESTS PASSED")
