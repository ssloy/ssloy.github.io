import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.gridspec import GridSpec

g     = -9.81 # gravity, m/s^2
speed = 30.   # initial speed (m/s)
angle = 45.   # launch angle in degrees

t = 0
x, y = 0., 0.
vx, vy = speed * np.cos(angle * np.pi/180.0), \
         speed * np.sin(angle * np.pi/180.0)

ts, xs, ys = [0.], [x], [y]
dt = 0.01

while y >= 0:
    x += dt * vx
    y += dt * vy
    vy += g * dt
    t += dt
    ts.append(t)
    xs.append(x)
    ys.append(y)


'''
plt.plot(xs, ys, label="Euler integration", marker='.')
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal', 'box')
plt.show()
'''

# --- Plot ---

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True
plt.rc('font', size=16)


fig = plt.figure(figsize=(16, 9))
gs = GridSpec(3, 2, width_ratios=[2, 1], height_ratios=[1, 1, 1], figure=fig)

# 3D curve x(t), y(t), t
ax3d = fig.add_subplot(gs[:, 0], projection='3d', proj_type='persp', focal_length=0.18)
ax3d.view_init(elev=10, azim=-120)
ax3d.plot(xs, ts, ys, color='black', lw=3)
ax3d.plot([0]*len(xs), ts, ys, 'g')
ax3d.plot(xs, ts, [0]*len(ys), 'r')
ax3d.plot(xs, [0]*len(ts), ys, 'b')
ax3d.set_xlabel("$x$", fontsize=24)
ax3d.set_ylabel("$t$", fontsize=24)
ax3d.set_zlabel("$y$", fontsize=24)
ax3d.set_title("3D trajectory: $x,y,t$", fontsize=32, y=0.9)
ax3d.set_xlim(0, max(xs))
ax3d.set_ylim(0, max(ts))
ax3d.set_zlim(0, max(ys))
ax3d.zaxis.set_pane_color([1, 0.9, 0.9, 0.5])  # light red, semi-transparent
ax3d.xaxis.set_pane_color([0.9, 1, 0.9, 0.5])  # light green
ax3d.yaxis.set_pane_color([0.9, 0.9, 1, 0.5])  # light blue
ax3d.xaxis._axinfo['grid'].update(color='gray', linestyle='--', linewidth=0.5)
ax3d.yaxis._axinfo['grid'].update(color='gray', linestyle='--', linewidth=0.5)
ax3d.zaxis._axinfo['grid'].update(color='gray', linestyle='--', linewidth=0.5)

# projection: x-t
ax_xt = fig.add_subplot(gs[0, 1])
ax_xt.plot(ts, xs, 'r')
ax_xt.set_xlabel("$t$")
ax_xt.set_ylabel("$x$")
ax_xt.set_title("$x(t)$", fontsize=24)
ax_xt.grid(color='gray', linestyle='--', linewidth=0.5)


# projection: y-t
ax_yt = fig.add_subplot(gs[1, 1])
ax_yt.plot(ts, ys, 'g')
ax_yt.set_xlabel("$t$")
ax_yt.set_ylabel("$y$")
ax_yt.set_title("$y(t)$", fontsize=24)
ax_yt.grid(color='gray', linestyle='--', linewidth=0.5)

# projection: x-y
ax_xy = fig.add_subplot(gs[2, 1])
ax_xy.plot(xs, ys, 'b')
ax_xy.set_xlabel("$x$")
ax_xy.set_ylabel("$y$")
ax_xy.set_title("$y(x)$", fontsize=24)
ax_xy.grid(color='gray', linestyle='--', linewidth=0.5)

plt.tight_layout()
plt.savefig("plot3d.png")
plt.show()

