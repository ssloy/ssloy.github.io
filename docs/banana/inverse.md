# The Ape Learns the Jungle Laws


We model a real-world experiment in which the physical state of the system has been measured at a specific time $t_{\text {meas}}$.
We denote this observation by $\vec s_{\text{meas}}$.
On the other hand, our numerical model evolves a predicted state $\vec s_n$
by integrating an ordinary differential equation with time step $\Delta t$,
so that the discrete index $n \approx t/\Delta t$
corresponds to the same physical instant at which the measurement was taken. 

The parameters of the ODE (gravity, wind, and drag coefficients) are a priori unknown, but we can have an initial guess.
For example, no wind, little drag and a reasonable gravity acting downwards.
Our objective is to adjust these parameters so that the simulated state 
$\vec s_n$  matches the real-world measurement $\vec s_{\text{meas}}$
  as closely as possible. In practice, this is expressed by minimizing the discrepancy 
$\vec s_n - \vec s_{\text{meas}}$
  through sensitivity-based optimization, ensuring that the estimated parameters yield a trajectory consistent with the observed experiment.

Let the state vector $\vec s\in \begin{pmatrix}x & y & v_x & v_y\end{pmatrix}^\top = \begin{pmatrix}\vec x\\ \vec v\end{pmatrix}$ (we group as $\vec x\in\mathbb R^2, \vec v \in \mathbb R^2$).
Parameters $\vec p$ we care about:
$\vec p = \begin{pmatrix}\tau & w_x & w_y &g\end{pmatrix}^\top$.
Right-hand side $\vec f(\vec s, \vec p)$ of the ODE $\frac{d}{dt}\vec s = \vec f(\vec s, \vec p)$:

$$
\vec f(\vec s, \vec p) = \begin{pmatrix} \vec v \\ \frac 1 \tau (\vec w - \vec v) + \vec g\end{pmatrix},
$$

where $\vec w = \begin{pmatrix}w_x\\w_y\end{pmatrix}$ and $\vec g = \begin{pmatrix}0\\g\end{pmatrix}$.

As I already said, we want to adjust the parameters $\vec p$ so that the simulated state $\vec s_n$
matches the measurement $\vec s_{\text{meas}}$.
To do so, we need to know how state of a system reacts to changes in its parameters.
We can do using the sensitivity matrix $S_n$, a central tool for gradient-based optimization:

$$
S_n := \frac{\partial \vec s_n}{\partial \vec p}
$$

In our example, it is a $4\times 4$ matrix, whose $i,j$ entry tells you how much the $i$-th component of the state changes when you slightly vary the $j$-th parameter.
In other words, it quantifies how errors or adjustments in the parameters propagate through the dynamics.

If the initial state $\vec s_0$ does not depend on parameters, then $S_0 = 0_{4\times 4}$.
Let us study the simplest case, where the ODE is integrated with the first-order Euler scheme.
Then $\vec s_n$ is built from $s_0$ using the Euler recurrence relation $\vec s_{i+1} := \vec s_i + \Delta t\, \vec f(\vec s, \vec p)$,
so we can estimate $S_{i+1}$ by differentiating the Euler step with respect to $\vec p$:

$$
\frac{\partial \vec s_{i+1}}{\partial \vec p}
= \frac{\partial \vec s_i}{\partial \vec p}
+ \Delta t\left(\frac{\partial \vec f}{\partial \vec s}(\vec s_i,\vec p)\,\frac{\partial \vec s_i}{\partial \vec p}
+ \frac{\partial \vec f}{\partial p}(\vec s_i,\vec p)\right).
$$

We can rewrite it as 

$$
S_{i+1} = S_i + \Delta t\, (F_s(\vec s_i, \vec p) S_i + F_p(\vec s_i, \vec p)),
$$

where $F_s$ and $F_p$ are state and parameter Jacobian matrices:

$$
\begin{align*}
F_s &:= \partial\vec f / \partial\vec s = 
\begin{pmatrix}
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1\\
0 & 0 & -\frac1\tau & 0\\
0 & 0 & 0 & -\frac1\tau
\end{pmatrix}\\
F_p &:= \partial\vec f / \partial\vec p = 
\begin{pmatrix}
0 & 0 & 0 & 0\\
0 & 0 & 0 & 0\\
\frac{v_x-w_x}{\tau^2} & \frac1\tau & 0 & 0\\
\frac{v_y-w_y}{\tau^2} & 0 & \frac1\tau & 1
\end{pmatrix}
\end{align*}
$$


Equivalently (grouping terms),

$$
\boxed{S_{i+1} = \bigl(I_{4\times 4}+ \Delta t\, F_s(\vec s_i,\vec p)\bigr)\,S_i \;+\; \Delta t\,F_p(\vec s_i,\vec p)}.
$$

This is the discrete Euler sensitivity recursion (exact derivative of the Euler map).

??? tip "Sensitivity matrix for RK2 integration"
    $$
    \begin{align*}
    \vec s_{i+0.5} & := \vec s_i + \frac{\Delta t}2 \vec f(\vec s_i, \vec p)\\
    \vec s_{i+1} & := \vec s_i + \Delta t \vec f(\vec s_{i+0.5}, \vec p)
    \end{align*}
    $$

    $$
    \boxed{
    \begin{align*}
    S_{i+0.5} &= S_i + \frac{\Delta t} 2 \big(F_s(\vec s_i, \vec p) S_i + F_p(\vec s_i, \vec p)\big)\\
    S_{i+1} &= S_i + \Delta t\, \big( F_s(\vec s_{i+0.5}, \vec p)\, S_{i+0.5} +  F_p(\vec s_{i+0.5}, \vec p)\big)
    \end{align*}
    }
    $$

Now we have all the tools necessary for the fitting of the parameters $\vec p$.
Define the residual (position error) at step $n$:

$$
\vec r_n(\vec p) = \vec s_n - \vec s_{\text meas}.
$$

We want $\vec r_n(\vec p)\to \vec 0$ by adjusting $\vec p$.

To do so, we can define a least squares cost function:

$$
\mathcal L(p) = \frac12 \|\vec r(\vec p)||^2
$$


#### Gradient descent

Gradient descent is a general optimization method that iteratively updates parameters in the direction that most rapidly decreases the objective function.
In our case, the objective is a least-squares function $\mathcal L$, the gradient of the cost with respect to the parameters can be computed using the sensitivity (or Jacobian) of the predicted state:

$$
\nabla_p\mathcal L = S^\top_n \vec r_n
$$

At each step, the parameters are updated proportionally to the negative gradient of the squared error, which guarantees that the cost decreases if the step size $\alpha$ is chosen appropriately.


$$
\vec p_{\text{new}} = \vec p_{\text{old}} - \alpha\ \nabla_p \mathcal L.
$$


```
choose p

while not tired:
    compute s_n and S_n
    p <- p - alpha * S_n^\top (s_n - s_meas)
    
```

Gradient descent is very simple and pretty robust, but it uses only first-order information and typically requires small, repeated steps to converge.
We can do better, if we use second-order (curvature) information.


#### Gauß-Newton

The Gauss–Newton method is an optimization technique designed specifically for least-squares problems, where you want to minimize the squared difference between a model’s predictions and measurements. It works by linearizing the model around the current parameter estimate: the residuals are approximated using the Jacobian (or sensitivity matrix), turning the nonlinear problem into a local linear least-squares one. Solving this linearized problem gives an update direction that typically converges faster than plain gradient descent. Intuitively, Gauss–Newton uses curvature information from the Jacobian to take more informed steps without computing full second derivatives.

first-order Taylor expansion of the residual:

$$
\vec r(\vec p_0 + \delta\vec p) \approx \vec r(\vec p_0) + S_n \delta\vec p
$$

We want $\vec r(\vec p_0) + S_n \delta\vec p = \vec 0$,
so we can solve following least-squares system:

$$
\delta \vec p = \text{argmin}_{\delta p} \|\vec r(\vec p_0) + S_n \delta\vec p\|^2 = -(S_n^\top S_n)^{-1} S_n^\top \vec r(p_0)
$$

```
choose p

while not tired:
    compute s_n and S_n
    p <- p - (S_n^\top S_n)^{-1} S_n^\top (s_n - s_meas)
    
```




