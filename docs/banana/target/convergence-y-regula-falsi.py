import numpy as np
import matplotlib.pyplot as plt
import random
random.seed(1)

plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=34)
plt.title(f'Convergence of the regula falsi method')
plt.grid(color='gray', linestyle='--', linewidth=0.5)

g     = -9.81 # gravity, m/s^2
angle = 60    # launch angle, degrees wrt the ground
xstar = 30

def y_impact(v0):
    x, y = 0, 0   # current state
    vx, vy = v0 * np.cos(angle * np.pi/180), \
             v0 * np.sin(angle * np.pi/180)
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
    return ys[-1]

bananas_max = -1
for _ in range(128):
    ystar = random.uniform(1, 50)
    a, b = 18, 100
    fa, fb = y_impact(a), y_impact(b)
    err = []
    while True:
        u = (ystar-fa)/(fb-fa)
        m = a + u*(b-a)
        y = y_impact(m)
        if y < ystar:
            a = m
            fa = y
        else:
            b = m
            fb = y
        err.append(abs(y-ystar))
        if err[-1] < 1e-3:
            v0 = m
            break
    bananas_max = max(bananas_max, len(err))
    plt.plot(range(1,len(err)+1), err,c='gray',alpha=.1)

plt.text(8, 20, f'max throws to hit the target: {bananas_max}', dict(size=30))
plt.ylim((1e-4,50))
plt.xlim((0,15))
plt.xlabel("Number of bananas launched")
plt.ylabel("Distance to the target, meters")
plt.yscale('log')

#plt.gca().set_aspect('equal', 'box')
plt.savefig("convergence-y-regula-falsi.png")
plt.show()

