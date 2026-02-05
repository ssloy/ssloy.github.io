# The Jungle Is Windy

## Ground truth for projectile motion


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
    A single particular solution + the space of homogeneous solutions give you all possible solutions.

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




--8<-- "comments.html"
