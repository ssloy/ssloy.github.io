import numpy as np

g     = -9.81 # gravity, m/s^2
angle = 60    # launch angle, degrees wrt the ground
xstar = 30

def simulate(speed):
    x, y = 0, 0   # current state
    vx, vy = speed * np.cos(angle * np.pi/180), \
             speed * np.sin(angle * np.pi/180)
    dt = .001
    xs, ys = [x], [y]
    while x < xstar and y>=0:
        x += dt * vx
        y += dt * vy
        vy += g * dt
        xs.append(x)
        ys.append(y)
    if y>0:
        u = (xstar-xs[-2])/(xs[-1]-xs[-2])
        xs[-1] = xstar
        ys[-1] = ys[-2] + u*(ys[-1]-ys[-2])
    return xs, ys

v = []
yrange = []
for v0 in np.linspace(0., 80., 100):
    xs,ys = simulate(v0)
    if xs[-1] == xstar:
        yrange.append(ys[-1])
        v.append(v0)

import matplotlib.pyplot as plt
plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=34)
plt.title(f'Shooting height at the skyscraper from ${xstar}$ m, $\\theta = {angle}^\\circ$')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.plot(v, yrange,linewidth=2)
#plt.plot(xs, [0]*len(xs))
plt.xlabel("$v_0$, meters per second")
plt.ylabel("height, meters")
#plt.gca().set_aspect('equal', 'box')
plt.savefig("plot-y-range.png")
plt.show()

