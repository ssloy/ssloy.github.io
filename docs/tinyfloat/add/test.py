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

'''
for i in range(128):
    print(i, float(Float8.from_uint8(i)))
'''


'''

a = Float8.from_float(2.875)
b = Float8.from_float(2.75)
fa = float(a)
fb = float(b)

print(float(Float8.from_float(float(a+b))), float(Float8.from_float(float(a-b))))




print(float(Float8.from_float(fa**2)), float(Float8.from_float(fb**2)))

r1 = float(Float8.from_float(fa**2) - Float8.from_float(fb**2))
r2 = float(Float8.from_float(float(a+b)*float(a-b)))
t = fa**2 - fb**2

print(r1, r2, t)
print(abs(r1-t)/abs(t), abs(r2-t)/abs(t))
'''


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

print(Float8.from_float(1/4).e, Float8.from_float(1/4).m)
print(Float8.from_float(1/128).e, Float8.from_float(1/128).m)

total = Float8.from_float(0)
for _ in range(128):
    total += Float8.from_float(1/128)
print(float(total))



arr = [ Float8.from_float(1/128) for _ in range(128) ]

arr = [ Float8.from_float(1/128) ] * 128

#import random
#random.seed(1)
#arr = [ Float8.from_float(random.uniform(-0.25, .25)) for _ in range(128) ]
print(([float(v) for v in arr]))



def naive_sum(arr):
    s = Float8.from_float(0.)
    for v in arr:
        s += v
    return s


def pairwise_sum(arr):
    match len(arr):
        case 0:
            return Float8.from_float(0)
        case 1:
            return arr[0]
    mid = len(arr)//2
    return pairwise_sum(arr[:mid]) + \
           pairwise_sum(arr[mid:])


def kahan_sum(arr):
    s, c = Float8.from_float(0), Float8.from_float(0)
    for v in arr:
        t = s + (v - c)
        c = (t - s) - (v - c)
        s = t
    return s


import random
random.seed(1)
arr = [ Float8.from_float(random.uniform(-0.25, .25)) for _ in range(128) ]

print('naive sum:\t',    float(   naive_sum(arr)))
print('pairwise sum:\t', float(pairwise_sum(arr)))
print('Kahan sum:\t',    float(   kahan_sum(arr)))
print('True sum:\t',     float(Float8.from_float(sum([float(v) for v in arr]))))

'''


errcnt = 0
for i in range(256):
    a = Float8.from_uint8(i)
    for j in range(256):
        b = Float8.from_uint8(j)
        c = a + b
        d = Float8.from_float(float(a)+float(b))
        errcnt += (float(c) != float(d))
print(errcnt, 'errors detected')

'''
