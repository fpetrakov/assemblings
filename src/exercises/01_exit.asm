section .text

global add_and_double
add_and_double:
    add rdi, rsi
    lea rax, [rdi + rdi]
    ret

global _start
_start:
    call add_and_double
    mov rdi, rax
    mov rax, 60
    syscall
