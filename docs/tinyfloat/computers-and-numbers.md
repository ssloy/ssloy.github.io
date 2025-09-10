# Computers and numbers

## Why reals are hard

Let us talk about numbers and computers.
First of all, there are three most common families of numbers we are dealing with: integer, rational and real numbers.
Let us check how well computers can handle them.

### Integers: computers’ natural language

Computers are digital machines. Inside the hardware, everything is stored in binary: strings of 0s and 1s.
This makes integers (whole numbers) the most natural fit.

A 32-bit register can hold exactly $2^{32}$ different patterns of 0s and 1s; it is common to interpret them as integers from $0$ to $4\ 294\ 967\ 295$ (unsigned), or from $-2\ 147\ 483\ 648$ to $2\ 147\ 483\ 647$ (signed).
Arithmetic on integers (addition, subtraction, multiplication, division) is exact, as long as the result fits in the chosen bit width.
So computers are great at integers: representation is exact, arithmetic is reliable, and all values in the range are covered.

### Rational numbers: manageable with two integers

A rational number is a ratio of two integers, like $\frac34$ or $-\frac{22}7$.
Computers can store this exactly by keeping an integer numerator and integer denominator.
This is sometimes called a fractional representation.
For example, in Python, the `fractions.Fraction` class does exactly this.
Arithmetic works, but denominators may grow very large, making computations slower.
So, representing rationals is possible and exact, but less efficient.
Computers can handle it, though it is not what hardware is optimized for.

### Real numbers: the impossible dream

Real numbers include all rationals plus all irrationals—like $\sqrt{2}$ and $\pi$.
Most real numbers cannot be described exactly with a finite sequence of digits, but even that is not the biggest problem.
The real problem is that there are **a lot of real numbers**.
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

Even for computable numbers, if we want to store the number itself, and not just the algorithm to compute it, we have a problem.
A real number may have infinitely many digits, while computers can only store finitely many bits at once.
Therefore, computers cannot represent even computable real numbers exactly, we need some sort of approximation.

Putting it together: most real numbers are incomputable — no algorithm can generate them.
Of the computable reals, computers can only hold a finite precision approximation.
This means the “continuum” of real numbers is **forever beyond reach** of finite digital machines.

In practice, numerical computation is built on the illusion of reals: we pretend to work with reals (solving equations, integrating, simulating physics),
but everything is grounded in a finite lattice of floating-point approximations.
The success of scientific computing rests on the fact that this illusion is often “good enough” — relative errors are kept small, and algorithms are stable.

## Approximations and errors

So we want to represent real numbers on a computer, but only have a finite number of bit patterns.
Suppose we want to represent numbers between 0 and 16, and we have 7 bits to represent any number, therefore we have a budget of $2^7 = 128$ numbers in total.

### Fixed-point numbers

If $m$ is the unsigned int interpretation of a 7-bit pattern, $m$ varies from 0 to 127.
This unsigned int can be used to represent the fractional number $\frac m8$, let us plot all 128 of them:

[![](computers-and-numbers/fixed-point.png)](computers-and-numbers/fixed-point.png)

In fact, we have evenly distributed 128 numbers across the range.
These rational numbers $\frac m8$ are called fixed-point because the denominator stays the same for all the range.
Let us consider, say, $m=125$. The bit pattern for m is `1111101`, since $125_{10} = 1111101_2$.
Dividing by 8 corresponds to shifting the binary point three times to the left, therefore $\frac{125}{8}_{10} = 1111.101_2$.
The position of the point is the same for all the numbers we represent, hence **fixed point** representation.

125/8 = 15.625
1111101

, and since 8 is a power of 2,
we have used 


Two natural goals:

    Cover a huge dynamic range: from tiny numbers like 10−3010−30 to huge numbers like 10301030.

    Give decent precision everywhere: the numbers should be relatively close to the true reals.

If we used fixed-point, the numbers are evenly spaced. That’s great for precision but terrible for range: you can’t represent both 10−3010−30 and 10301030 unless you use thousands of bits.


