import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

g     = -9.81 # gravity, m/s^2
x_star, y_star = 34, 23

def distance_point_parabola(x0, y0, a, b):
    """
    Distance from point (x0,y0) to parabola y = a x^2 + b x.
    Returns (distance, closest_x, closest_y).
    """

    # Cubic coefficients
    A = 2 * a * a
    B = 3 * a * b
    C = b * b - 2 * a * y0 + 1
    D = -(b * y0 + x0)

    # Solve cubic
    roots = np.roots([A, B, C, D])

    # Keep real roots only
    real_roots = roots[np.isclose(roots.imag, 0)].real

    # Evaluate distance for each candidate
    best_dist = np.inf
    best_x = None

    for x in real_roots:
        y = a * x * x + b * x
        d = np.hypot(x - x0, y - y0)
        if d < best_dist:
            best_dist = d
            best_x = x

    best_y = a * best_x * best_x + b * best_x
    return best_dist #, best_x, best_y


#plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=36)
'''
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.plot(xs, ys, marker='.')
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.gca().set_aspect('equal', 'box')
plt.savefig("plot-euler.png")
plt.show()
'''

VX, VY = np.meshgrid(np.linspace(.01, 50, 300),
                     np.linspace(.01, 50, 300))
fig, axes = plt.subplots(1, 3, figsize=(32, 12))

fig.suptitle("Hit a target with least effort:\n unconstrained minimization", fontsize=48)

Z1 = np.zeros_like(VX)
for i in range(VX.shape[0]):
    for j in range(VX.shape[1]):
        vx,vy = VX[i,j],VY[i,j]
        Z1[i, j] = np.hypot(vx, vy)

Z2 = np.zeros_like(VX)
for i in range(VX.shape[0]):
    for j in range(VX.shape[1]):
        vx,vy = VX[i,j],VY[i,j]
        Z2[i, j] = distance_point_parabola(x_star, y_star, g/2/vx**2, vy/vx)

Z3 = np.zeros_like(VX)
for i in range(VX.shape[0]):
    for j in range(VX.shape[1]):
        vx,vy = VX[i,j],VY[i,j]
        Z3[i, j] = (distance_point_parabola(x_star, y_star, g/2/vx**2, vy/vx)*4  + np.sqrt(vx*vx + vy*vy))

contour = axes[0].contourf(VX, VY, Z1, levels=200, cmap='viridis')
divider = make_axes_locatable(axes[0])
cax = divider.append_axes("right", size="5%", pad=0.05)  # width 5% of ax, small padding
plt.colorbar(contour, cax=cax)
contour = axes[1].contourf(VX, VY, Z2, levels=200, cmap='viridis')
divider = make_axes_locatable(axes[1])
cax = divider.append_axes("right", size="5%", pad=0.05)  # width 5% of ax, small padding
plt.colorbar(contour, cax=cax)

contour = axes[2].contourf(VX, VY, Z3, levels=200, cmap='viridis')

divider = make_axes_locatable(axes[2])
cax = divider.append_axes("right", size="5%", pad=0.05)  # width 5% of ax, small padding
plt.colorbar(contour, cax=cax)
axes[0].contour(VX, VY, Z1, levels=5, colors='silver', linewidths=0.8, linestyles='dashed')
axes[1].contour(VX, VY, Z2, levels=5, colors='silver', linewidths=0.8, linestyles='dashed')
axes[2].contour(VX, VY, Z3, levels=5, colors='silver', linewidths=0.8, linestyles='dashed')


axes[0].set_title("$\\sqrt{v_{x,0}^2 + v_{y,0}^2}$", fontsize=32)
axes[0].set_xlabel('$v_{x,0}$')
axes[0].set_ylabel('$v_{y,0}$')

axes[1].set_title("$\\min_i \\sqrt{(x^*-x_i)^2 + (y^* - y_i)^2}$", fontsize=32)
axes[1].set_xlabel('$v_{x,0}$')
axes[1].set_ylabel('$v_{y,0}$')

axes[2].set_title("$\\sqrt{v_{x,0}^2 + v_{y,0}^2} + \\lambda \\cdot \\min_i \\sqrt{(x^*-x_i)^2 + (y^* - y_i)^2}$", fontsize=32)
axes[2].set_xlabel('$v_{x,0}$')
axes[2].set_ylabel('$v_{y,0}$')


axes[0].set_aspect('equal')
axes[1].set_aspect('equal')
axes[2].set_aspect('equal')
plt.tight_layout()


plt.savefig("plot3.png")
plt.show()

