section .text

global sub_and_negate
sub_and_negate:
    sub rdi, rsi
    mov rax, rdi
    ; TODO: rax currently holds (rdi - rsi), but it should hold -(rdi - rsi)
    neg rax
    ret

global _start
_start:
    call sub_and_negate
    mov rdi, rax
    mov rax, 60
    syscall
