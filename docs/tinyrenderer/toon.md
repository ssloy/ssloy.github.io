# Bonus: toon shading

##  Attention, work in progress

<!--
##  Sobel edge detection

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

-->

--8<-- "comments.html"

