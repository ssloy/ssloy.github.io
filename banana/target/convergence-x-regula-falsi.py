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
def x_impact(v0):
    x, y = 0, 0   # current state
    vx, vy = v0 * np.cos(angle * np.pi/180), \
             v0 * np.sin(angle * np.pi/180)
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
    return xs[-1]

for _ in range(100):
    xstar = random.uniform(1, 100)
    a, b = 0, 35
    fa, fb = x_impact(a), x_impact(b)
    err = []
    while True:
        u = (xstar-fa)/(fb-fa)
        m = a + u*(b-a)
        x = x_impact(m)
        if x < xstar:
            a = m
            fa = x
        else:
            b = m
            fb = x
        err.append(abs(x-xstar))
        if err[-1] < 1e-3:
            v0 = m
            break
    plt.plot(range(1,len(err)+1), err,c='gray',alpha=.1)

plt.ylim((1e-4,50))
plt.xlim((0,15))
plt.xlabel("Number of bananas launched")
plt.ylabel("Distance to the target, meters")
plt.yscale('log')

#plt.gca().set_aspect('equal', 'box')
plt.savefig("convergence-x-regula-falsi.png")
plt.show()

