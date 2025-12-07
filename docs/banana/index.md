## Solving ordinary differential equations

Let us consider an ordinary differential equation (ODE) of the form

$$
\frac{dx}{dt} = f(t, x),\quad t\geq 0
$$

with some initial condition $x(0)$. We want to solve computers to solve the ODE numerically,
so let us set some time sampling rate $\Delta t$ and define the series $t_{i+1} := t_i + \Delta t$.
The idea is to compute a sequence $\{x_i\}_{i=0}^{n}$ that approximates the ODE, i.e. $x_i \approx x(t_i)$.
Note the difference, when I am writing $x(t_i)$, I mean the true (unknown) function, whereas $x_i$ is its approximation we want to compute.

Recall that Taylor series is a way to recover a function from its derivatives,
and our ODE gives exactly that. So we can write an expansion $x(t)$ around the point $t_i$:

$$
x(t) = x(t_i) + f(t_i, x(t_i))(t-t_i) + \frac{1}{2!}f'(t_i, x(t_i))(t-t_i)^2 +  \frac{1}{3!}f''(t_i, x(t_i))(t-t_i)^3 + \dots
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

### RK2 scheme for the banana

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


## Ground truth for projectile motion

### No air friction

We treat motion in the horizontal $x$ and vertical $y$ directions separately,
since they are uncoupled except through the time variable.
Thus, projectile trajectory is given by $(x(t), y(t))$.
Let us note by $v_x(t)$ and $v_y(t)$ the corresponding velocity.

Here are our assumptions:

* Gravity is acting vertically, i.e. $\frac{dv_x}{dt} = 0$ and $\frac{dv_y}{dt} = g$ with constant $g$, i.e. flat Earth approximation ;).
* No air resistance.
* Initial conditions: the projectile is launched from the origin at the beginning of the time: $x(0) = 0$, $y(0) = 0$.
The launch speed is $v_0$, and $\theta$ is the launch angle w.r.t the ground.
So, we can compute the initial velocity as

$$
\begin{align*}
v_x(0) &= v_0 \cos\theta\\
v_y(0) &= v_0 \sin\theta
\end{align*}
$$

We can derive the motion equation from Newton's second law.
As per our assumptions, the acceleration is constant:

$$
\frac{d^2x}{dt^2} = \frac{dv_x}{dt} = 0, \qquad \frac{d^2y}{dt^2} = \frac{dv_y}{dt} = g.
$$

We can integrate these once to get the velocity:

$$
\begin{align*}
v_x(t) &= v_0 \cos\theta + \int_0^t 0 \,ds =  v_0 \cos\theta\\
v_y(t) &= v_0 \sin\theta + \int_0^t g \,ds =  v_0 \sin\theta + gt.
\end{align*}
$$

And integrate the second time to retrieve the position:

$$
\begin{align*}
x(t) &= \int_0^t v_0 \cos\theta \,ds = v_0 \cos\theta \, t \\
y(t) &= \int_0^t (v_0 \sin\theta + gs) \,ds = v_0 \sin\theta\, t + g\frac{t^2}2 .
\end{align*}
$$



### Linear drag

If the drag force is proportional to the velocity relative to the air, i.e

$$
m\frac{d\vec v(t)}{dt}=-\mu(\vec v(t) -\vec w)+m\vec g
$$

with constant wind $\vec w$ and constant gravity $\vec g$, this is a linear ODE and has an elementary closed-form solution.
Let $\tau:=m/\mu$. We can rewrite the ODE:

$$
\frac{d\vec v(t)}{dt}=-\frac 1 \tau (\vec v(t) -\vec w)+\vec g.
$$

Setting the derivative $\frac{d \vec v(\infty)}{dt}$ to zero, we can find the terminal velocity:

$$
\vec v(\infty) = \vec w+\tau\vec g.
$$

Interpretation: if you waited long enough, the projectile velocity tends to the wind plus the terminal velocity due to gravity.

Now let us examine the homogeneous equation. If $\vec g = \vec w = 0$, then

$$
\frac{d\vec v(t)}{dt}=-\frac 1 \tau \vec v(t).
$$

The homogeneous equation has an elementary solution:

$$
\vec v(t)= \vec c\,e^{-t/\tau},
$$

where $\vec c$ is a constant vector determined by initial conditions.

Because the ODE is linear, any sum of the homogeneous and particular (steady) solution is a solution of the full ODE.

??? tip "Why does the superposition give all solutions?"
    Let $L$ be a linear differential operator, and
    suppose $u$ and $v$ are two different solutions of the full ODE:
    $L(u)=f$, $L(v)=f$.
    Then $L(u-v) = L(u) - L(v) = f - f = 0$.
    So the difference of any two full solutions is a homogeneous solution.
    This is one of the most important ideas in differential equations, and it’s surprisingly simple once you see the underlying structure.
    All diversity of solutions comes entirely from the homogeneous part.
    A single particular solution + the space of homogeneous solutions gives you all possible solutions.

Thus full solution:

$$
\vec v(t)=\vec v(\infty) + \vec c\, e^{-t/\tau}.
$$

Then use the initial condition $\vec v(0)$ to determine the constant $\vec c = \vec v(0) - \vec v(\infty)$, giving:

$$
\boxed{\vec v(t)= \vec w+\tau\vec g + (\vec v(0) - \vec w - \tau\vec g)\, e^{-t/\tau}.}
$$

We can recover the trajectory by integrating the velocity:

$$
\begin{align*}
\vec x(t) &= \vec x(0) + \int_0^t \vec v(s)\, ds = \\
&= \boxed{\vec x(0) + t\, ( \vec w+\tau\vec g)  + \tau\, (\vec v(0) - \vec w - \tau\vec g) \bigl(1-e^{-t/\tau}\bigr)}
\end{align*}
$$

### Back to frictionless motion

If you set the linear drag coefficient $\mu=0$ (so no friction), the wind has no effect and you recover the standard frictionless projectile motion:

$$
\boxed{
\begin{align*}
\vec v(t) &= \vec v(0) + g\,t \\
\vec x(t) &= \vec x(0) + \vec v(0)\,t + \vec g\,\frac{t^2}{2}.
\end{align*}
}
$$

Why is that so different from our earliest closed-form solution, can't we just set $\mu = 0$?
Well, we can, if we do it carefully. The problem is that $\vec v(\infty)$ appears to blow up $(\tau \rightarrow \infty)$.
That is an indeterminate form: individual pieces diverge but the combination can have a finite limit.
So we must either:

* go back to the ODE and set $\mu$ (easy and safest), or
* take the limit $\mu\rightarrow 0$  (i.e. $\tau\rightarrow\infty$) carefully.

Let us perform the latter. Recall our closed-form solution for the ODE with linear drag:

$$
\vec v(t)=\vec w+\tau\vec g+(\vec v(0)-\vec w-\tau\vec g)\,e^{-t/\tau}.
$$

Expand $e^{-t/\tau}=1-\tfrac{t}{\tau}+O(1/\tau^2)$. Then

$$
\vec v(t)=\vec v(0) + \vec g t + \underbrace{O(1/\tau)}_{\to 0\ \text{as }\tau\to\infty}.
$$

Thus as $\tau\to\infty$ (i.e. $\mu \to 0$) the finite limit is

$$
\vec v(t)\to \vec v(0)+\vec g\,t,
$$

and integrating gives $\vec x(t)\to \vec x(0)+\vec v(0) t+\tfrac12\vec g t^2$. The wind contributions vanish in the limit.

As a practical note, if you want to simulate the frictionless case, don’t use the closed-form formulas that explicitly contain $\mu$; instead use the standard frictionless solution above.
If $\mu$ is small but nonzero, wind will eventually matter, but only through terms proportional to $1/\tau$ (small corrections for short times).





