---
title: Addition
---

# Addition and numerical errors

Let us continue talking about the most unoptimized 32-bit software floating point library [TinyFloat](https://github.com/ssloy/tinyfloat).
The library itself is written in C++ and does not use any data types besides 32 bit integers.
The idea is to have the most readable code possible, so no bit hacking and other clever tricks.
Moreover, I want an extensive documentation on what is happening under the hood.
Turns out, the best way to document the C++ code is to make a full rewrite in Python :)

In this writing, I use 8-bit floating point, ignoring edge cases such as `NaN` and `Inf`,
which allows me to give simpler examples and more graphics illustrations.
In addition to that, in the Python implementation I use native `float` type to test my code.

From now on, we will be working with signed floating point numbers, so I add the last bit we need to get a `Float8` class.
If you have read previous two chapters, you know that this class has integer `e` and `m` members (standing for exponent and mantissa).
Here I add `s` member that can take either `1` or `-1` value.
This $(s,e,m)$ triplet represents the real number that can be written in scientific notation $s\cdot  m \cdot 2^{e-4}$, check line 17 of the following listing:

??? example "float8.py"
    ```py linenums="1" hl_lines="20-25"
    --8<-- "add/float8a.py"
    ```

Note that `Float8` stores exponent $e$ and mantissa $m$ after recovering the hidden bit and correcting for the denormalized numbers (lines 10-13), i.e. 
 $e \in [-3\dots 3]$ and $m\in[0\dots 31]$.
Therefore, I do not have any edge cases to handle and can safely say that  the  $(s,e,m)$ triplet  encodes the number $s\cdot  m \cdot 2^{e-4}$.


## Rounding

The IEEE754 standard defines a number of rounding modes, but the default rounding mode is the *round-to-nearest-even-on-ties* (RNE) mode.
Here is an illustration of RNE rounding mode with our 8-bit floating point representation:

![](add/rounding.svg)

The real number 4.65 is rounded to its only nearest `Float8` neighbor 4.75,
however there are two nearest `Float8` values (4.75 and 5.0) equidistant to the real number 4.875.
In this case, RNE mode specifies that 4.875 should round to 5.0 because the bit representation of 5.0 (`0b01100100`) is an even number when interpreted as an integer.
Similarly, the real number 5.125 rounds to 5.0 and 5.375 rounds to 5.5.

In the above snippet, `from_float()` function takes a python `float` and rounds it up to our `Float8` using RNE mode.
The idea is extremely simple: first I compute the distance from the input `float` to all possible `Float8` (line 21).
Then in this distance array there will be either one or two minimum values.
If there is one, then I return the corresponding `Float8`, otherwise (if the `float` is equidistant from two `Float8`), I check the parity of the index in the distance array.

## Naïve addition

Let us see the general idea behind floating point addition.
I want to sum two positive numbers $a$ and $b$, represented by their integer mantissas $a_m, b_m$ and exponents $a_e, b_e$:

$$
\begin{align}
a &= a_m \cdot 2^{a_e - 4}\\
b &= b_m \cdot 2^{b_e - 4}
\end{align}
$$

Here is a naïve implementation (lines 30-52):

??? example "Naïve addition implementation"
    ```py linenums="1" hl_lines="30-52"
    --8<-- "add/float8b.py"
    ```

By "naïve" I mean that for a moment I ignore the correct rounding of the result.
Summing two numbers in scientific notation is not that hard, let us split it into two cases:

### Equal exponents: $a_e = b_e$

If the exponents are equal, then we can add the mantissas directly to compute the sum:

$$
a + b = a_m \cdot 2^{a_e - 4} + b_m \cdot 2^{b_e - 4} = (a_m + b_m) \cdot 2^{a_e - 4}.
$$

Let us consider an example of $a=4.25$ and $b=5.25$.
In this case, $a_e = b_e = 2$, $a_m = 17$ and $b_m = 21$:

$$
\begin{align}
a &= 4.25 = 17 \cdot 2^{2-4}\\
b &= 5.25 = 21 \cdot 2^{2-4}
\end{align}
$$

Then the sum can be represented by the exponent $2$ and the mantissa $17+21 = 38$:

$$
a+b = (17+21) \cdot 2^{2-4} = 9.5.
$$

While it is really simple, we need to pay a bit of attention.
Indeed the sum $a+b$ can be represented by the exponent $a_e$ and the mantissa $a_m+b_m$, but there is a catch.
To be stored back into `Float8`, the resulting mantissa must fit into the $[0\dots 31]$ range, and 38 exceeds 31.

That is not a problem: we can divide the mantissa by 2 and increment the exponent.
This process is called normalization, check the lines 43-49 of the previous listing.

$$
9.5 = 38\cdot 2^{2-4} = 19 \cdot 2^{3-4}.
$$

Here the sum is represented by the mantissa $19$ and exponent $3$.
Let us test our implementation:

```python
from float8 import *

r = Float8.from_float(4.25) + \
    Float8.from_float(5.25)
t = Float8.from_float(4.25 + 5.25)
print(f'The sum is {r.m}*2**({r.e}-4) = {float(r)}, expected {float(t)}')
```

Note that here I assess the correctness of the result by computing the sum with native `float` and casting it to `Float8`.
In this case, we get the correct result:

```
The sum is 19*2**(3-4) = 9.5, expected 9.5
```

??? tip "Spoiler alert"
    Do not forget that exponent must also fit into $[-3\dots 3]$ range.
    Whenever it exceeds the maximum value, IEEE754 standard tells that the result is the special value `Inf`.
    [TinyFloat](https://github.com/ssloy/tinyfloat) handles infinities correclty, but in this python implementation
    I round to the maximum representable float, i.e. $15.5$ (line 51 in the listing).

There is one more catch to handle, let us try to add $4.5$ and $5.25$:

```python
from float8 import *

r = Float8.from_float(4.5) + \
    Float8.from_float(5.25)
t = Float8.from_float(4.5 + 5.25)
print(f'The sum is {r.m}*2**({r.e}-4) = {float(r)}, expected {float(t)}')
```

As you can see, our naïve addition differs from the ground truth:

```
The sum is 19*2**(3-4) = 9.5, expected 10.0
```

Let us inspect closely what is happening.
First of all, note that the true result $9.75$ is not exactly representable in our `Float8`, therefore we need to round the sum.
Prior to the resulting normalization, the mantissa of the sum was $18+21 = 39$, and the exponent was $2$:

$$
\begin{align}
a = 4.5 & = 18 \cdot 2^{2-4}\\
b = 5.25 & = 21 \cdot 2^{2-4}\\
a + b & = 39 \cdot 2^{2-4}
\end{align}
$$

The normalization halves the mantissa and increments the exponent:

$$
a + b  = 39 \cdot 2^{2-4} =  \frac{39}{2} \cdot 2^{3-4}
$$

Since the mantissa must be integer, our naïve implementation truncates $\frac{39}2 = 19.5$ to $19$, effectively loosing one bit of precision.
Under RNE rules, $19.5$ ought to be rounded to $20$.
I'll postpone the rounding discussion for a moment, but remember that normalization can lead to the loss of one bit of information.

### Different exponents: $a_e>b_e$

If the exponents $a_e$ and $b_e$ differ, we can suppose that $a_e>b_e$, otherwise we simply swap the numbers, check lines 32-33 in the listing.
That being said, we can align the exponents:

$$
b = b_m \cdot 2^{b_e - 4} = \frac{b_m}{2^{a_e - b_e}} \cdot 2^{b_e - 4 + (a_e - b_e)} = \frac{b_m}{2^{a_e - b_e}} \cdot 2^{a_e - 4}.
$$

Once the alignment is made, we can compute the sum just as before by simply adding the (integer) mantissas!

$$
a + b = \left(a_m + \frac{b_m}{2^{a_e - b_e}}\right) \cdot 2^{a_e - 4}.
$$

This alignment is made in lines 35-37 of the above listing.
Note that this procedure is very similar to the normalization (lines 47-49), therefore it has exactly the same rounding problem.
If $\frac{b_m}{2^{a_e - b_e}}$ is integer, then alignment does not introduce any data loss.
If, however, it is not integer, we need to do some additional work to correctly round the result.

Here's a quick question for you: why do we shift $b_m$ right instead of shifting $a_m$ left?
Theoretically, both would result in aligned exponents.

??? question "Spoiler Alert!"
    Left-shifting a large mantissa can easily cause mantissa overflow before addition.
    Right-shifting the mantissa never increases magnitude; it only reduces precision safely.
    Therefore, by right-shifting $b_m$ we lose tiny, insignificant bits (that we will recover shortly), whereas left-shifting
    would cause the loss of *important* high bits.

## Guard, round and sticky bits: correct rounding

In our naïve implementation we have two moments that can potentially lead to incorrect final rounding in a sum:

* halving the mantissa during alignment of exponents
* and halving the mantissa during the normalization.

Floating point addition uses extra bits (to the “right” of the mantissa) during the computation.
As the mantissa shifts off the end, it shifts into these bits.
It turns out that three bits suffice for the correct rounding, but we will get to it later.

Let us compute by hand $7 + 0.875$, while paying close attention to this problem:

$$
\begin{alignat}{2}
a & = 7     & = 28 \cdot 2^{2-4} \\
b & =0.875 & = 14 \cdot 2^{0-4}
\end{alignat}
$$

The exponents differ, $a_e > b_e$, so we need to align them:

$$
b = 14 \cdot 2^{0-4} = 3.5 \cdot 2^{2-4}.
$$

In the naïve implementation we truncated 3.5 down to 3, thus introducing an error.
This time, we keep the fractional part of the mantissa.
Having the exponents aligned, we can simply add the mantissas:

$$
a + b = (28 + 3.5) \cdot 2^{2-4} = 31.5 \cdot 2^{2-4}
$$

Note that we do not enter a vicious cycle here: the addition 28 + 3.5 does not need floating point math, it is made with integers (i.e. in fixed-point representation, since three extra bits suffice for the rounding).
Now we need to perform the normalization, since $31.5$ exceeds $31$:

$$
a + b = 15.75 \cdot 2^{3-4}.
$$

Now we need to correctly round the mantissa following the *round-to-nearest-even-on-ties* rule.
The decision is simple to make:

```
if the fractional part > 0.5:
    round the mantissa up
if the fractional part < 0.5:
    truncate the mantissa down
if the fractional part = 0.5:
    if the integer part is odd:
        round the mantissa up
    otherwise:
        truncate the mantissa down
```

Since $0.75 > 0.5$, we can safely conclude that

$$
a + b = 15.75 \cdot 2^{3-4} \approx 16 \cdot 2^{3-4}.
$$

Congratulations, the nearest `Float8` to the true sum $7.875$ is $8$!

Here is the correct implementation of the addition, I have highlighted the modifications:

??? example "Correct addition"
    ```py linenums="1" hl_lines="35-36 38 50 53-56 58-62"
    --8<-- "add/float8c.py"
    ```

I reserved three extra bits of precision in lines 35-36.
In lines 53-56 I recover the integer and the fractional part of the mantissa.
Finally, the RNE rule is applied in lines 58-62.

Let us try the code on the above example:

```python
from float8 import *

r = Float8.from_float(7) + \
    Float8.from_float(0.875)
t = Float8.from_float(7 + 0.875)
print(f'The sum is {r.m}*2**({r.e}-4) = {float(r)}, expected {float(t)}')
```

The result is indeed 8.0, just as expected:

```
The sum is 16*2**(3-4) = 8.0, expected 8.0
```

The extra three bits I have allocated are called GRS bits (guard, round and sticky).
Three bits are sufficient to guarantee the correct RNE rounding for all sizes of floats, including 32-bit.

### Homework assignment #1

Find an example where we would need all three bits to decide the rounding.
Note that we did not use the LSB (the sticky one) in the above example.
??? question "Spoiler alert"
    You'd need for the normalization phase to shift the mantissa *left* and not right.

### Homework assignment #2

Show that three bits are sufficient for the rounding on one condition: the sticky bit is indeed **sticky**.

As the mantissa shifts off the end, it shifts into GRS bits.
This works basically like a normal shift right, with the exception that the moment that **any** 1 bit get shifted into the sticky bit, it stays 1 from that point on (that’s what makes it sticky).

Check line 38 (also line 50) of the listing:
```python
            b.m = (b.m // 2) | (b.m % 2)         # LSB is sticky
```
The mantissa is shifted right, but once the least significant bit is set, it remains set forever.
??? question "Spoiler alert"
    Alignment of exponents may require more than 3 shifts, so we cannot store all the bits going off the mantissa into GRS bits.
    Nevertheless, the sticky behaviour is sufficient for the final rounding tiebreaker.



## Numerical errors

The result of arithmetic operations in floating point experiences rounding error when it cannot be exactly represented.
While modern hardware and libraries produce correctly rounded results for arithmetic operations,
this rounding error can get amplified with a series of operations because the intermediate result must be rounded.
When working with finite precision, numerical errors should be carefully addressed.

### Catastrophic cancellation

### Summation


--8<-- "comments.html"
