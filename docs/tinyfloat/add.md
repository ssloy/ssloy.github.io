---
title: Addition and errors
---

# Addition and numerical errors

Let us continue discussing the most unoptimized 32-bit software floating-point library [TinyFloat](https://github.com/ssloy/tinyfloat).
The library is written in C++ and deliberately avoids built-in floating-point types, relying solely on 32-bit integers.
The intention is to make the code as readable as possible — no bit-hacks, no clever tricks.

Moreover, I want an extensive documentation on what is happening under the hood.
Turns out, the best way to document the C++ code is to make a full rewrite in Python :)

In this writing, I use 8-bit floating point, and ignore special values (`NaN`, `Inf`).
I rely on Python’s native float only for testing the implementation.

From now on, we work with signed floating point numbers, so I add the last bit we need to get a `Float8` class.
If you have read previous two chapters, you know that this class has integer `e` and `m` members (standing for exponent and mantissa).
Here I add `s` member that can take either `1` or `-1` value.
This $(s,e,m)$ triplet represents the real number that can be written in scientific notation $s\cdot  m \cdot 2^{e-4}$, check line 17 of the following listing:

??? example "float8.py"
    ```py linenums="1" hl_lines="20-25"
    --8<-- "add/float8a.py"
    ```

Note that `Float8` stores the normalized exponent and mantissa: the hidden bit is restored and denormals are converted into normalized form (lines 10-13).

Thus,

* $s \in \{-1, 1\}$,
* $e \in [-3\dots 3]$,
* $m\in[0\dots 31]$,

and the triplet encodes the number $s\cdot  m \cdot 2^{e-4}$ without any remaining special-case logic.


## Rounding

The IEEE754 standard defines a number of rounding modes, but the default rounding mode is the *round-to-nearest-even-on-ties* (RNE) mode.
Here is an illustration of RNE rounding mode with our 8-bit floating point representation:

![](add/rounding.svg)

The real number 4.65 is closest to the `Float8` value 4.75,
But 4.875 lies exactly halfway between 4.75 and 5.0; in this case RNE requires rounding to the even of the two representable values.
Since the bit pattern of 5.0 (`0b01100100`) is even as an integer, 4.875 rounds to 5.0.
Similarly, the real number 5.125 rounds to 5.0 and 5.375 rounds to 5.5.

In the above snippet, `from_float()` function takes a python `float` and rounds it up to our `Float8` using RNE mode.
The implementation is simple: compute the distance from the real number to all `Float8` values (line 21), identify the closest candidate(s), and apply the RNE tiebreaker.

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
if the fractional part > 0.5 OR
   the fractional part = 0.5 AND the integer part is odd:
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

As we have just witnessed, the result of arithmetic operations in floating point experiences rounding error when it cannot be exactly represented.
While modern hardware and libraries produce correctly rounded results for arithmetic operations,
this rounding error can get amplified with a series of operations because the intermediate result must be rounded.
When working with finite precision, numerical errors should be carefully addressed.

### Catastrophic cancellation


Imagine you are measuring how much gasoline you use on two identical road trips.

* On the first trip, the car uses $30.2$ liters (your gas pump only shows one decimal place, $\pm 0.1\ L$).
* On the second trip, after a minor tune-up, you use $30.0$ liters (again, $\pm 0.1\ L$ precision).

You want to figure out how much less gasoline you used after the tune-up:

$$
\text{Fuel saved} = 30.2\ L - 30.0\ L = 0.2\ L
$$

But with the pump’s limited precision, each measurement could be off by $\pm 0.1\ L$, so the actual amounts used could have been anywhere from:

* First trip: $30.1 - 30.3\ L$
* Second trip: $29.9 - 30.1\ L$

So the difference (the savings) could be anywhere from $0.0\ L$ ($30.1 - 30.1$) up to $0.4\ L$ ($30.3 – 29.9$)!
Your relative error is huge compared to the “saving” you measured.
Even though your original measurements looked precise to $0.1\ L$, subtracting nearly equal numbers (to get the savings) made your result mostly just noise.

This is catastrophic cancellation: when you subtract nearly equal values, whatever error or uncertainty was in each gets blown up in your small result, regardless of using computers or physical tools.

The problem is NOT because of "floating point", but because you lost accuracy by subtracting two almost equal measurements.
Catastrophic cancellation can happen in **any system with limited precision** (physical measurements, financial calculations with limited decimal places, etc.).

Now, let's see how a similar effect happens in floating point computations, and how it can be even worse when the numbers are truncated or rounded first.
The difference of two squares $a^2 − b^2$ seems innocuous,
but when the two terms are close, catastrophic cancellation occurs.
Usually it happens in a subtraction on previously truncated operands, for instance, the product of other operands (here, squares).

Let us consider $a = 2.875$ and $b = 2.75$.
It is easy to compute the true difference of squares $a^2 - b^2 = 0.703125$.

Note that both $a$ and $b$ are **exactly** representable in `Float8`.
If, however, we compute $a^2-b^2$ in our `Float8` representation, we will get obtain $1.0$ as the result.
The nearest `Float8` to $a^2$ is $8.5$, and $b^2$ is rounded to $7.5$.

$$
\begin{alignat}{2}
2.875^2 &= 8.265625 & \approx 8.5 \\
2.75^2  &= 7.5625   & \approx 7.5
\end{alignat}
$$

Subtracting the two, we get $1.0$. The relative error of our result is $42\%$!

$$
\frac{|1 - 0.703125|}{|0.703125|} \approx 0.42.
$$

There is no general, systematic method to completely avoid catastrophic cancellation or to reliably predict exactly how many digits of accuracy have been lost in a given computation.
However, we can mitigate its effects by carefully designing numerically stable algorithms and reformulating calculations to minimize the subtraction of nearly equal quantities.
For our difference of squares, the best solution is to use a factorized formulation of the computation $a^2 - b^2 = (a+b)(a-b)$.

For our example, the difference $2.875 - 2.75$ can be computed exactly in our `Float8`, and the sum $2.875 + 2.75$ is rounded to $5.5$:

$$
\begin{alignat}{2}
2.875 + 2.75 &= 5.625 & \approx 5.5 \\
2.875 - 2.75  &= 0.125. &
\end{alignat}
$$

Then the product $5.5 \cdot 0.125 = 0.6875$, which is again exactly computable in our `Float8` representation, has only $2\%$ of relative error:

$$
\frac{|0.6875 - 0.703125|}{|0.703125|} \approx 0.02.
$$

$2\%$ of error is much better than $42\%$ we had before!


### Summation

Well, okay, subtraction is tricky, but if we add positive numbers nothing can go wrong.
Say, if I sum $128$ times $\frac{1}{128}$, I'll get $1$, right? Am I right?


Note that $1/128$ can be represented exactly in `Float8`, so when I write `Float8.from_float(1/128)`, there is no loss of information.
Let us test the summation. I start with the accumulator variable `total` initialized to $0$, and add $128$ times $0.0078125$.

```python
from float8 import *

total = Float8.from_float(0)
for _ in range(128):
    total += Float8.from_float(1/128)
print(float(total))
```

AAaaand here is the result!

```
0.25
```

It is important to understand why it is happening, so let us add $0.25$ and $0.0078125$ by hand.
First of all, let us find their mantissas and exponents:

$$
\begin{align}
0.25 &= 16 \cdot 2^{-2-4}\\
0.0078125  &= 1\cdot 2^{-3-4}
\end{align}
$$

We need to align the mantissas:

$$
0.0078125 = 0.5 \cdot 2^{-2-4}
$$

Finally, we sum the mantissas and round them using the RNE rule:

$$
0.25 + 0.0078125 = (16 + 0.5) \cdot 2^{-2-4} \approx 16 \cdot 2^{-2-4}.
$$

In other words, in `Float8` representation, `0.25 + 0.0078125 = 0.25`.

When you add two numbers with very different magnitudes, the smaller number may be ignored or “lost” due to limited precision, resulting in a loss of accuracy.
This is because the significant digits of the smaller number may not fit within the precision allowed when combined with the much larger number.

This is a particular problem in the straightforward (sequential) way of summing a list.
Pairwise summation is a numerically stable technique that helps reduce this error.
Instead of adding numbers in a sequence, you recursively sum pairs of numbers, then pairs of those sums, and so on, like a binary tree.
By always adding numbers of similar size first, pairwise summation keeps as many significant digits as possible, making the final result more accurate than simple sequential addition.

Let us illustrate the idea with working code.
Here I define two function returning the sum of an array. The first one is the naive, sequential implementation, and the other one implements the binary tree idea:

```python
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
```

And now let us invoke both of them on our test data:

```python
arr = [ Float8.from_float(1/128) ] * 128

print('naive sum:\t',    float(   naive_sum(arr)))
print('pairwise sum:\t', float(pairwise_sum(arr)))
```

Pairwise summation greatly improves the result:

```
naive sum:       0.25
pairwise sum:    1.0
```

While pairwise summation reduces rounding errors when adding large sequences of numbers, there are even more refined methods, such as Kahan summation, that go a step further.
Kahan summation keeps track of small errors that are typically lost in standard addition.
By maintaining a compensation variable for lost low-order bits, it ensures that even subtle contributions from tiny numbers aren’t “forgotten.”
This makes Kahan’s algorithm especially valuable in situations requiring high precision over long sequences of additions.

Moreover, pairwise summation  typically requires knowing all the values in advance, making it ideal for **offline** summation when the complete list is available.
However, in many practical scenarios, we need to sum values as they arrive, one by one, this is known as **online** summation.
For such cases, Kahan summation is especially effective.

Here is an implementation:

```python
def kahan_sum(arr):
    s, c = Float8.from_float(0), Float8.from_float(0)
    for v in arr:
        t = s + (v - c)
        c = (t - s) - (v - c)
        s = t
    return s
```

Variable `s` is the accumulator, while `c` is the compensation variable.
The useful obervation to make is that we can approximate the inaccuracy of `s` is it changes from iteration to iteration.
To do so, consider the expression

$$
((a+b)-a)-b.
$$

Algebraically, this expression equals zero. Numerically, however, this may not be the case.
In particular, the sum $a+b$ may be rounded to floating-point precision. Subtracting $a$ and $b$ one at a time then yields an approximation of the error of approximating $a+b$.
Removing $a$ and $b$ from $a+b$ intuitively transitions *from* large orders of magnitude *to* smaller ones rather than vice versa and hence is less likely oto induce rounding error
than evaluating the sum $a+b$; this observation explains why the error estimate is not itself as prone to rounding issues as the original operation.

Let us confront all the implementations on more real world-like data.
Here I want to sum $128$ random numbers from the range $(-0.25, 0.25)$:

```python
import random
random.seed(1)
arr = [ Float8.from_float(random.uniform(-0.25, .25)) for _ in range(128) ]

print('naive sum:\t',    float(   naive_sum(arr)))
print('pairwise sum:\t', float(pairwise_sum(arr)))
print('Kahan sum:\t',    float(   kahan_sum(arr)))
print('True sum:\t',     float(Float8.from_float(sum([float(v) for v in arr]))))
```

And here are the results:

```python
naive sum:       0.1875
pairwise sum:    -0.03125
Kahan sum:       0.015625
True sum:        0.015625
```
As expected, naïve sum is way off the true result, pairwise summation gives a reasonable approximation, and Kahan summation is the best.

## Conclusion

Floating-point addition is deceptively subtle.
Even though the mathematical operation is simple, implementing it correctly requires careful attention to the details.

Limited precision is not a flaw, it is a fundamental constraint of representing infinitely many real numbers with finitely many bits.
What does matter is understanding where errors arise and how to mitigate them:

* rewrite expressions to improve numerical stability,
* avoid subtracting nearly equal numbers,
* use pairwise or Kahan summation when combining long lists of values.

With these tools, even a tiny 8-bit floating-point format can behave predictably and transparently, helping reveal the structure of real floating-point hardware and the numerical algorithms it enables.


--8<-- "comments.html"
