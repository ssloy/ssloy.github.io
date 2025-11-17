from float8c import *

'''
errcnt = 0
for i in range(256):
    a = Float8.from_uint8(i)
    for j in range(256):
        b = Float8.from_uint8(j)
        c = a + b
        d = Float8.from_float(float(a)+float(b))
        errcnt += (float(c) != float(d))
        print(str(float(a)) + ' + ' + str(float(b)) + ' = ' + str(float(d)) + ( '\t= ' if float(c)==float(d) else '\t!= ' ) + str(float(c)) )
        errcnt += (float(c) != float(d))
print(errcnt, 'errors detected')

'''

for i in range(128):
    print(i, float(Float8.from_uint8(i)))

'''
for i in range(96):
    a = float(Float8.from_uint8(i))
    for j in range(96):
        b = float(Float8.from_uint8(j))
        s = a*a - b*b
        if not s: continue
        t = float(Float8.from_float(a*a)) - float(Float8.from_float(b*b))
        print(abs(t - s)/abs(s), abs(t-s), a, b)

'''
#arr = [ Float8.from_float(1/128) for _ in range(128) ]
import random
random.seed(1)
arr = [ Float8.from_float(random.uniform(-0.25, .25)) for _ in range(128) ]
print(([float(v) for v in arr]))


def naive_sum(arr):
    s = Float8.from_float(0.)
    for v in arr:
        s += v
    return s

print('naive sum:\t', float(naive_sum(arr)))

def pairwise_sum(arr):
    match len(arr):
        case 0:
            return Float8.from_float(0)
        case 1:
            return arr[0]
    mid = len(arr)//2
    return pairwise_sum(arr[:mid]) + \
           pairwise_sum(arr[mid:])

print('pairwise sum:\t', float(pairwise_sum(arr)))

def kahan_sum(arr):
    s, c = Float8.from_float(0), Float8.from_float(0)
    for v in arr:
        t = s + (v - c)
        c = (t - s) - (v - c)
        s = t
    return s


print('Kahan sum:\t', float(kahan_sum(arr)))

print('True sum:\t', float(Float8.from_float(sum([float(v) for v in arr]))))


errcnt = 0
for i in range(256):
    a = Float8.from_uint8(i)
    for j in range(256):
        b = Float8.from_uint8(j)
        c = a + b
        d = Float8.from_float(float(a)+float(b))
        errcnt += (float(c) != float(d))
print(errcnt, 'errors detected')

