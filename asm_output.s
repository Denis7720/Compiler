.intel_syntax noprefix
.global main
.LC0:
.string "%d\n"
main:
push rbp
mov rbp, rsp
mov DWORD PTR [rbp-4], 9
mov DWORD PTR [rbp-8], 4
mov edx, DWORD PTR [rbp-8]
mov DWORD PTR [rbp-4], edx
mov edx, DWORD PTR [rbp-4]
add edx, DWORD PTR [rbp-8]
mov DWORD PTR [rbp-12], edx
mov edx, DWORD PTR [rbp-12]
mov esi, edx
mov edi, OFFSET FLAT:.LC0
mov edx, 0
call printf
mov edx, 0
nop
pop rbp 
ret
