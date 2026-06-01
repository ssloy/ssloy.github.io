def main():
	def even(n):
		if n == 0:
			return True
		else:
			n = abs(n)
			return odd(n - 1)

	def odd(n):
		if n == 0:
			return False
		else:
			n = abs(n)
			return even(n - 1)

	def abs(n):
		if n < 0:
			return -n
		else:
			return n

	n = -3
	print(f'odd({n}) = ', end='')
	print(odd(n))

main()

