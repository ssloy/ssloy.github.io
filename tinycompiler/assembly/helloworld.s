.global _start
        .data
hello: .ascii "hello world\n"
        hello_len = . - hello
        .align 2
        .text
_start:
        movl $4, %eax         # sys_write system call (check asm/unistd_32.h for the table)
        movl $1, %ebx         # file descriptor (stdout)
        movl $hello, %ecx     # message to write
        movl $hello_len, %edx # message length
        int  $0x80            # make system call

_end:
        movl $1, %eax   # sys_exit system call
        movl $0, %ebx   # error code 0
        int $0x80       # make system call
