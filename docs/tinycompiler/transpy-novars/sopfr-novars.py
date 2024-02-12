def main_uniqstr4():
	global eax, ebx, stack, display
	def sopfr_uniqstr5():
		global eax, ebx, stack, display
		def sopfr_aux_uniqstr6():
			global eax, ebx, stack, display
			
			eax = 0
			stack[display[2]+1] = eax # recursion
			
			eax = stack[display[2]+0] # n
			stack.append(eax) # evaluate left argument and stash it
			eax = stack[display[1]+1] # div
			ebx = eax # evaluate right arg
			eax = stack.pop() # recall left arg
			eax = eax % ebx # binary operation
			stack.append(eax) # evaluate left argument and stash it
			eax = 0
			ebx = eax # evaluate right arg
			eax = stack.pop() # recall left arg
			eax = eax == ebx # binary operation
			if eax:
				eax = stack[display[1]+1] # div
				stack[display[2]+1] = eax # recursion
				eax = stack[display[2]+0] # n
				stack.append(eax) # evaluate left argument and stash it
				eax = stack[display[1]+1] # div
				ebx = eax # evaluate right arg
				eax = stack.pop() # recall left arg
				eax = eax != ebx # binary operation
				if eax:
					eax = stack[display[2]+1] # recursion
					stack.append(eax) # evaluate left argument and stash it
					# prepare sopfr_aux() call
					# evalaute function arguments
					eax = stack[display[2]+0] # n
					stack.append(eax) # evaluate left argument and stash it
					eax = stack[display[1]+1] # div
					ebx = eax # evaluate right arg
					eax = stack.pop() # recall left arg
					eax = eax // ebx # binary operation
					stack.append(eax)
					# reserve local variables
					stack.append( None ) # recursion
					stack.append(display[2]) # save old frame pointer
					display[2] = len(stack)-3 # activate new frame pointer
					eax = sopfr_aux_uniqstr6()
					display[2] = stack.pop() # restore old frame pointer
					del stack[-2] # delete fun args and local vars if any, thus finishing sopfr_aux() call
					ebx = eax # evaluate right arg
					eax = stack.pop() # recall left arg
					eax = eax + ebx # binary operation
					stack[display[2]+1] = eax # recursion
				else:
					pass
			else:
				eax = stack[display[1]+1] # div
				stack.append(eax) # evaluate left argument and stash it
				eax = 1
				ebx = eax # evaluate right arg
				eax = stack.pop() # recall left arg
				eax = eax + ebx # binary operation
				stack[display[1]+1] = eax # div
				# prepare sopfr_aux() call
				# evalaute function arguments
				eax = stack[display[2]+0] # n
				stack.append(eax)
				# reserve local variables
				stack.append( None ) # recursion
				stack.append(display[2]) # save old frame pointer
				display[2] = len(stack)-3 # activate new frame pointer
				eax = sopfr_aux_uniqstr6()
				display[2] = stack.pop() # restore old frame pointer
				del stack[-2] # delete fun args and local vars if any, thus finishing sopfr_aux() call
				stack[display[2]+1] = eax # recursion
			
			eax = stack[display[2]+1] # recursion
			return eax
		
		eax = 2
		stack[display[1]+1] = eax # div
		
		# prepare sopfr_aux() call
		# evalaute function arguments
		eax = stack[display[1]+0] # n
		stack.append(eax)
		# reserve local variables
		stack.append( None ) # recursion
		stack.append(display[2]) # save old frame pointer
		display[2] = len(stack)-3 # activate new frame pointer
		eax = sopfr_aux_uniqstr6()
		display[2] = stack.pop() # restore old frame pointer
		del stack[-2] # delete fun args and local vars if any, thus finishing sopfr_aux() call
		return eax
	
	# prepare sopfr() call
	# evalaute function arguments
	eax = 42
	stack.append(eax)
	# reserve local variables
	stack.append( None ) # div
	stack.append(display[1]) # save old frame pointer
	display[1] = len(stack)-3 # activate new frame pointer
	eax = sopfr_uniqstr5()
	display[1] = stack.pop() # restore old frame pointer
	del stack[-2] # delete fun args and local vars if any, thus finishing sopfr() call
	print(eax, end='\n')

eax, ebx = None, None
display = [ 65536 ]*3
stack = []
display[0] = len(stack) # frame pointer for fun main
pass
main_uniqstr4()

