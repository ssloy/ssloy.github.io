---
title: Better camera
---

# Better camera handling

In the [previous chapter](camera-naive.md) we have chained three different transformations to the 3D object in order to simulate a camera:

```cpp
auto [ax, ay, az] = project(persp(rot(model.vert(i, 0))));
auto [bx, by, bz] = project(persp(rot(model.vert(i, 1))));
auto [cx, cy, cz] = project(persp(rot(model.vert(i, 2))));
```

All three transformations are encoded by very different functions, let us see if we can unify the treatment.
The idea is to ensure the **composability**: in the above code each 3D vertex is transformed three times.
If we could find the way to pre-compose the transformations and transform the data array just one time, it would allow us to
avoid re-computing intermediate results, resulting in faster batch processing of geometry.

Essentially we want to position, orient, and size objects in a scene, and multiple such transformations can be combined into a single one.
Let us review two classes of transformations that will allow us to do that.

-----------

## Linear transformations

In computer graphics, everything you see - models, characters, cameras - is made of **points and vectors**.
To animate, move, rotate, or resize them, we apply linear and affine transformations to their coordinates.

A linear transformation is a mathematical way to reshape space using just multiplication — no bending, no shifting.
In 1D, this is easy to imagine: multiplying a number by 2 stretches the space, and multiplying by -1 flips it.
For example, the transformation $x \mapsto 2x$ doubles $x$, and $x \mapsto -x$ reflects it across zero.

In 2D or 3D the same idea applies, but now we multiply a **vector** by a **matrix** instead of a single number.
This matrix controls how space is scaled, rotated, or sheared.
Formally, in $\mathbb R^n$, a linear transformation can be written as $\vec x \mapsto A\vec x$,
where $\vec x$ is a vector (or a point), and $A$ is a $n\times n$ matrix.

In 2D $A$ has for entries: $A = \begin{bmatrix}a&b\\c&d\end{bmatrix}$, so any 2D point $\begin{bmatrix}x\\y\end{bmatrix}$ is mapped to $\begin{bmatrix}ax+by\\cx+dy\end{bmatrix}$, since
$\begin{bmatrix}a&b\\c&d\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix} = \begin{bmatrix}ax+by\\cx+dy\end{bmatrix}.$

Let us see few examples.

-----------

### Identity
The simplest 2D transformation is the identity:

$$
\begin{bmatrix}1&0\\0&1\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix} = \begin{bmatrix}x\\y\end{bmatrix}
$$

Here is an illustration: I took a colored 2D plane (an image), and applied the identity transformation to every point of the plane.
Without any surprise the image is unchanged.

![](camera/identity.png)

-----------

### Scaling

A scaling matrix stretches objects wider or taller.
For example, $\begin{bmatrix} 2 & 0 \\ 0 & 1/2 \end{bmatrix}$ stretches the x-axis by 2 and squishes the y-axis by $1/2$.
In fact, this matrix performs simple 1D multiplication to the coordinates independently one from another.


![](camera/scaling.png)

-----------

### Rotation

A 2D rotation matrix $\begin{bmatrix} \cos\theta & -\sin\theta \\  \sin\theta & \cos\theta  \end{bmatrix}$ rotates a point counterclockwise by angle $\theta$ around the orgin.
If we take $\theta = 90°$, the matrix becomes $\begin{bmatrix} 0 & -1 \\  1 & 0 \end{bmatrix}$,
so any 2D point $\begin{bmatrix}x\\y\end{bmatrix}$ is mapped to $\begin{bmatrix}-y\\x\end{bmatrix}$, as it can be seen in this illustration:


![](camera/rotation.png)

-----------

### Shear

A shear matrix slants shapes like melting jello.
For example, $\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$
  slants shapes horizontally, like tilting a rectangle into a parallelogram.


![](camera/shear.png)

-----------

These transformations are called linear because they preserve straight lines and keep the origin fixed.
Linear transformations have compact representation: a transformation like rotation or scaling in 3D can be represented with a small square matrix.
Moreover, we have the composability we were looking for. 
Suppose we have three different transformations $A_1, A_2$ and $A_3$ to be chained on every vertex $\vec x_i$ of the scene (i.e. to compute $A_3 \times A_2 \times A_1 \times \vec x_i$).
Note that the multiplication is associative, i.e. $A_3 \times (A_2 \times (A_1 \times \vec x_i)) = ((A_3 \times A_2) \times A_1) \times \vec x_i$,
therefore, we can precompute $A = A_3\times A_2 \times A_1$ and apply the matrix $A$ directly to the vertices by computing the product $A\times \vec x_i$.



-----------

## Affine transformations

Note that linear transformations always map the origin to the origin, since $A \vec 0 = \vec 0$.
But in graphics, we often need to move (translate) things - hence affine transformations are more general and more useful.


Formally, in $\mathbb R^n$, an affine transformation $T$ has form $T(\vec x)=A\vec x+\vec b$,
where $\vec x$ is a vector (or a point), $A$ is a $n\times n$ matrix representing a linear transformation (like rotation, scaling or shear),
and $\vec b$ is a translation vector.

In 2D it looks like this:

$$
\begin{bmatrix}x\\y\end{bmatrix} \quad \mapsto \quad \begin{bmatrix}a&b\\c&d\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix} + \begin{bmatrix}e\\f\end{bmatrix} = \begin{bmatrix}ax+by+e\\cx+dy+f\end{bmatrix}
$$


This expression is really cool.
We can rotate, scale, shear and translate.
However, let us recall that we are interested in composing multiple transformations. 
Here is what a composition of two transformations looks like (remember, we need to compose dozens of those):

<!--

$$
\vec x \mapsto
A_2
\left(A_1 \vec x + \vec b_1\right)
+\vec b_2
$$

-->

$$
\begin{bmatrix}x\\y\end{bmatrix} \quad \mapsto \quad \begin{bmatrix}a_2&b_2\\c_2&d_2\end{bmatrix}
\left(\begin{bmatrix}a_1&b_1\\c_1&d_1\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix} + \begin{bmatrix}e_1\\f_1\end{bmatrix}\right)
+\begin{bmatrix}e_2\\f_2\end{bmatrix}
$$

It is starting to look ugly even for a single composition, add more and things get even worse.


-----------

##  Homogeneous Coordinates
Okay, now it is the time for the black magic. Imagine that I add one column and one row to our transformation matrix (thus making it 3x3 for a 2D transformation and 4x4 for 3D) and append one coordinate always equal to 1 to our vector to be transformed:


$$
\begin{bmatrix}
T(\vec{x}) \\
1
\end{bmatrix}
=
\begin{bmatrix}
A & \vec{b} \\
\vec{0}^\top & 1
\end{bmatrix}
\begin{bmatrix}
\vec{x} \\
1
\end{bmatrix}
$$


Let us write it down explicitly for 2D:

$$
\begin{bmatrix}a&b&e\\c&d&f\\0&0&1\end{bmatrix}\begin{bmatrix}x\\y\\1\end{bmatrix} = \begin{bmatrix}ax+by+e\\cx+dy+f\\1\end{bmatrix}
$$

This matrix captures the entire transformation and is easy to store and manipulate.
If we multiply this matrix and the vector augmented by 1 we get another vector with 1 in the last component, but the other two components have exactly the shape we would like! Magic.

In fact, the idea is really simple. Translations are not linear in the 2D space. So we embed our 2D into 3D space (by simply adding 1 for the 3rd component).
It means that our 2D space is the plane $z=1$ in the 3D space. Then we perform a linear 3D transformation and project the result onto our 2D physical plane. 
How do we project 3D back onto the 2D plane? Simply by dividing by the third component:

$$
\begin{bmatrix}x\\ y\\ z\end{bmatrix} \quad \mapsto \quad \begin{bmatrix}x/z \\ y/z\end{bmatrix}
$$

In the above example the 3rd component is always 1 independently from $A$ and $\vec b$, but very soon we will meet other cases.
In fact, we have just used **homogeneous coordinates**.
They are called *homogeneous* because of the way they use ratios of coordinates that remain consistent under scaling - a key idea from projective geometry.

In the process I described, a point $(x, y)$ in Cartesian coordinates becomes $(x, y, 1)$ in homogeneous coordinates.
More generally, a 2D point $(x, y)$ is represented as:

$$
(x, y) \quad \mapsto \quad (wx, wy, w)
$$

where $w \ne 0$, and the point in Cartesian coordinates is recovered by:

$$
\left(\frac{wx}{w}, \frac{wy}{w}\right) = (x, y)
$$

So any scalar multiple of $(x, y, 1)$ — like $(2x, 2y, 2)$, or $(5x, 5y, 5)$ — represents the same point in the plane. That's the essence of homogeneity different triples represent the same point because they are all scalar multiples.

In computer graphics, we extend affine transformations into matrix form using homogeneous coordinates allowing all transformations (including translation) to be expressed as a single matrix.
This is why we often use 3×3 matrices in 2D and 4×4 matrices in 3D graphics.
While being strange at the first sight, the approach is very straightforward, and it offers two serious advantages:

1. **Translation becomes matrix multiplication.**
   Affine transformations (like translation) are not linear in Cartesian coordinates but are linear in homogeneous coordinates, thus allowing for the composability we were looking for.
2. **Enables perspective projection.**
   Homogeneous coordinates naturally handle perspective division, which is key for realistic rendering of 3D scenes (we will revisit it shortly).
   Therefore, all camera handling (rotation, scaling, translation, projection) can be done within the same consistent framework.


## Chain of coordinate transformations

So, let us sum up.
Our models (characters, for example) are created in their own local frame (**object coordinates**).
They are placed into a scene expressed in **world coordinates**.
The transformation from one to another is made with matrix **Model**.
Then, we want to express it in the camera frame (**eye coordinates**), the transformation is called **View**.
Then, we deform the scene to create a perspective deformation with **Projection** matrix, this matrix transforms the scene to so-called clip coordinates.
Finally, we draw the scene, and the matrix transforming clip coordinates to the screen coordinates is called Viewport.




## Change of basis in 3D space

In Euclidean space, coordinates can be given by a point (the origin) and a basis. What does it mean that point $P$ has coordinates $(x,y,z)$ in the frame $(O, \vec i,\vec j,\vec k)$?
It means that the vector $\overrightarrow{OP}$ can be expressed as follows:

$$
\overrightarrow{OP} = \vec{i}x + \vec{j}y + \vec{k}z = \begin{bmatrix}\vec{i} & \vec{j} & \vec{k}\end{bmatrix}\begin{bmatrix}x \\ y \\ z\end{bmatrix}
$$

Now image that we have another frame $(O', \vec i',\vec j',\vec k')$.
How do we transform coordinates given in one frame to another?
First of all let us note that since $(\vec i,\vec j,\vec k)$ and $(\vec i', \vec j',\vec k')$ are bases of 3D, there exists a (non degenerate) matrix $M$ such that:

$$
\begin{bmatrix}\vec{i'} & \vec{j'} & \vec{k'}\end{bmatrix} =
\begin{bmatrix}\vec{i} & \vec{j} & \vec{k}\end{bmatrix} \times M
$$

Let us draw an illustration:


![](camera/basis_change.svg)

Then let us re-express the vector OP:

$$
\overrightarrow{OP} = \overrightarrow{OO'} + \overrightarrow{O'P} = 
\begin{bmatrix}\vec{i} & \vec{j} & \vec{k}\end{bmatrix}
\begin{bmatrix}O'_x \\ O'_y \\ O'_z\end{bmatrix} + 
\begin{bmatrix}\vec{i'} & \vec{j'} & \vec{k'}\end{bmatrix} 
\begin{bmatrix}x' \\ y' \\ z'\end{bmatrix} 
$$

Now let us substitute (i',j',k') in the right part with the change of basis matrix:


$$
\overrightarrow{OP} =
\begin{bmatrix}\vec{i} & \vec{j} & \vec{k}\end{bmatrix}\left(
\begin{bmatrix}O'_x \\ O'_y \\ O'_z\end{bmatrix} + 
 M \begin{bmatrix}x' \\ y' \\ z'\end{bmatrix} \right)
$$

And it gives us the formula to transform coordinates from one frame to another:



$$
 \begin{bmatrix}x \\ y \\ z\end{bmatrix} = 
\begin{bmatrix}O'_x \\ O'_y \\ O'_z\end{bmatrix} + 
 M \begin{bmatrix}x' \\ y' \\ z'\end{bmatrix} 
 \qquad\Rightarrow\qquad
 \begin{bmatrix}x' \\ y' \\ z'\end{bmatrix}  =
M^{-1}\left( \begin{bmatrix}x \\ y \\ z\end{bmatrix} - \begin{bmatrix}O'_x \\ O'_y \\ O'_z\end{bmatrix}\right)
$$


## Let us create our own gluLookAt

Camera is defined via view parameters $\text{eye}$, $\text{center}$ and $\overrightarrow{\text{up}}$, measured in world space.
It is located at  $\text{eye}$, pointing at $\text{center}$, with upward orientation towards $\overrightarrow{\text{up}}$.
In camera space, the camera is located at the axis $\vec{k}$, pointing at the origin, and vector $\overrightarrow{\text{up}}$ is vertical.


In 3D graphics, we position the camera onto the world space by specifying three view parameters: EYE, AT and UP, in world space.

The point EYE (ex, ey, ez) defines the location of the camera.
The vector AT (ax, ay, az) denotes the direction where the camera is aiming at, usually at the center of the world or an object.
The vector UP (ux, uy, uz) denotes the upward orientation of the camera roughly. UP is typically coincided with the y-axis of the world space. UP is roughly orthogonal to AT, but not necessary. As UP and AT define a plane, we can construct an orthogonal vector to AT in the camera space.



OpenGL and, as a consequence, our tiny renderer are able to draw scenes only with the camera located on the z-axis. If we want to move the camera, no problem, we can move all the scene, leaving the camera immobile.

Let us put the problem this way: we want to draw a scene with a camera situated in point e (eye), the camera should be pointed to the point c (center) in such way that a given vector u (up) is to be vertical in the final render.

Here is an illustration:

![](camera/glulookat.svg)

It means that we want to do the rendering in the frame (c, x',y',z'). But then our model is given in the frame (O, x,y,z)... No problem, all we need is to compute the transformation of the coordinates. Here is a C++ code computing the necessary 4x4 matrix ModelView:


```cpp
void lookat(const vec3 eye, const vec3 center, const vec3 up) {
    vec3 z = normalized(center-eye);
    vec3 x = normalized(cross(up,z));
    vec3 y = normalized(cross(z, x));
    ModelView = mat<4,4>{{{x.x,x.y,x.z,0}, {y.x,y.y,y.z,0}, {z.x,z.y,z.z,0}, {0,0,0,1}}} *
                mat<4,4>{{{1,0,0,-eye.x},  {0,1,0,-eye.y},  {0,0,1,-eye.z},  {0,0,0,1}}};
}
```

Note that z' is given by the vector ce (do not forget to normalize it, it helps later). How do we compute x'? Simply by a cross product between u and z'. Then we compute y', such that it is orthogonal to already calculated x' and z' (let me remind you that in our problem settings ce and u are not necessarily orthogonal). The very last step is a translation of the origin to the point of viewer e and our transformation matrix is ready. Now it suffices to get any point with coordinates (x,y,z,1) in the model frame, multiply it by the matrix ModelView and we get the coordinates in the camera frame! By the way, the name ModelView comes from OpenGL terminology.


## Viewport

$$
\begin{bmatrix}\frac{w}{2}&0&0&x+\frac{w}{2} \\ 0&\frac{h}{2}&0&y+\frac{h}{2}\\ 0&0&\frac{d}{2}&\frac{d}{2}\\ 0 &0 &0&1\end{bmatrix}
$$


```cpp
void viewport(const int x, const int y, const int w, const int h) {
    Viewport = {{{w/2., 0, 0, x+w/2.}, {0, h/2., 0, y+h/2.}, {0,0,1,0}, {0,0,0,1}}};
}
```

```cpp
void projection(const double f) {
    Projection = {{{1,0,0,0}, {0,-1,0,0}, {0,0,1,0}, {0,0,-1/f,0}}};
}
```



--8<-- "comments.html"

