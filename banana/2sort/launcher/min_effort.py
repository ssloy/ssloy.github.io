import numpy as np
import matplotlib.pyplot as plt

import numpy as np

g     = -9.81 # gravity, m/s^2
x_star, y_star = 34.710114278058825, 31.330622944200034


def simulate(vx0, vy0, g, dt):
    t, x, y, vx, vy = 0, 0, 0, vx0, vy0
    ts, xs, ys = [t], [x], [y]
    while y >= 0:
        x  += dt * vx
        y  += dt * vy
        vy += dt * g
        t  += dt
        ts.append(t)
        xs.append(x)
        ys.append(y)

#    plt.plot(xs, ys, alpha=.3)
    return [ts, xs, ys]

def miss_distance_sq(vx0, vy0, g, dt, x_star, y_star):
    _, xs, ys = simulate(vx0, vy0, g, dt)
    return min([(x - x_star)**2 + (y - y_star)**2 for x, y in zip(xs, ys)])

def objective(vx0, vy0, g, dt, x_star, y_star):
    effort = vx0**2 + vy0**2
    miss = miss_distance_sq(vx0, vy0, g, dt, x_star, y_star)
    return effort + 10000 * miss

dt = 0.001

best = np.inf
best_v = None

for vx in np.linspace(0, 30, 300):
    for vy in np.linspace(0, 30, 300):
        val = objective(vx, vy, g, dt, x_star, y_star)
        if val < best:
            best = val
            best_v = (vx, vy)

_, xs, ys = simulate(best_v[0], best_v[1], g, dt)

print(best, best_v)
plt.plot(xs, ys)
plt.scatter(x_star, y_star)



'''
VX, VY = np.meshgrid(np.linspace(0, 50, 100),
                   np.linspace(0, 50, 100))

Z = np.zeros_like(VX)
for i in range(VX.shape[0]):
    for j in range(VX.shape[1]):
        Z[i, j] = objective(VX[i,j], VY[i,j], g, dt, x_star, y_star)

contour = plt.contourf(VX, VY, np.log(Z + 1e-8))
plt.colorbar(contour, label='Objective J(vx, vy)')
'''

plt.show()


