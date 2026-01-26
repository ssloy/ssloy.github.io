# The Ape Hits a Target

Up to this point, the simulation has been used to predict what happens given a throw. In this chapter, the direction is reversed: the throw itself becomes the unknown. The question is simple to state:

— If the throw angle is fixed, which launch angle makes the banana hit a target at the ground?

While the problem has an analytical solution, the idea is to find the answer entirely from numerical simulation. This way, we can check the closed-form solution to assess our results.

A target is painted on the ground, at a known horizontal position $x^*$.
The throw angle is fixed, and the only thing the ape is willing to adjust is the initial speed.
Every failed throw costs a banana.
The ape wants to spend as few bananas as possible.

## One parameter, one event, one constraint.

In the previous chapter, the ape learned how to simulate the motion of a banana using a time-stepping scheme and how to detect the moment when the banana hits the ground.
This required careful handling of two distinct ingredients:

* A numerical integration scheme (explicit Euler)
* An event detection mechanism to stop the simulation at the correct physical time.

We now revisit this procedure from a different point of view.

At first sight, the simulation seems to produce a trajectory: $(x(t),y(t)),t \geq 0$.

However, this is not what we ultimately need.

In the present problem, the ape is not interested in the entire flight of the banana.
Only one number matters, namely, the horizontal position of the banana when it hits the ground.
Let us call it $x_\text{impact}$.

This observation allows us to radically simplify our description of the numerical procedure.
Since the gravitational acceleration, the launch angle, the initial position and the time step $\Delta t$ are fixed, 
the only remaining free parameter is the initial speed $v_0$.
The numerical procedure is fully determined, so 

We view the simulator as a function from parameters to outcomes; in inverse-problem language, this is called the forward map.

This entire procedure defines a mapping:
$$
F:v_0\to x_\text{impact}
$$


We call $F$ the forward map.

It is essential to understand what the forward map is — and what it is not.

    FF is not a closed-form formula.

    FF is not evaluated analytically.

    FF is produced by a numerical algorithm.

Yet, from the outside, it behaves exactly like an ordinary function:

    One input

    One output

    Always the same output for the same input

From now on, we will treat the simulator as a function.


1.5 Black-box viewpoint

In scientific computing, it is often neither possible nor useful to inspect the internal structure of a simulation code.

We therefore adopt the following rule:

    The forward map FF is a black box.

This means:

    We can evaluate F(v0)F(v0​).

    We can evaluate it again for another value of v0v0​.

    We do not assume any explicit formula for FF.

This viewpoint is not a simplification — it is a realistic model of how numerical solvers are used in practice.
1.6 Determinism and reproducibility

Because all numerical choices are fixed, the forward map has an important property:

    Determinism

Running the simulation twice with the same v0v0​ produces exactly the same ximpactximpact​.

This is what allows us to reason about FF as a mathematical object, even though it is generated numerically.
1.7 Smoothness: an empirical observation

At this stage, we do not assume anything about the regularity of FF.

However, numerical experiments reveal that:

    Small changes in v0v0​ lead to small changes in ximpactximpact​.

    The map appears smooth.

This observation will become important later, but for now it remains empirical.
1.8 Cost of evaluating the forward map

Each evaluation of FF requires:

    A full time integration

    Event detection

    Interpolation

In the ape’s world, this cost is easy to measure:

    One evaluation of FF consumes exactly one banana.

From this point onward, numerical algorithms will be judged not only by correctness, but also by banana efficiency.
1.9 Why this abstraction matters

This section marks a conceptual turning point.

We no longer think in terms of:

    Positions

    Velocities

    Time steps

Instead, we think in terms of:

    Inputs

    Outputs

    Numerical cost

This shift allows us to formulate the ape’s task in a new way:

    Given a function FF, find an input such that its output satisfies a constraint.

This is the foundation of inverse problems, optimization, and parameter identification.

![](target/plot-x-range.png)

![](target/hit-x-binary.png)

![](target/hit-x-linear.png)

Let $x_0,x_1,x_2\dots$ be a sequence which converges to $x^\star$ and $e_k:= |x_k - x^\star|$. If there exist $p$ and $r\neq 0$ such that 

$$
\lim\limits_{k\to\infty} \frac{e_{k+1}}{e_k^p} = r, 
$$

then $p$ is called the order of convergence and $r$ is the rate of convergence.
Intuitively, they can be understand by considering the amount of digits accurate per iteration

The number of correct digits in $x_n$ is related to the magnitude of the error, i.e.

$$
\text{Number of correct digits} \approx - \lg |x_k - x^\star|.
$$

Let’s analyze how the error changes from $x_k$ to $x_{k+1}$:

$$
e_{k+1} \approx e_k^p \cdot r
$$


Taking the base-10 logarithm:
$$
\lg e_{k+1} \approx p \lg e_k + \lg r
$$
This shows that the number of correct digits roughly multiplies by p per iteration.
Initially the rate of convergence matters the most when $\lg e_k$ is small, while for large $\lg e_k$ the order of convergence will matter more.






|           | Bisection | Regula falsi                  | Secant                   | Newton                   |
|---------- | :-------: | :---------------------------: | :----------------------: | :----------------------: |
| **Order** | $1$       | $1$                           | $\frac{1+\sqrt 5}{2}$    | $2$                      |
| **Rate**  | $\frac12$ | $-\frac{f''(x)}{2f'(x)}(x-z)$ | $-\frac{f''(x)}{2f'(x)}$ | $-\frac{f''(x)}{2f'(x)}$ |

$z$ denotes the second point used in the regula falsi.

Bisection is very easy to prove, since the interval always halves.
Midpoint $x_{k+1}$ of interval $(a_k, b_k)$ is an approximation of $x^\star$ with error

$$
|x_{k+1} - x^\star| \leq \frac12 (b_k - a_k) = 2^{-k-1}(b_0 - a_0).
$$

Then

$$
\lim\limits_{k\to\infty} \frac{e_{k+1}}{e_k^p} = \frac{2^{-k-1}(b_0 - a_0)}{\left(2^{-k}(b_0 - a_0)\right)^p} = \frac12 \left(\frac{2^k}{b_0 - a_0}\right)^{p-1}
$$

For this limit to exist and be finite, the exponent of 2 must vanish, i.e.

$$
p = 1,\qquad r = \frac12.
$$


## Newton's method

```C linenums="1"
float Q_rsqrt( float number ) {
	long i;
	float x2, y;
	const float threehalfs = 1.5F;
	x2 = number * 0.5F;
	y  = number;
	i  = * ( long * ) &y;                       // evil floating point bit level hacking
	i  = 0x5f3759df - ( i >> 1 );               // what the fuck?
	y  = * ( float * ) &i;
	y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration
//	y  = y * ( threehalfs - ( x2 * y * y ) );   // 2nd iteration, this can be removed
	return y;
}
```

## Deliverables



Let the error $e_k$ be 

$$
e_k := |x_k - x^\star|.
$$

Define $\delta_k$ as

$$
\delta_k := \frac{b_k - a_k}{2} - e_k
$$

Let us assume the root $x^\star$ never coincides with a midpoint $x_k$, i.e. $e_k>0$ for all $k$ (otherwise convergence is finite and the asymptotic question is moot).
It means that 

$$
\delta_k < \frac{b_k-a_k}{2} = \frac{b_0 - a_0}{2^{k+1}}.
$$


Thus:

$$
e_k = \frac{b_0-a_0}{2^{k+1}} - \delta_k,
\qquad
 \delta_k < \frac{b_0-a_0}{2^{k+1}}.
$$



Now form the ratio:

$$
\frac{e_{k+1}}{e_k} =
\frac{
\frac{b_0-a_0}{2^{k+2}} - \delta_{k+1}
}{
\frac{b_0-a_0}{2^{k+1}} - \delta_k
}
=
\frac12
\cdot
\frac{
1 - \frac{2^{k+2}}{b_0-a_0}\delta_{k+1}
}{
1 - \frac{2^{k+1}}{b_0-a_0}\delta_k
}.
$$


Now define:

$$
\varepsilon_k := \frac{2^{k+1}}{b_0-a_0}\delta_k \in (0,1).
$$

So:

$$
\frac{|e_{k+1}|}{|e_k|} = \frac12 \cdot \frac{1-\varepsilon_{k+1}}{1-\varepsilon_k}.
$$

---

