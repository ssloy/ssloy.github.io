import numpy as np

g     = -9.81 # gravity, m/s^2
speed = 30    # initial speed (m/s)
angle = 45    # launch angle in degrees

x, y = 0, 0   # current state
vx, vy = speed * np.cos(angle * np.pi/180), \
         speed * np.sin(angle * np.pi/180)

dt = 1
xs, ys = [x], [y]
while y >= 0:
    x += dt * vx
    y += dt * vy
    vy += g * dt
    xs.append(x)
    ys.append(y)

u = ys[-2]/(ys[-2]-ys[-1])
xs[-1] = xs[-2] + u*(xs[-1]-xs[-2])
ys[-1] = 0

import matplotlib.pyplot as plt
plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=24)
plt.title('The ape detects the ground')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.plot(xs, ys, marker='.')
plt.plot(xs, [0]*len(xs))
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.gca().set_aspect('equal', 'box')
plt.savefig("plot-event.png")
plt.show()

