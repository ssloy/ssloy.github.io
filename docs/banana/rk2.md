# Between Two Seconds, Things Happen

An inverse problem always has this structure:

* You choose parameters θ (e.g. g, wind, drag)
* You simulate forward to get a trajectory
* You compare simulation to data
* You adjust θ

So what you are really optimizing is:
θ  ↦  Integrator(θ)

This means: Any numerical error in the forward solver becomes part of the inverse problem.




Halving Δt halves Euler’s error, but quarters RK2’s error.


RK2 stabilizes inverse problems by preventing numerical error from masquerading as physics.



## Solving ordinary differential equations

Let us consider an ordinary differential equation (ODE) of the form

$$
\frac{dx}{dt} = f(t, x),\quad t\geq 0
$$

with some initial condition $x(0)$. We want to use computers to solve the ODE numerically,
so let us set some time sampling rate $\Delta t$ and define the series $t_{i+1} := t_i + \Delta t$.
The idea is to compute a sequence $\{x_i\}_{i=0}^{n}$ that approximates the ODE, i.e. $x_i \approx x(t_i)$.
Note the difference, when I am writing $x(t_i)$, I mean the true (unknown) function, whereas $x_i$ is its approximation we want to compute.

Recall that Taylor series is a way to recover a function from its derivatives,
and our ODE gives exactly that. So we can write an expansion $x(t)$ around the point $t_i$:

$$
\begin{align*}
x(t) = x(t_i) + &f(t_i, x(t_i))(t-t_i) + \\
 +\, \frac{1}{2!}&f'(t_i, x(t_i))(t-t_i)^2 +  \\
 +\, \frac{1}{3!}&f''(t_i, x(t_i))(t-t_i)^3 + \dots
\end{align*}
$$

### Runge-Kutta 1st order (aka Euler’s) method
We can build the simplest approximation $\{x_i\}_{i=0}^{n}$ by using the first two terms of the Taylor series:

$$
x_{i+1} := x_i + f(t_i, x_i) \Delta t.
$$


### Runge-Kutta 2nd order methods

So what would a 2nd order method formula look like? It would include one more term of the Taylor series as follows.

$$
x_{i+1} := x_i + f(t_i, x_i) \Delta t + \frac 1{2!} f'(t_i, x_i)\Delta t^2.
$$

Because $x'=f(t,x)$, we already know the first derivative.
The second derivative $x''$ can be computed using the chain rule:

$$
x''(t) = \frac d {dt} f(t, x(t)) = \frac{\partial f}{\partial t} + \frac{\partial f}{\partial x} f.
$$

Thus

$$
x(t+\Delta t) = x(t) + \Delta t\, f(t, x) + \frac {\Delta t^2}{2}\Big(\frac{\partial f}{\partial t} + \frac{\partial f}{\partial x} f\Big) + O(\Delta t^3).
\tag{1}
\label{taylor}
$$

This is the **target** that any 2nd-order numerical method should match up to $O(\Delta t^3)$.

Note that we won't use this expansion directly, even if it is possible.
As you can see, it would explicitly require derivatives of $f$ with both $t$ and $x$.
For a scalar ODE, that’s already annoying.
For systems of equations it rapidly becomes untractable:
if we have a system of $n$ equations ($x\in R^{n}$), even the first derivative $\partial f/\partial x$ is an $n\times n$ matrix.
It becomes unusable for real problems, especially as we increase order.

The idea behind Runge-Kutta methods is to get the same accuracy Taylor expansion offers, but without ever differentiating $f$.
Instead, we can evaluate $f$ multiple times at cleverly chosen points.
What [Carl Runge](https://en.wikipedia.org/wiki/Carl_Runge) and [Wilhelm Kutta](https://en.wikipedia.org/wiki/Martin_Kutta) did in 1901, was write the 2nd order method as

$$
x_{i+1} := x_i + (a_1 k_1 + a_2 k_2) \Delta t,
\tag{2}
\label{rk}
$$

where

$$
\begin{align*}
k_1 &:= f(t_i, x_i)\\
k_2 &:= f(t_i + b_1\Delta t,\, x_i + b_2 k_1\Delta t).
\end{align*}
$$

This form allows one to reach the accuracy of the 2nd order method without having to calculate $f'(t, x)$.
Here we do not yet know the coefficients $a_1, a_2, b_1, b_2$.
We determine them by matching Taylor expansions.

To do so, first we expand $k_2$ around $(t_i, x_i)$:

$$
\begin{align*}
k_2 &= f + b_1 \Delta t \frac{\partial f}{\partial t} + b_2 k_1 \Delta t \frac{\partial f}{\partial x} + O(\Delta t^2) = \\
&= f +\Delta t \left( b_1 \frac{\partial f}{\partial t} + b_2\, f\, \frac{\partial f}{\partial x}\right) + O(\Delta t^2).
\end{align*}
$$

We can plug this expansion into the RK update:

$$
\begin{align*}
x_{i+1} & := x_i + (a_1 k_1 + a_2 k_2) \Delta t = \\
& = x_i + \Delta t\left(a_1 f+ a_2\left(  f +\Delta t \left( b_1 \frac{\partial f}{\partial t} + b_2\, f\, \frac{\partial f}{\partial x}\right)    \right)\right)  + O(\Delta t^3) = \\
& = x_i + \Delta t (a_1 + a_2)\,f  + \Delta t^2\, a_2 \left( b_1 \frac{\partial f}{\partial t} + b_2\, f\, \frac{\partial f}{\partial x}\right)      + O(\Delta t^3)
\end{align*}
$$

Now we can match the coefficients with respect to the true expansion $\eqref{taylor}$.
This gives us following constraints:

$$
\begin{align*}
a_1 + a_2 &= 1\\
a_2\, b_1 &= \frac12\\
a_2\, b_2 &= \frac12
\end{align*}
$$

Thus Runge-Kutta update scheme $\eqref{rk}$ uses four parameters that are tied by three constraints,
leaving one parameter free.
Generally, the value of $a_2$ is chosen to evaluate the other three constants.
Three popular choices for $a_2$ are $\frac12$, $1$ and $\frac23$,
and are known as [Heun’s method](https://en.wikipedia.org/wiki/Heun%27s_method), the midpoint method, and Ralston’s method, respectively.

The midpoint method ($a_1 = 0$, $a_2 = 1$, $b_1 = b_2 = 1/2$) is the simplest one.
It results to the following RK2 update:

* first we estimate the midpoint using 1st order integration

$$
  \begin{align*}
  t_{i+0.5} &:= t_i + \frac{\Delta t}{2}\\
  x_{i+0.5} &:= x_i + \frac{\Delta t}{2} f(t_i,  x_i)
  \end{align*}
$$

* and then we evaluate $f$ at the midpoint to obtain the 2nd order without ever differentiating $f$

$$
x_{i+1} := x_i + \Delta t\, f\left(t_{i+0.5}, ~ x_{i+0.5} \right).
$$

Clever and beautiful, is not it?

<!--

Recall that our general idea is to approximate the exact integral over one timestep:

$$
\int_{t_i}^{t_{i+1}} f(t, x(t))\, dt
$$

Each RK2 method tries to approximate this integral by evaluating $f$ only two times:

* Midpoint samples the slope exactly in the middle (best accuracy for smooth curves).
* Heun samples at the ends and averages (more smoothing, more stable).
* Ralston samples at slightly biased points to minimize the truncation error.

Each is a different quadrature rule for the unknown slope curve,
so the choice depends on what you care about.

* If you want best accuracy per step, use Ralston.
* If you want simplicity and good behavior on oscillatory systems, use midpoint.
* If you want stability and robustness, then Heun is a good choice.

-->

### RK2 scheme for the no-air banana

Let the state vector be

$$
\vec x(t) = \begin{pmatrix}x \\ y \\ v_x \\ v_y\end{pmatrix}.
$$

Then the projectile motion equation can be written as $\frac{d}{dt} \vec x(t) = \vec f(t, \vec x)$, where $\vec f$ is:

$$
\vec f(t, \vec x) = \begin{pmatrix}v_x \\ v_y \\ 0 \\ g\end{pmatrix}
$$

Having an approximation $\vec x_i$ of the state vector at time $t_i$, we want to compute the RK2 update $\vec x_{i+1}$.
First we need to compute the midpoint state $\vec x_{i+0.5}$:

$$
\vec x_{i+0.5} = \vec x_i +  \frac{\Delta t}{2} \vec f(t_i, \vec x_i) = \begin{pmatrix}x_i + \frac{\Delta t}{2} v_{x,i} \\ y_i + \frac{\Delta t}{2} v_{y,i} \\ v_{x,i} \\ v_{y,i} + \frac{\Delta t}{2} g\end{pmatrix}.
$$

Then we can compute $\vec x_{i+1}$:

$$
\vec x_{i+1} = \vec x_i + \Delta t\, \vec f(t_{i+0.5}, \vec x_{i+0.5}) =  \begin{pmatrix}x_i \\ y_i \\ v_{x,i} \\ v_{y,i}\end{pmatrix} + \Delta t \begin{pmatrix}v_{x,i} \\ v_{y,i} + \frac{\Delta t}{2} g \\ 0 \\ g\end{pmatrix}
$$


### RK2 scheme for the banana with wind

Let the state vector be

$$
\vec x(t) = \begin{pmatrix}x \\ y \\ v_x \\ v_y\end{pmatrix}.
$$

Then the projectile motion equation can be written as $\frac{d}{dt} \vec x(t) = \vec f(t, \vec x)$, where $\vec f$ is:

$$
\vec f(t, \vec x) = \begin{pmatrix}v_x \\ v_y \\ \frac1\mu (w_x - v_x) \\ \frac1\mu(w_y - v_y) + g\end{pmatrix}
$$

$$
\vec x_{i+0.5} = \vec x_i +  \frac{\Delta t}{2} \vec f(t_i, \vec x_i) = \begin{pmatrix}x_i + \frac{\Delta t}{2} v_{x,i} \\ y_i + \frac{\Delta t}{2} v_{y,i} \\ v_{x,i} + \frac{\Delta t}{2}\frac1\mu (w_x - v_x)  \\ v_{y,i} + \frac{\Delta t}{2}\left(\frac1\mu (w_y - v_y) + g\right)\end{pmatrix}.
$$


--8<-- "comments.html"
