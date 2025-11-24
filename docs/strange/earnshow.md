
## 2D electric potential due to a point charge

In 2D, 

$$
\Delta f(r) = f''(r) + \frac1r f'(r),
$$

therefore $\Delta f = 0$ becomes

$$
f''(r) + \frac{1}{r} f'(r) = 0.
$$


To solve it, we can rewrite left part in “derivative of a product” form:

$$
f''(r) + \frac{1}{r} f'(r) = \frac{1}{r} \big( r f'(r) \big)'.
$$


So the ODE becomes

$$
\frac{1}{r} (r f'(r))' = 0 \quad\Rightarrow\quad (r f'(r))' = 0.
$$

Then to recover $f$ it suffices to integrate the equation twice:


$$
\begin{align}
(r f'(r))' = 0 \quad&\Rightarrow\quad r f'(r) = A,\\
f'(r) = \frac{A}{r} \quad&\Rightarrow\quad  \boxed{f(r) = A \ln r + B},
\end{align}
$$

where $A$ and $B$ are constants.

??? spoiler "Derivation of Coulomb's law in 3D"
    The 3D Laplace equation for a radial function $f(r)$ is

    $$
    \Delta f = f''(r) + \frac{2}{r} f'(r) = 0, \quad r>0.
    $$

    Note the constant 2 appearing in the 3D version, if you are curious where it comes from, check the text under the spoiler.



    ??? spoiler "Laplacian for radial functions for arbitrary dimenensions"
        Let $\vec{x}=(x_1,\dots,x_n)$. Set $r:=|\vec x|$.
        Then the gradient  $\nabla f$ can be written as:


        $$
           \nabla f = f'(r)\,\nabla r = f'(r)\,\frac{\vec{x}}{r} = f'(r)\,\hat{\vec r},
        $$

        where $\hat{\vec r}=\vec{x}/r$ is the radial unit vector.
        Laplacian is divergence of the gradient:

        $$
           \Delta f = \nabla\cdot\Big(f'(r)\,\hat{\vec r}\Big).
        $$

        Use product rule:

        $$
           \nabla\cdot\Big(f'(r)\,\hat{\vec r}\Big) = f''(r)\,\hat{\vec r}\cdot\nabla r + f'(r)\,\nabla\cdot\hat{\vec r}.
        $$

        But $\hat{\vec r}\cdot\nabla r = \dfrac{\vec{x}}{r}\cdot\dfrac{\vec{x}}{r}=1$, so the first term is $f''(r)$.
        For the second term we can note that the divergence of the radial unit vector in $n$ dimensions is
        $\nabla\cdot\hat{\mathbf r}=\frac{n-1}{r}$. Combining both, we obtain

        $$
           \boxed{\Delta f = f''(r) + f'(r)\frac{n-1}{r}}.
        $$

    As before, we rewrite the left part in “derivative of a product” form:

    $$
    f''(r) + \frac{2}{r} f'(r) = \frac{1}{r^2} \big( r^2 f'(r) \big)'.
    $$


    $$
    \begin{align}
    (r^2 f'(r))' = 0 \quad&\Rightarrow\quad r^2 f'(r) = A,\\
    f'(r) = \frac{A}{r^2} \quad&\Rightarrow\quad \boxed{f(r) = \frac{A}{r} + B},
    \end{align}
    $$

    where $A$ and $B$ are constants.
    To sum up, we Coulomb's electric potential due to a point charge is indeed derived from Laplace's equation.



## **Big Picture Intuition**

Think of the electric field like a *flowing fluid*:

* Field lines = water streams
* Charge = source/sink that creates or absorbs flow
* Potential = height of a landscape; water flows downhill

With that analogy, we can reinterpret each step.

---

## **1. Gauss’s Law = Conservation of Electric Flux**

**Gauss says: charge is the source of electric field lines.**

If you imagine the field as water flow, then enclosing a charge is like enclosing a faucet: there is net flow *out* of the surface.

* Positive charge = fountain
* Negative charge = drain
* No charge = no net flow through the boundary

This is a **local conservation law**:

> If there is no charge inside a region, the total electric flux out of any closed surface is zero.

→ *What flows in must flow out* (no accumulation).

---

## **2. Faraday + Electrostatics = No Swirling, Only Gradient Flow**

Faraday says changing magnetic fields create vortices in the electric field.
But in electrostatics nothing changes in time, so **no vortices exist.**

That means the “water” never swirls in circles—it only flows downhill from one place to another.

Flows with no loops must come from a **height function**:

> **Electric field = downhill direction of potential landscape**
> [
> \mathbf{E} = -\nabla \phi
> ]

This is like saying water flows because gravity pulls it downward on a landscape.

---

## **3. Plug into Gauss → Charge Creates Curvature in the Potential**

Now combine both ideas:

* Electric field = flow
* Charge = source of flow
* Potential = height generating the flow

If the field comes from a potential, then **the amount of flow leaving a point is controlled by how curved the potential landscape is.**

Mathematically:
[
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}
]
[
\mathbf{E} = -\nabla\phi
]

→ Gives **Poisson’s equation**:
[
\nabla^2\phi = -\frac{\rho}{\varepsilon_0}
]

Interpretation:

> **Charge causes bulges or dents in the potential surface—the curvature of the potential measures how much source you have.**

---

## **4. No Charge → No Curvature → Harmonic Potential**

If there's no charge, there’s no source or sink for field flow.

→ Flow is balanced everywhere.
→ Nothing pushes the potential up or down.

So:
[
\nabla^2\phi = 0
]

This is Laplace’s equation.

Interpretation:

> **A harmonic function is like a rubber sheet pulled tight: it can only bend if something forces it from the boundary.**

Physical consequences:

* No internal maxima or minima (only at boundaries)
* Mean value property: value at a point = average of surroundings
* Completely determined by boundary conditions → explains uniqueness in electrostatics

---

## **Summary in One Sentence**

> **In electrostatics the field is a flow with no vortices, and if there is no charge then this flow neither originates nor ends anywhere—this forces the potential to be a perfectly balanced surface, i.e., a harmonic function.**

