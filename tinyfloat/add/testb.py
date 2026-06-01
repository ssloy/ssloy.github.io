from float8c import *

r = Float8.from_float(7) + \
    Float8.from_float(0.875)
t = Float8.from_float(7 + 0.875)
print(f'The sum is {r.m}*2**({r.e}-4) = {float(r)}, expected {float(t)}')

