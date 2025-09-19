# Computers and Numbers

## Why Reals Are Hard

Let us talk about numbers and computers.
First of all, there are three most common families of numbers we are dealing with: integer, rational and real numbers.
Computers can manipulate integers perfectly, rationals with effort, and reals only in dreams. Most reals cannot even be named by any algorithm, and the few that can still collapse to approximations when stored in finite memory.
Let me elaborate.

### Integers: computers’ natural language

Computers are digital machines. Inside the hardware, everything is stored in binary: strings of 0s and 1s.
This makes integers (whole numbers) the most natural fit.

A 32-bit register can hold exactly $2^{32}$ different patterns of 0s and 1s; it is common to interpret them as integers from $0$ to $4\ 294\ 967\ 295$ (unsigned), or from $-2\ 147\ 483\ 648$ to $2\ 147\ 483\ 647$ (signed).
Arithmetic on integers (addition, subtraction, multiplication, division) is exact, as long as the result fits within the chosen bit width.
So computers excel at integers: representation is exact, arithmetic is reliable, and all values in the range are covered.

### Rational numbers: manageable with two integers

A rational number is a ratio of two integers, like $\frac34$ or $-\frac{22}7$.
Computers can store these exactly by keeping an integer numerator and denominator.
For example, in Python, the `fractions.Fraction` class does exactly this.
Arithmetic works correctly, but denominators may grow very large, making computations slower.
So, representing rationals is possible and exact, but less efficient.
Computers can handle it, though it is not what hardware is optimized for.

### Real numbers: the impossible dream

Real numbers include all rationals plus all irrationals — like $\sqrt{2}$ and $\pi$.
Most real numbers cannot be described exactly with a finite sequence of digits,
but this infinity is not the biggest problem.
The problem with real numbers is their sheer abundance.
Forget about computers for a moment, let us talk about math on paper.

#### Computable reals: a tiny subset

Let us say that a real number is **computable** if there exists an algorithm that, given $n$, outputs the $n$-th digit of the number.
Examples are numerous, we know formulas to compute digits of $\pi$, $\sqrt 2$, $e$ and many others.
Let us focus on the word **algorithm**.
In our context, an algorithm is a textual description (in fact, a computer program) telling us how to compute the $n$-th digit of some number.
The set of texts (computer programs) is **countable**: there are only finitely many programs of length 1, finitely many of length 2, and so on.

The set of real numbers $\mathbb R$, however, is **uncountable** ([Cantor’s diagonal argument](https://en.wikipedia.org/wiki/Cantor%27s_diagonal_argument)).
Uncountable sets are "bigger" that countable sets, therefore most real numbers cannot even be described by any program — they are **incomputable**.
Although there are infinitely many computable reals, they form a countable set — a drop in the ocean compared to all reals.

#### Storage limits: finite precision

Even for computable numbers, storing them directly is problematic.
A real number may have infinitely many digits, but a computer can only store finitely many bits.
Therefore, even computable real numbers cannot be represented exactly. Approximations are unavoidable.

Putting it together: most real numbers are incomputable — no algorithm can generate them.
Of the computable reals, computers can only hold a finite precision approximation.
This means the “continuum” of real numbers is **forever beyond reach** of finite digital machines.

In practice, numerical computation is built on the illusion of reals: we pretend to work with them (solving equations, integrating, simulating physics),
but everything is grounded in a finite lattice of floating-point approximations.
The success of scientific computing rests on the fact that this illusion is often “good enough” — relative errors are kept small, and algorithms are stable.

## Approximations and errors

So we want to represent real numbers on a computer, but only have a finite number of bit patterns.
Suppose we want to represent numbers between 0 and 16, and we have 7 bits available. This gives us a budget of $2^7 = 128$ distinct numbers.

### Fixed-point numbers

If $m$ is the unsigned integer value of a 7‑bit pattern, then $m$ ranges from 0 to 127.
We can interpret this as the fractional number $m/8$. Let us plot all 128 such numbers:


[![](computers-and-numbers/fixed-point.png)](computers-and-numbers/fixed-point.png)

These numbers are evenly spaced across the range.
They are called **fixed‑point** numbers because the “binary point” (the denominator) stays in the same position for all values.

For example, take $m = 125$. The bit pattern for $m$ is `1111101` (since $125_{10} = 1111101_2$).
Dividing by 8 shifts the binary point three places to the left: $\tfrac{125}{8}_{10} = 1111.101_2$.
The binary point is fixed for all the numbers, hence the name.


### Approximation errors

Fixed-point numbers offer the best possible **absolute error** of approximation.
If the real number is $x$ and the computer stores $\tilde x$, then
$$
\text{absolute error} := |x - \tilde{x}|.
$$


Say, we want to represent the real number $0.1$ with our 7 bit fixed-point numbers.
The closest number we have is $\frac{10}{8} = 0.125$.
Therefore, we commited a 0.025 error.

Often what matters is how big the error is compared to the size of the number.
Let us define the notion of **relative error**:

$$
\text{relative error} := \frac{|x - \tilde{x}|}{|x|}.
$$

Let us illustrate the difference between the two:

* If $x=1000$ and $\tilde x = 1000.1$, then absolute error = 0.1, but relative error = 0.1 / 1000 = 0.0001 (very small, good).
* If $x=0.01$ and $\tilde x = 0.0101$, then absolute error is very small (0.0001), but relative error = 0.0001 / 0.01 = 0.01. That is 1% error, not great.

There are two natural goals that arise when representing real numbers on a computer:

* Cover a huge dynamic range: from tiny numbers like $10^{-30}$ to to huge numbers like $10^{30}$.
* Give decent precision everywhere: the numbers should be relatively close to the true reals.

If we used fixed-point, the numbers are evenly spaced. That’s great for precision but terrible for range: you can’t represent both 
$10^{-30}$ and $10^{30}$ unless you use thousands of bits.

The solution is to use a logarithmic distribution of representable numbers:

[![](computers-and-numbers/ideal-distribution.png)](computers-and-numbers/ideal-distribution.png)

Here the numbers are evenly spaced on a log scale:

[![](computers-and-numbers/ideal-distribution2.png)](computers-and-numbers/ideal-distribution2.png)

This means there are as many numbers between 0.1 and 1 as between 1 and 10.
Thus we achieve uniform relative precision rather than uniform absolute precision.
This matches real‑world needs, where significant digits matter more than absolute spacing.

The more bits available, the larger the range we can cover.
IEEE [single‑precision floating‑point](https://en.wikipedia.org/wiki/Single-precision_floating-point_format) numbers, for example, can go up to about $10^{38}$.

If we again take $m \in [0,127]$, we could define numbers as $2^{-4 + m/16}$ in the $[0,16]$ range — as plotted in the “ideal” graphs above.

??? bug "Spoiler"
    Attentive readers may notice that these numbers do not start from zero — a detail we will address later.


This distribution would be perfect if our only goal was to approximate reals with uniform relative error. Unfortunately, it introduces problems.

For example, suppose we want to add two such numbers. Given $a$ and $b$ representing $2^{-4 + a/16}$ and $2^{-4 + b/16}$, we would need to solve for $c$:
$$
2^{-4 + a/16} + 2^{-4 + b/16} = 2^{-4 + c/16}.
$$
This is a gnarly equation to solve, especially since the exponents are fractional.
Even a simple addition of two numbers kills efficiency.

Moreover, pure log encoding cannot represent integers exactly, except powers of two. Floating‑point formats fix this: they preserve all integers up to a certain size exactly (e.g., all integers up to $2^{24}$ fit in a `float32`). This property is essential in many algorithms (array indexing, loop counters, geometry).

??? tip "Fun fact"
    There are “[logarithmic number systems](https://en.wikipedia.org/wiki/Logarithmic_number_system)” (LNS), used in niche areas like DSP (digital signal processing) and deep learning accelerators. They are great for multiplication/division (turns into add/subtract), but bad for addition. Hardware designs typically combine both worlds.


### Floating point numbers

The idea of floating‑point is to mimic the logarithmic distribution while retaining efficient arithmetic.
A good way to understand floating‑point numbers is to construct them step by step.

In our example, we have a budget of 7 bits total to represent a number.
We will use them to store two integer numbers: $e$ (exponent) and $m$ (mantissa).
It is up to us to decide how many bits we reserve for $e$, so let us say that we use $0 < n_e <7$ bits for the exponent
and $n_m:=7-n_e$ bits for the mantissa.

If we interpret $n_e$ bits as a signed int, then under the [offset binary interpretation](https://en.wikipedia.org/wiki/Signed_number_representations), $e \in [-2^{n_e-1} \dots 2^{n_e-1}-1]$.
If $n_e = 3$, then $e$ can take $2^3=8$ values from $-4$ to $3$.
Let us plot all $8$ values $2^e$ and in addition one more value $2^{2^{n_e-1}}$ (dashed):

[![](computers-and-numbers/anchors.png)](computers-and-numbers/anchors.png)

Python snippet:
```py
n_e = 3
anchors = []
for e in range(-2**(n_e-1), 2**(n_e-1)+1):
    anchors.append(2**e)
```

These anchors divide the range into intervals. With $n_m = 4$, $m$ can take $2^4 = 16$ values.
Within each interval, we evenly place 16 numbers. Thus we have $8 \times 16 = 128$ numbers, exactly fitting into 7 bits.

Here is a bit of python that generates all the numbers:
```py
n_m = 7 - n_e
numbers = []
for i in range(len(anchors)-1): # for each interval
    for m in range(2**n_m):     # populate it with 2**n_m numbers
        v = anchors[i] + m/2**n_m * (anchors[i+1]-anchors[i])
        numbers.append(v)
```

And here is the corresponding plot of the numbers:

[![](computers-and-numbers/floats.png)](computers-and-numbers/floats.png)

Each interval is a linear interpolation between anchors. Inside each interval the binary point is fixed, but it shifts between intervals — hence **floating point**.

One issue remains: the very first anchor is $2^{-2^{n_e-1}}$, so zero is missing.
The common fix is a hack: redefine the first anchor as zero.

```py
anchors = [ 0 ]
for e in range(-2**(n_e-1)+1, 2**(n_e-1)+1):
    anchors.append(2**e)
```

The first interval is now special — its values are called [**subnormals**](https://en.wikipedia.org/wiki/Subnormal_number) (a term we will revisit later).

Here are our 128 floats:

[![](computers-and-numbers/subnormal.png)](computers-and-numbers/subnormal.png)

Because anchors are powers of two, integers can be represented exactly.
As for arithmetic efficiency — that is the focus of this tutorial: how to manipulate floating‑point numbers using only integer operations.

Next time we will talk about printing the decimal value of a float.
Surprisingly enough, this problem is far from being trivial.
It is actually one of the hardest parts of floating-point support in a language runtime.
Stay tuned!

--8<-- "comments.html"

