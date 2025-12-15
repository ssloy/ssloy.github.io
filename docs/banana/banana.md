
We have a projectile starting at $(x_0, y_0) = (0,0)$, with initial velocity $(v_{x0}, v_{y0})$, under constant gravity $g$ acting downward. No air resistance.

The ODEs are:

$$
\frac{dx}{dt} = v_x, \quad \frac{dy}{dt} = v_y, \quad \frac{dv_x}{dt} = 0, \quad \frac{dv_y}{dt} = -g
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
x_i &= \sum_{k=0}^{i-1} v_{x,k}~\Delta t = v_{x,0} \sum_{k=0}^{i-1} \Delta t = v_{x,0}~i ~\Delta t = v_{x,0}~t\\
y_i & = \sum_{k=0}^{i-1} v_{y,k}~\Delta t= \sum_{k=0}^{i-1} (v_{y0} + k~g~\Delta t)~\Delta t = \\
&= \left(v_{y0}\sum_{k=0}^{i-1}1  + g \Delta t \sum_{k=0}^{i-1} k \right)\Delta t\\
&= v_{y0} i \Delta t + g (\Delta t)^2 \frac{(i-1)~i}{2}\\
& = v_{y0} t + g (\Delta t)^2 \frac{(t/\Delta t)(t/\Delta t - 1)}{2}\\
& = v_{y0} t + g\frac{t (t - \Delta t)}{2} 
\end{align*}
$$

As $\Delta t \to 0$:

$$
y(t) \to  v_{y0}~t + g \frac{t^2}{2} 
$$

