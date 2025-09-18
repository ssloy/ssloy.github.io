How should the result of dividing `3.0` by `10.0` be displayed on a screen?
How many digits should be printed if the user has not specified this?

As you might have noticed, I specified the numbers `3.0` and `10.0` in decimal (base 10), because that’s the notation us humans are used to.
The problem, however, is that most decimal fractions do not have an exact binary representation:

$$
0.3_{10} = 0.0100110011001100110011001100\dots_2.
$$

This binary fraction is infinite, the pattern 0011 repeats forever.
So, when we write `x = 0.3`, the variable `x` actually strores the nearest representable floating point number.
For example, in python floating point has double precision (64 bits), so `x` actually stores `0.299999999999999988897769753748434595763683319091796875`.

If we create a second variable `y = 0.1 + 0.2`, it actually stores `0.3000000000000000444089209850062616169452667236328125`.
It is not surprising to see the difference between the two, since we have accumulated three approximation errors for computing `y`: 

1. first, we need to find the closest float to `0.1` (it is `0.1000000000000000055511151231257827021181583404541015625`), 
2. then the closest float to `0.2` (it is `0.200000000000000011102230246251565404236316680908203125`).
3. Finally, the sum introduces its own rounding errors.


How should we print the values of `x` and `y`?
First and foremost, we must guarantee the roundtrip safety.
It means that whatever the decimal string must allow to recover exactly the same binary float we had in memory.

* If the system displays too many digits, the extra digits may be “garbage” that reflects more information than the number actually contains;
* if the system displays too few digits, the result will be incorrect in a stricter sense: when converting the decimal representation back to binary, the original binary value may not be restored.




* When read back, exactly recovers the same binary float.
* But doesn’t show more digits than necessary.








But when we print the value of `x`, we get a simple `0.3` on the screen and not the exact stored value:

The idea is to print just enough digits to identify the stored value.
The correct approach is to print the shortest decimal string that:

* When read back, exactly recovers the same binary float.
* But doesn’t show more digits than necessary.


Let us see an example of why `0.1 + 0.2` is not equal to `0.3`:


```python
from decimal import Decimal
a = 0.1 + 0.2
print(Decimal(a))

b = 0.3
print(Decimal(b))
```





Let us dig in.

A floating-point number is stored in binary, as sign × mantissa × 2^exponent.

Most decimal fractions are not exact in binary.
For example:

0.5 = 1/2 = 0.1₂ → exact in binary.

0.25 = 1/4 = 0.01₂ → exact.

0.1 = 1/10 → binary expansion is infinite:


```py linenums="1" hl_lines="11"
n_e = 3
n_m = 7-n_e

anchors = [ 0 ]
for e in range(-2**(n_e-1)+1, 2**(n_e-1)+1): # prepare 2**n_e intervals
    anchors.append(2**e)

numbers = []
for i in range(len(anchors)-1): # for each interval
    for m in range(2**n_m):     # populate it with 2**n_m numbers
        v = anchors[i] + m/2**n_m * (anchors[i+1]-anchors[i])
        numbers.append(v)
print(numbers)
```

```
[0.0, 0.0078125, 0.015625, 0.0234375, 0.03125, 0.0390625, 0.046875, 0.0546875, 0.0625, 0.0703125, 0.078125, 0.0859375, 0.09375, 0.1015625, 0.109375, 0.1171875, 0.125, 0.1328125, 0.140625, 0.1484375, 0.15625, 0.1640625, 0.171875, 0.1796875, 0.1875, 0.1953125, 0.203125, 0.2109375, 0.21875, 0.2265625, 0.234375, 0.2421875, 0.25, 0.265625, 0.28125, 0.296875, 0.3125, 0.328125, 0.34375, 0.359375, 0.375, 0.390625, 0.40625, 0.421875, 0.4375, 0.453125, 0.46875, 0.484375, 0.5, 0.53125, 0.5625, 0.59375, 0.625, 0.65625, 0.6875, 0.71875, 0.75, 0.78125, 0.8125, 0.84375, 0.875, 0.90625, 0.9375, 0.96875, 1.0, 1.0625, 1.125, 1.1875, 1.25, 1.3125, 1.375, 1.4375, 1.5, 1.5625, 1.625, 1.6875, 1.75, 1.8125, 1.875, 1.9375, 2.0, 2.125, 2.25, 2.375, 2.5, 2.625, 2.75, 2.875, 3.0, 3.125, 3.25, 3.375, 3.5, 3.625, 3.75, 3.875, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5]
```

$$
v_{e,m} = \left\{
\begin{array}{lll}
0 + \frac{m}{2^{n_m}}\left(2^{e+1} - 0\right) & = m \cdot 2^{e+1-n_m} \quad & \text{if}~e= -2^{n_e-1}\\
 2^e + \frac{m}{2^{n_m}}\left(2^{e+1} - 2^e\right) & = (m+2^{n_m}) \cdot 2^{e-n_m}  & \text{otherwise}
\end{array}
\right.
$$

$e\leftarrow e+1$ if subnormal and $m\leftarrow m+2^{n_m}$ if normal

$m$ is not a $n_m$-bit, but $(n_m+1)$-bit unsigned. The 5th bit is not stored explicitly, it is hidden and can be recovered from the value of `e`.

As a side note, it is also means that mantissa $m$ encodes a fixed-point number with 1 bit for the integer part and $2^{n_m}$ bits for the fraction.
Therefore, $\frac m {2^{n_m}} \in [0, 2)$.
Multiplying it by $2^e$ we make the point float by $e$ binary places.


```py linenums="1" hl_lines="5 7"
numbers = []
for e in range(-2**(n_e-1), 2**(n_e-1)):
    for m in range(2**n_m):
        if e == -2**(n_e-1):
            e += 1          # subnormal number
        else:
            m += 2**n_m     # normal number
        v = m * 2**(e-n_m)
        numbers.append(v)
print(numbers)
```

```py linenums="1"
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

print(float(Float7(93)))
```

```
3.625
```

$93_{10} = 101\ 1101_2$

$e = \left\lfloor\frac{93}{16}\right\rfloor-4 = 1$

$m = (93 \mod 16) + 16 = 29$

$29 \cdot 2^{1-4} = 3.625$


It turns out that our float7 can be represented as a fixed-point number with 4 bits in the integer part and 7 bits in the fractional part, which we can summarize as 4.7 format.
We can determine this by noting that a float’s mantissa is a 1.4 fixed-point number.
The maximum float exponent is 3, which is equivalent to shifting the mantissa left 3 positions.
The minimum float exponent is -3, which is equivalent to shifting the mantissa right 3 positions.
Those shift amounts of our 1.4 mantissa mean that all floats can fit into a 4.7 fixed-point number, for a total of 11 bits.

All we need to do is create this number, by pasting the mantissa into the correct location, and then convert the large fixed-point number to decimal.

$$
v = \sum_{i=0}^{10} b_i\ 2^{i-7}
$$


$29_{10} = 11101_2$

0011.1010000



$3.625_{10} =  0011.1010000_2$

primary school - column addition
```
     0.0078125  * 0
   + 0.0156250  * 0
   + 0.0312500  * 0
   + 0.0625000  * 0
   + 0.1250000  * 1
   + 0.2500000  * 0
   + 0.5000000  * 1
   + 1.0000000  * 1
   + 2.0000000  * 1
   + 4.0000000  * 0
     8.0000000  * 0
   = ---------
     3.6250000
```


```py linenums="1" hl_lines="14"
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
        [0,0,0,0,0,0,0,0,0,0,0]  # zero padding to avoid extra logic in line 41
    ]

    def __init__(self, offset, uint5):
        self.number = [ 0 ]*11   # 11-bit number, binary expansion of uint5 * 2**offset
        while uint5 > 0:
            self.number[offset] = uint5 % 2
            uint5 //= 2
            offset += 1

    def __str__(self):
        print(self.number)
        string = ''
        carry = 0
        for position in range(9):             # loop from the least significant digit to the most significant
            total = sum(bit * dgt for bit, dgt in zip(self.number, self.digits[position])) # sum of 11 digits
            digit = str((total + carry) % 10) # current digit to output
            carry = (total + carry)//10
            string = digit + string
            if position==6:                   # decimal dot position
                string = '.' + string
        return string
print(Float7(93))
```

```
03.6250000
```


