import numpy as np

g     = -9.81 # gravity, m/s^2
angle = 60    # launch angle, degrees wrt the ground
xstar = 42    # the distance to hit

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
    plt.plot(xs, ys)
    return xs[-1]


import matplotlib.pyplot as plt
plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=34)
plt.title(f'Targeting $x^*$={xstar} m with improved binary search')
plt.grid(color='gray', linestyle='--', linewidth=0.5)

bananas = 0
a, b = 0, 35
fa, fb = None, None
while True: # binary search
    bananas += 1
    if fa is None or fb is None:
        m = (a + b)/2
    else:
        u = (xstar-fa)/(fb-fa)
        m = a + u*(b-a)
    x = x_impact(m)
    if x < xstar:
        a = m
        fa = x
    else:
        b = m
        fb = x
    if abs(x-xstar)<0.1:
        v0 = m
        break
print(v0, x_impact(v0))
print(bananas, "bananas spent")

plt.xlabel("$x$, meters")
plt.ylabel("$y$, meters")
plt.gca().set_aspect('equal', 'box')
plt.savefig("hit-x-linear.png")
plt.show()

