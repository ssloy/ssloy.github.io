n_e = 3
n_m = 7-n_e

anchors = [ 0 ]
for e in range(-2**(n_e-1)+1, 2**(n_e-1)+1):
    anchors.append(2**e)

numbers = []
for i in range(len(anchors)-1): # for each interval
    for m in range(2**n_m):     # populate it with 2**n_m numbers
        v = anchors[i] + m/2**n_m * (anchors[i+1]-anchors[i])
        numbers.append(v)

print(anchors)
print(numbers)

for i in range(len(anchors)-1): # for each interval
     print((anchors[i+1]-anchors[i])/16)

numbers = []
for e in range(-2**(n_e-1), 2**(n_e-1)):
    for m in range(2**n_m):
        if e == -2**(n_e-1):
            e += 1
        else:
            m += 2**n_m
        v = m * 2**(e-n_m)
        numbers.append(v)

print(numbers)

#a, b = -2**(n_e-1)+1-n_m, 2**(n_e-1)-1
#print(a,b)
#for e in range(a,b+1):
#    print(2**e)

class Float7:
    def __init__(self, uint7):
        self.e = uint7 // 16 - 4
        self.m = uint7 %  16
        if self.e == -4:
            self.e += 1  # if subnormal, increment the exponent, the hidden bit = 0
        else:
            self.m += 16 # if normal, recover the hidden bit = 1

    def __float__(self):
        return self.m * 2**(self.e-4)

    def __str__(self):
        return str(Fx4_7(self.e + 3, self.m))

class Fx4_7:  # 11-bit number with 4 bits in the integer part and 7 in the fraction
    digits = [
        [5,0,0,0,0,0,0,0,0,0,0], # constant array, 11 powers of 2 in base 10
        [2,5,0,0,0,0,0,0,0,0,0],
        [1,2,5,0,0,0,0,0,0,0,0],
        [8,6,2,5,0,0,0,0,0,0,0],
        [7,5,1,2,5,0,0,0,0,0,0],
        [0,1,3,6,2,5,0,0,0,0,0],
        [0,0,0,0,1,2,5,0,0,0,0], # the decimal dot is here
        [0,0,0,0,0,0,0,1,2,4,8],
        [0,0,0,0,0,0,0,0,0,0,0]  # zero padding to avoid extra logic
    ]

    def __init__(self, offset, uint5):
        self.number = [ 0 ]*11 # 11-bit number, binary expansion of uint5 * 2**offset
        while uint5 > 0:
            self.number[offset] = uint5 % 2
            uint5 //= 2
            offset += 1

    def __str__(self):
        print(self.number)
        string = ''
        carry = 0
        for position in range(9): # loop from the least significant digit to the most significant
            total = sum(bit * dgt for bit, dgt in zip(self.number, self.digits[position])) # sum of 11 digits
            digit = str((total + carry) % 10) # current digit to output
            carry = (total + carry)//10
            string = digit + string
            if position==6:
                string = '.' + string
        return string

print(float(Float7(93)))
print(Float7(93))



'''
def float2str(x):
    result = '' if x>0 else '-'
    x = abs(x)
    result += str(int(x)) + '.'
    x -= int(x)

    while x>0:
        x *= 10
        result += str(int(x))
        x -= int(x)
    return result

import math
def float2str2(x):
    result = '' if x>0 else '-'
    x = abs(x)

    i = ''
    while x>=1:
        d = int(math.fmod(x, 10))
        i = str(d) + i
        x -= d
        x /= 10

    result += i + '.'

    while x>0:
        x *= 10
        result += str(int(x))
        x -= int(x)
    return result





for i in range(128):
    print(float(Float7(i)))

print()

for i in range(128):
    print(float(Float7(i))-float(str(Float7(i))))

#print([float(Float7(i)) for i in range(128)])
#print([str(Float7(i)) for i in range(128)])

#for i in range(128):
#    print(float2str(float(Float7(i))))

import numpy as np
import sys
import math

print(float2str2(math.ulp(0.0) ))
print(math.ulp(0.0) )
print(float2str2(sys.float_info.max ))
print(sys.float_info.max )

print(float2str(-np.pi ))
print(float2str2(-np.pi ))



'''

