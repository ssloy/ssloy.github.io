'''
def factorial(n):
    if n < 2:
        return 1
    else:
        return n * factorial(n-1)
'''
import inspect

def factorial(n):
    result = 1
    print('instances of n:', [frame[0].f_locals['n'] for frame in reversed(inspect.stack()[:-1])])
    if n > 1:
        result = n * factorial(n-1)
    return result

print(factorial(7))
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


def factorial():
    result = 1
    if stack[-1] > 1:
        stack.append(stack[-1]-1)
        result = stack[-2] * factorial() # note -2 here
        stack.pop()
    return result

stack = []
stack.append(7)
print(factorial())
stack.pop()

'''
