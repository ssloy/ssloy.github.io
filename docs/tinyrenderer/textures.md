---
title: More data!
---

# Textures

![](textures/phong.png)
![](textures/normalmap.jpg)

![](textures/uv-map.jpg)

![](textures/mit.svg)

$$
\vec{e} = (1,-1)
$$

$$
\vec{n} = (1,1)
$$

$$
\vec{e} \cdot \vec{n} = 1\cdot 1 + (-1)\cdot 1 = 0
$$

$$
M = \begin{pmatrix}1 & 0 \\ 0 & 2\end{pmatrix}
$$

$$
(M^{-1})^\top = \begin{pmatrix}1 & 0 \\ 0 & \frac12\end{pmatrix}
$$

$$
\vec{e'} = M\ \vec e = (1, -2)
$$

$$
\vec{n'} = M\ \vec n = (1, 2)
$$

$$
\vec{e'}\cdot\vec{n'} = 1\cdot 1 + (-2)\cdot 2 \neq 0
$$



## 2. How positions transform vs. how normals must transform

Suppose our model transformation is the matrix **M**, which maps old positions to new positions:

$$
\vec{p'} = M \, \vec{p}
$$

A tangent vector transforms the same way:

$$
\vec{t'} = M \, \vec{t}
$$

If we naively transformed normals like:

$$
\vec{n'} = M \, \vec{n}
$$

then the perpendicularity condition after transformation would require:

$$
\vec{n'} \cdot \vec{t'} = (M \vec{n}) \cdot (M \vec{t}) = 0
$$

But in general:

$$
(M \vec{n}) \cdot (M \vec{t}) = \vec{n}^\top M^\top M \, \vec{t}
$$

This equals $\vec{n} \cdot \vec{t}$ **only if** $M^\top M = I$, i.e. when **M** is orthogonal (pure rotation/reflection, possibly uniform scaling).
For non-uniform scaling or shear, this fails — perpendicularity is lost.




We want the condition $\vec{n'} \cdot \vec{t'} = 0$ to hold for all tangents **t** such that $\vec{n} \cdot \vec{t} = 0$.

Substitute $\vec{t'} = M \vec{t}$:

$$
\vec{n'} \cdot (M \vec{t}) = 0
$$

Using the property of the dot product $(\vec{a} \cdot (B\vec{b})) = ((B^\top \vec{a}) \cdot \vec{b})$:

$$
(M^\top \vec{n'}) \cdot \vec{t} = 0
$$

For this to hold for all tangents **t** with $\vec{n} \cdot \vec{t} = 0$, we must have:

$$
M^\top \vec{n'} \; \parallel \; \vec{n}
$$

Choosing equality (ignoring scaling factors we can normalize away):

$$
M^\top \vec{n'} = \vec{n}
$$

Thus:

$$
\vec{n'} = (M^{-1})^\top \vec{n}
$$

---


--8<-- "comments.html"




