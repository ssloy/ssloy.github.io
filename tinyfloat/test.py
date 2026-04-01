class Float8:
    def __init__(self, s, e, m):
        self.s, self.e, self.m = s, e, m

    @classmethod
    def from_uint8(cls, uint8):
        s = 1 if uint8<128 else -1
        e = (uint8 % 128) // 16 - 4
        m = (uint8 % 128) %  16
        if e == -4:
            e += 1  # if subnormal, increment the exponent, the hidden bit = 0
        else:
            m += 16 # if normal, recover the hidden bit = 1
        return cls(s, e, m)

    def __float__(self):
        return self.s * self.m * 2**(self.e-4)

    @classmethod
    def from_float(cls, f):
        dist = [ abs(float(Float8.from_uint8(i)) - abs(f)) for i in range(128) ] # distance from |f| to all non-negative Float8
        i = min(range(128), key=lambda j : dist[j])                              # take the (first) closest
        if i < 127 and dist[i] == dist[i+1]:                                     # if tie
            i += i % 2                                                           # round to even
        return Float8.from_uint8(i + (0 if f>=0 else 128))                       # do not forget to recover the sign

    def copy(self):
        return Float8(**self.__dict__)

    def __add__(self, other):
        a, b = self.copy(), other.copy()
        if a.e < b.e:
            a, b = b, a

        a.m *= 8                                 # reserve place for GRS bits
        b.m *= 8
        while a.e > b.e:                         # align exponents
            b.m = (b.m // 2) | (b.m % 2)         # LSB is sticky
            b.e += 1

        sum = Float8(a.s if a.m >= b.m else b.s, # sign
                     a.e,                        # exponent
                     abs(a.s*a.m + b.s*b.m))     # mantissa

        while sum.m < 16*8 and sum.e > -3:       # normalize the result
            sum.m *= 2
            sum.e -= 1

        while sum.m >= 32*8 and sum.e < 3:       # can't be more than one iteration
            sum.m = (sum.m // 2) | (sum.m % 2)   # do not forget the sticky bit
            sum.e += 1

        g = (sum.m // 4) % 2                     # guard bit
        r = (sum.m // 2) % 2                     # round bit
        s =  sum.m % 2                           # sticky bit
        sum.m //= 8

        if g and (r or s or sum.m % 2):          # round-to-nearest, even-on-ties
            sum.m += 1
            if sum.m == 32 and sum.e < 3:        # renormalize if necessary
                sum.m //= 2
                sum.e += 1

        sum.m = min(sum.m, 31)                   # handle overflows (we have no infinities here)
        return sum

    def __sub__(self, other):
        return self + Float8(-other.s, other.e, other.m)



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

