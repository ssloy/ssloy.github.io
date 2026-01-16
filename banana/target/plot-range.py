import numpy as np

g     = -9.81 # gravity, m/s^2
angle = 60    # launch angle, degrees wrt the ground

def simulate(speed):
    x, y = 0, 0   # current state
    vx, vy = speed * np.cos(angle * np.pi/180), \
             speed * np.sin(angle * np.pi/180)
    dt = .001
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
    return xs, ys

V = np.linspace(0., 30., 100)
range = [ simulate(v)[0][-1] for v in V ]

import matplotlib.pyplot as plt
plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=34)
plt.title(f'Shooting range with throw angle fixed at ${angle}^\\circ$')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.plot(V, range,linewidth=2)
#plt.plot(xs, [0]*len(xs))
plt.xlabel("$v_0$, meters per second")
plt.ylabel("range, meters")
#plt.gca().set_aspect('equal', 'box')
plt.savefig("plot-range.png")
plt.show()

