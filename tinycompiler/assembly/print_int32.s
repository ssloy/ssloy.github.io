.global _start
        .data
        .align 2
        .text
_start:
        pushl $-729
        call print_int32
        addl $4, %esp
_end:
        movl $1, %eax   # sys_exit system call
        movl $0, %ebx   # error code 0
        int $0x80       # make system call

print_int32:
        movl 4(%esp), %eax  # the number to print
        cdq
        xorl %edx, %eax
        subl %edx, %eax     # abs(%eax)
        pushl $10           # base 10
        movl %esp, %ecx     # buffer for the string to print
        subl $16, %esp      # max 10 digits for a 32-bit number (keep %esp dword-aligned)
0:      xorl %edx, %edx     #     %edx = 0
        divl 16(%esp)       #     %eax = %edx:%eax/10 ; %edx = %edx:%eax % 10
        decl %ecx           #     allocate one more digit
        addb $48, %dl       #     %edx += '0'       # 0,0,0,0,0,0,0,0,0,0,'1','2','3','4','5','6'
        movb %dl, (%ecx)    #     store the digit   # ^                   ^                    ^
        test %eax, %eax     #                       # %esp                %ecx (after)         %ecx (before)
        jnz 0b              # until %eax==0         #                     <----- %edx = 6 ----->
        cmp %eax, 24(%esp)  # if the number is negative                            |
        jge 0f              #                                                      |
        decl %ecx           # allocate one more character                          |
        movb $45, 0(%ecx)   # '-'                                                  |
0:      movl $4, %eax       # write system call                                    |
        movl $1, %ebx       # stdout                                               |
        leal 16(%esp), %edx # the buffer to print                                  |
        subl %ecx, %edx     # number of digits    <--------------------------------┘
        int $0x80           # make system call
        addl $20, %esp      # deallocate the buffer
        ret
