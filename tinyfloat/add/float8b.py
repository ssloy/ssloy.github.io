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

        while a.e > b.e:                         # align exponents
            b.m //= 2
            b.e += 1

        sum = Float8(a.s if a.m >= b.m else b.s, # sign
                     a.e,                        # exponent
                     abs(a.s*a.m + b.s*b.m))     # mantissa

        while sum.m < 16 and sum.e > -3:         # normalize the result
            sum.m *= 2
            sum.e -= 1

        while sum.m >= 32 and sum.e < 3:         # can't be more than one iteration
            sum.m //= 2
            sum.e += 1

        sum.m = min(sum.m, 31)                   # handle overflows (we have no infinities here)
        return sum

    def __sub__(self, other):
        return self + Float8(-other.s, other.e, other.m)

