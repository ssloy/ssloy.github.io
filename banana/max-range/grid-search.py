import matplotlib.pyplot as plt
import numpy as np

g     = -9.81 # gravity, m/s^2
speed = 30    # initial speed (m/s)

def simulate(angle):
    x, y = 0, 0   # current state
    vx, vy = speed * np.cos(angle * np.pi/180), \
             speed * np.sin(angle * np.pi/180)
    dt = .01
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
    plt.plot(xs, ys)
    return xs, ys

plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=24)
plt.title('Grid search: running out of bananas')
plt.grid(color='gray', linestyle='--', linewidth=0.5)

angles = np.linspace(0., 90., 100)
range = [ simulate(a)[0][-1] for a in angles ]

#plt.plot(angles, range)
#plt.plot(xs, [0]*len(xs))
plt.xlabel("$x$")
plt.ylabel("$y$")
#plt.gca().set_aspect('equal', 'box')
plt.savefig("plot-grid.png")
plt.show()

