---
title: Barycentric coordinates
---
# Primer on barycentric coordinates

## 1D barycentric coordinates
Now it is the time to recall the note I made on the barycentric coordinates when we rasterized segments.
Just as regular coordinates give the position of a point with respect to a chosen basis,
barycentric coordinates express a point's position relative to a given set of reference points.
Let's first consider the simplest case: a **1D segment** defined by two values \( A \in \mathbb R\) and \( B \in \mathbb R \).
Given a point \( P \) on the segment between \( A \) and \( B \), we can express its position as a weighted combination:

\[
P = \alpha A + \beta B
\]

The term "barycentric" comes from the Greek word *barys* (meaning heavy), as these coordinates originally arose in **center of mass computations**.
If we place a weight of $\alpha$ kg to the point $A$ and $\beta$ kg to the point $B$, then the barycenter of the system will be situated in the point $P$.
Note that the barycenter would not move if we put weights $13 \alpha$ and $13 \beta$ instead of $\alpha$ and $\beta$.
The usual way to eliminate this redundancy is to distribute $1$ kg in total, meaning that

\[
\alpha + \beta = 1.
\]

Under this constraint $\alpha$ and $\beta$ are unique for each choice of point $P$ and the reference segment $[A, B]$.
How do we find $\alpha$ and $\beta$ for given $P$, $A$ and $B$?
Well, we have a system of two equations with two unknowns:

$$
\left\{
\begin{array}{l}
    P = \alpha A + \beta B\\
    1~ = \alpha + \beta
\end{array}\right.
$$

Solving the system, we get following equations:

\[
\alpha = \frac{B - P}{B - A}, \quad \beta = 1-\alpha = \frac{P - A}{B - A}.
\]

These coordinates tell us how much of \( A \) and \( B \) contribute to the position of \( P \):

- If \( P = A \), then \( \alpha = 1 \) and \( \beta = 0 \).
- If \( P = B \), then \( \alpha = 0 \) and \( \beta = 1 \).
- If \( P \) is outside \( [A, B] \), then one coordinate is **negative**.
- If \( P \) is exactly on \( A \) or \( B \), one coordinate is **zero**.
- If both coordinates are **between 0 and 1**, \( P \) is strictly inside the segment.

## 2D barycentric coordinates

In 1D we used two points to compute their barycenter. In 2D we'd need a triangle.
Given a triangle with vertices \( A, B, C \), any point \( P \) inside the triangle can be written as:

\[
P = \alpha A + \beta B + \gamma C,
\]

where the barycentric coordinates \( \alpha, \beta, \gamma \) satisfy:

\[
\alpha + \beta + \gamma = 1.
\]

We can compute the weights $\alpha$, $\beta$ and $\gamma$ for given 2D points $P$, $A$, $B$ and $C$ in the same manner we did in the previous example.
We have three unknowns with three equations linking them:

$$
\left\{
\begin{array}{ll}
    \alpha A_x + \beta B_x + \gamma C_x &= P_x\\
    \alpha A_y + \beta B_y + \gamma C_y &= P_y\\
    \alpha + \beta + \gamma &= 1
\end{array}\right.
$$

For a better readability (optional), we can rewrite the same equation in the matrix form:

$$
\begin{pmatrix}
    A_x & B_x & C_x\\
    A_y & B_y & C_y\\
    1 & 1 & 1
\end{pmatrix}
\begin{pmatrix}\alpha \\ \beta \\ \gamma\end{pmatrix}
=
\begin{pmatrix}P.x \\ P.y \\ 1\end{pmatrix}
$$

It turns out that the matrix on the left has a very particular form.
Its determinant is equal to twice the **signed area** of the triangle $ABC$.
Then the coordinate \( \alpha \) is given by the ratio of the sub-triangle \( PBC \) to the total triangle \( ABC \):

\[
\alpha = \frac{ \, \text{Area}(PBC) \, }{ \, \text{Area}(ABC) \, }.
\]

Similarly,

\[
\beta = \frac{ \, \text{Area}(PCA) \, }{ \, \text{Area}(ABC) \, }, \quad \gamma = \frac{ \, \text{Area}(PAB) \, }{ \, \text{Area}(ABC) \, }.
\]

The [shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula) allows to efficiently compute these areas:

\[
\text{Area}(ABC) = \frac{1}{2} \left| A_x B_y + B_x C_y + C_x A_y - (A_y B_x + B_y C_x + C_y A_x) \right|.
\]

The interpretation of the weights is very similar to the 1D case:

- If \( \alpha, \beta, \gamma \) are all **between 0 and 1**, \( P \) is **inside** the triangle.
- If any coordinate is **negative**, \( P \) is **outside** the triangle.
- If one coordinate is exactly **zero**, \( P \) lies **on an edge**.
- If two coordinates are **zero**, \( P \) is exactly on a vertex.

Barycentric coordinates are fundamental in rasterization because they allow efficient interpolation of attributes such as colors, depth values, and texture coordinates across triangles in 3D rendering.

