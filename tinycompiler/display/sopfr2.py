def main():
    def sopfr():
        def sopfr_aux():
            global display,stack,eax
            stack.append( None )      # allocate memory for local variable rec
            stack.append(display[2])  # save old frame pointer
            display[2] = len(stack)-3 # frame pointer for sopfr_aux()
            stack[display[2]+1] = 0   # rec = 0

            if stack[display[2]+0] % stack[display[1]+1] == 0:  # if n % div == 0
                print(stack)
                stack[display[2]+1] = stack[display[1]+1]       # rec = div
                if  stack[display[2]+0] != stack[display[1]+1]: # if n != div
                    stack.append(stack[display[2]+0]//stack[display[1]+1]) # push n/div ┐
                    sopfr_aux()                                            #            > sopfr_aux(n/div) call
                    del stack[-1:]                                         #  pop n/div ┘
                    stack[display[2]+1] = stack[display[2]+1] + eax
            else:
                stack[display[1]+1] = stack[display[1]+1] + 1
                stack.append(stack[display[2]+0]) # push n  ┐
                sopfr_aux()                       #         > sopfr_aux(n) call
                del stack[-1:]                    #  pop n  ┘
                stack[display[2]+1] = eax

            eax = stack[display[2]+1]
            display[2] = stack.pop()  # restore frame pointer
            del stack[-1:]            # remove rec from stack

        global display,stack,eax
        stack.append( None )      # allocate memory for local variable div
        stack.append(display[1])  # save old frame pointer
        display[1] = len(stack)-3 # frame pointer for sopfr()
        stack[display[1]+1] = 2   # div = 2
        stack.append(stack[display[1]+0]) # push n ┐
        sopfr_aux()                       #        > sopfr_aux(n) call
        del stack[-1:]                    #  pop n ┘
        display[1] = stack.pop()  # restore frame pointer
        del stack[-1:]            # remove div from stack

    global display,stack,eax
    stack.append(display[0])  # save old frame pointer
    display[0] = len(stack)-1 # frame pointer for main()
    stack.append(42)          # push 42 ┐
    sopfr()                   #         > sopfr(42) call
    del stack[-1:]            #  pop 42 ┘
    display[0] = stack.pop()  # restore frame pointer
    print(eax)

display = [ None ]*3 # uninitialized frame pointers
stack   = []         # empty stack
eax     = None       # registers
main()

