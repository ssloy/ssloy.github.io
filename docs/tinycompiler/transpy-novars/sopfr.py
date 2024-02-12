def main():
	def sopfr(n):
		def sopfr_aux(n):
			nonlocal div
			recursion = 0
			if n % div == 0:
				recursion = div
				if n != div:
					recursion = recursion + sopfr_aux(n // div)
			else:
				div = div + 1
				recursion = sopfr_aux(n)
			return recursion

		div = 2
		return sopfr_aux(n)

	print(sopfr(42))

main()

