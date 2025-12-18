# The Ape Buys a Better Watch

Although this description is approximate, refining the time step will gradually reveal the smooth parabolic path familiar from physics.

![](euler/plot-convergence.png)



We have a projectile starting at $(x_0, y_0) = (0,0)$, with initial velocity $(v_{x,0}, v_{y,0})$, under constant gravity $g$ acting downward. No air resistance.

The ODEs are:

$$
\frac{dx}{dt} = v_x, \quad \frac{dy}{dt} = v_y, \quad \frac{dv_x}{dt} = 0, \quad \frac{dv_y}{dt} = g
$$

---

### 2. Euler integration scheme

With a time step $\Delta t$, the Euler update rules are:

$$
\begin{align*}
x_{i+1} & = x_i + v_{x,i}~\Delta t\\
y_{i+1} & = y_i + v_{y,i}~\Delta t\\
v_{x,i+1} & = v_{x,i} \\
v_{y,i+1} & = v_{y,i} + g~\Delta t
\end{align*}
$$

---



Let’s write the explicit formula for $x_i$ and $y_i$.

Let $t := i \Delta t$. Then

$$
\begin{align*}
x(t) &= \sum_{k=0}^{i-1} v_{x,k}~\Delta t = v_{x,0} \sum_{k=0}^{i-1} \Delta t = v_{x,0}~i ~\Delta t = v_{x,0}~t\\
y(t) & = \sum_{k=0}^{i-1} v_{y,k}~\Delta t= \sum_{k=0}^{i-1} (v_{y,0} + k~g~\Delta t)~\Delta t = \\
&= \left(v_{y,0}\sum_{k=0}^{i-1}1  + g \Delta t \sum_{k=0}^{i-1} k \right)\Delta t =\\
&= v_{y,0} i \Delta t + g (\Delta t)^2 \frac{(i-1)~i}{2} = \\
& = v_{y,0} t + g (\Delta t)^2 \frac{(t/\Delta t)(t/\Delta t - 1)}{2} =\\
& = v_{y,0} t + g\frac{t (t - \Delta t)}{2}
\end{align*}
$$

As $\Delta t \to 0$:

$$
y(t) \to  v_{y,0}~t + g \frac{t^2}{2} 
$$

---
We treat motion in the horizontal $x$ and vertical $y$ directions separately,
since they are uncoupled except through the time variable.
Thus, projectile trajectory is given by $(x(t), y(t))$.
Let us note by $v_x(t)$ and $v_y(t)$ the corresponding velocity.

Here are our assumptions:

* Gravity is acting vertically, i.e. $\frac{dv_x}{dt} = 0$ and $\frac{dv_y}{dt} = g$ with constant $g$, i.e. flat Earth approximation ;).
* No air resistance.
* Initial conditions: the projectile is launched from the origin at the beginning of the time: $x(0) = 0$, $y(0) = 0$.
The launch speed is $v_0$, and $\theta_0$ is the launch angle w.r.t the ground.
So, we can compute the initial velocity as

$$
\begin{align*}
v_x(0) &= v_0 \cos\theta_0\\
v_y(0) &= v_0 \sin\theta_0
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
v_x(t) &= v_0 \cos\theta_0 + \int_0^t 0 \,ds =  v_0 \cos\theta_0\\
v_y(t) &= v_0 \sin\theta_0 + \int_0^t g \,ds =  v_0 \sin\theta_0 + gt.
\end{align*}
$$

And integrate the second time to retrieve the position:

$$
\begin{align*}
x(t) &= \int_0^t v_0 \cos\theta_0 \,ds = v_0 \cos\theta_0 \, t \\
y(t) &= \int_0^t (v_0 \sin\theta_0 + gs) \,ds = v_0 \sin\theta_0\, t + g\frac{t^2}2 .
\end{align*}
$$




---



When we write down the equations of motion for a projectile, we are in fact describing a curve in a three-dimensional space whose coordinates are time and position.
Each state of the system is a point $(t, x, y)$, and the differential equation tells us how this point moves as time increases.
From this point of view, the solution of the ODE is not directly a curve in the plane, but a space curve parameterized by time.
By projecting this curve onto the $(t,x)$ and $(t,y)$ planes, we obtain the two functions $x(t)$ and $y(t)$, which describe how the horizontal and vertical positions evolve in time.
Most of the time, however, we visualize motion by eliminating time altogether and plotting $y$ as a function of $x$.
This $(x,y)$ plot is only a projection of the full trajectory, and it hides the role of time.
It is therefore important to keep the axes in mind: a graph of $y$ versus $t$ does not tell the same story as a graph of $y$ versus $x$, even though both come from the same underlying motion.


![](euler/plot3d.png)

