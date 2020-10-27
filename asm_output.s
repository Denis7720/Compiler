.intel_syntax noprefix
.global main
.LC0:
.string "%d\n"
.OUTPUT:
.string "Hello, world!\n"
main:
push rbp
mov rbp, rsp
mov edi, OFFSET FLAT:.OUTPUT
mov eax, 0
call printf
mov eax, 0
nop
pop rbp 
ret
