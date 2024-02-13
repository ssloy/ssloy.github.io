'''
def factorial(n):
    if n < 2:
        return 1
    else:
        return n * factorial(n-1)
'''
'''
def factorial(n):
    result = 1
    if n > 1:
        result = n * factorial(n-1)
    return result
'''


def factorial():
    n = stack[-1]
    result = 1
    if n > 1:
        stack.append(n-1)
        result = n * factorial()
        stack.pop()
    return result

stack = []
stack.append(7)
print(factorial())
stack.pop()
