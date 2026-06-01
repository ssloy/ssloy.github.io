from float8c import *

a = Float8.from_float(4.25)
b = Float8.from_float(5.25)

print(a.e, a.m)
print(b.e, b.m)

print(float(a+b))

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

#for i in range(128):
#    print(i, float(Float8.from_uint8(i)))

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
