def main():
	def even():
		stack.append(display[1])                  # save old frame pointer
		display[1] = len(stack)-2                 # new frame pointer
		if stack[display[1]+0] == 0:              # if n == 0
			stack[display[1]-1] = True            # store return value
		else:
			stack.append( None )                  # allocate memory for return value              \
			stack.append(stack[display[1]+0])     # argument for abs(n) call                      |
			abs()                                 #                                                > abs(n) call
			stack[display[1]+0] = stack[-2]       # n = abs(n)                                    |
			del stack[-2:]                        # remove ret value and argument from the stack  /

			stack.append( None )                  # allocate memory for return value              \
			stack.append(stack[display[1]+0] - 1) # argument for odd(n-1) call                    |
			odd()                                 #                                                > odd(n-1) call
			stack[display[1]-1] = stack[-2]       # store return value                            |
			del stack[-2:]                        # remove ret value and argument from the stack  /
		display[1] = stack.pop()                  # restore frame pointer

	def odd():
		stack.append(display[2])                  # save old frame pointer
		display[2] = len(stack)-2                 # new frame pointer
		if stack[display[2]+0] == 0:              # if n == 0
			stack[display[2]-1] = False           # store return value
		else:
			stack.append( None )                  # allocate memory for return value              \
			stack.append(stack[display[2]+0])     # argument for abs(n) call                      |
			abs()                                 #                                                > abs(n) call
			stack[display[2]+0] = stack[-2]       # n = abs(n)                                    |
			del stack[-2:]                        # remove ret value and argument from the stack  /

			stack.append( None )                  # allocate memory for return value              \
			stack.append(stack[display[2]+0] - 1) # argument for even(n-1) call                   |
			even()                                #                                                > even(n-1) call
			stack[display[2]-1] = stack[-2]       # store return value                            |
			del stack[-2:]                        # remove ret value and argument from the stack  /
		display[2] = stack.pop()                  # restore frame pointer

	def abs():
		stack.append(display[3])                  # save old frame pointer
		display[3] = len(stack)-2                 # new frame pointer
		if stack[display[3]+0] < 0:
			stack[display[3]-1] = -stack[display[3]+0]
		else:
			stack[display[3]-1] =  stack[display[3]+0]
		display[3] = stack.pop()                  # restore frame pointer

	stack.append( None )                      # allocate memory for local variable n
	stack.append(display[0])                  # save old frame pointer
	display[0] = len(stack)-2                 # frame pointer for main()
	stack[display[0]+0] = -3                  # n = -3

	print(f'odd({stack[display[0]+0]}) = ', end='')
	stack.append( None )                      # allocate memory for return value              \
	stack.append(stack[display[0]+0])         # argument for odd(n) call                      |
	odd()                                     #                                                > odd(n) call
	print(stack[-2])                          # print(odd(n))                                 |
	del stack[-2:]                            # remove ret value and argument from the stack  /

	display[0] = stack.pop()                  # restore frame pointer
	del stack[-1:]                            # free local variable

display = [ None ]*4 # uninitialized frame pointers
stack   = []         # empty stack
main()

