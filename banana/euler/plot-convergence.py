import numpy as np
import matplotlib.pyplot as plt

g     = -9.81 # gravity, m/s^2
speed = 30.   # initial speed (m/s)
angle = 45.   # launch angle in degrees

def euler(dt):
    x, y = 0., 0.
    vx, vy = speed * np.cos(angle * np.pi/180.0), \
             speed * np.sin(angle * np.pi/180.0)

    xs, ys = [x], [y]
    while y >= 0:
        x += dt * vx
        y += dt * vy
        vy += g * dt
        xs.append(x)
        ys.append(y)
    return xs, ys

plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=24)

dt = 1
for _ in range(6):
    xs, ys = euler(dt)
    plt.plot(xs, ys, label=f'$\\Delta t = {dt}$', marker='.')
    dt /= 2

plt.gca().set_xlabel("$x$", fontsize=32)
plt.gca().set_ylabel("$y$", fontsize=32)
plt.legend()
plt.title('Convergence of Euler\'s schema as $\\Delta t \\to 0$')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.gca().set_aspect('equal', 'box')
plt.savefig("plot-convergence.png")
plt.show()

