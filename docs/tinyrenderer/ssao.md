---
title: Ambient occlusion
---

# (Attention, work in progress) Ambient occlusion

In the classical Phong reflection model, the ambient term is often represented as a simple constant added to the shading equation.
This constant acts as a crude approximation of indirect lighting: it prevents regions not directly lit by any source from appearing completely black.
While effective for real-time rendering, this approach lacks realism because it does not account for the actual geometry of the scene and how much of the surrounding light can reach a given point.

A more physically motivated idea is to consider global illumination, where light is allowed to bounce and scatter between surfaces.
One practical approximation of this idea is ambient occlusion (AO).
Instead of assuming a uniform ambient term everywhere, AO measures how much of the hemisphere around a point is blocked by nearby geometry.
Points in narrow crevices or under overhangs appear darker, while exposed points on open surfaces remain brighter.
This creates the perception of depth and realism, even without fully simulating indirect light transport.

A simple way to approximate ambient occlusion is by extending the concept of shadow mapping.
In standard shadow mapping, we determine whether a point is visible from a light source, producing a binary "in shadow" or "lit" decision.
For ambient occlusion, we could imagine rendering many such shadow maps from different directions across the hemisphere around a point, each one giving us a hard shadow.
By averaging the results of many such "virtual shadow tests," we obtain a continuous measure of how occluded a point is by its surroundings.
This technique transforms the idea of a constant ambient term into a geometry-aware shading effect, bridging the gap between Phong’s local model and global illumination.

[![](ssao/teaser.jpg)](ssao/teaser.jpg)

![](ssao/samples.jpg)

# Screen-space ambient occlusion

## Bonus: Sobel edge detection

Think of a row of pixel intensities as of a 1D signal.
In 1D, edge detection is just about finding changes in signal intensity.
An edge is where the signal changes quickly.

The simplest way:

    Look at the left neighbor and the right neighbor.

    Subtract them.

That’s exactly what the 1D Sobel filter [-1, 0, +1] does:

    Multiply left pixel by -1

    Ignore the center

    Multiply right pixel by +1

    Add them up → big value if there’s a jump, small if flat.



In 2D images, we care about changes in intensity along x and y directions: edges can go horizontally or vertically.


Sobel defines two 3×3 convolution kernels:


    Gxemphasizes horizontal changes (edges vertical in the image).

    Gy emphasizes vertical changes (edges horizontal in the image).

The final gradient magnitude is:


So Sobel uses two small 3×3 grids:

    Horizontal edges (changes left↔right):

-1  0  +1
-2  0  +2
-1  0  +1

    Vertical edges (changes up↔down):

-1 -2 -1
 0  0  0
+1 +2 +1

Then we combine them:

    Gx = how strong the left↔right change is.

    Gy = how strong the up↔down change is.

    Edge strength = sqrt(Gx² + Gy²).


--8<-- "comments.html"

