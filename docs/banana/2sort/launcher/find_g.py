import numpy as np
import matplotlib.pyplot as plt

from launcher import *

speed = 30    # initial speed, m/s
angle = 45    # launch angle in degrees

vx0, vy0 = speed * np.cos(angle * np.pi/180), \
           speed * np.sin(angle * np.pi/180)

t_meas, x_meas, y_meas = Launcher.launch(vx0, vy0)

def simulate(g, rk2=False):
    t, x, y, vx, vy = 0, 0, 0, vx0, vy0
    ts, xs, ys = [t], [x], [y]
#    t_max = max(t_meas)
    dt = .25
    while True: #t < t_max:
        x  += dt * vx
        if rk2:
            y += dt * (vy + dt/2 * g)
        else:
            y  += dt * vy

        vy += dt * g
        t  += dt

        if y < 0:
            t = ts[-1]/(ts[-1] - y)
            x = xs[-1] + t * (x - xs[-1])
            y = 0
#            ts.append(ts[-1])
            xs.append(x)
            ys.append(y)
            break

        ts.append(t)
        xs.append(x)
        ys.append(y)
    plt.plot(xs, ys, alpha=.3, marker='.')
    return [ts, xs, ys]

def cost(g):
    t_sim, x_sim, y_sim = simulate(g)
    x_sim = np.interp(t_meas, t_sim, x_sim) # interpolate simulated positions
    y_sim = np.interp(t_meas, t_sim, y_sim) # at the measurement times
    return np.sum((x_sim - x_meas)**2 + (y_sim - y_meas)**2)

'''
def grid_search(a, b):
    gs = np.linspace(a, b, int(100*(b-a)))
    costs = [ cost(g) for g in gs ]
    return gs[np.argmin(costs)]

g = grid_search(-20, 0)
print(g)
'''

def ternary_search(a, b):
    while b - a > 0.01:
        m1 = a + (b - a) / 3
        m2 = b - (b - a) / 3
        if cost(m1) > \
            cost(m2):
            a = m1
        else:
            b = m2
    return (a + b)/2

g = ternary_search(-20, 0)
print(g)

plt.clf()
simulate(g, True)
plt.scatter(x_meas,y_meas)
plt.grid(True)
plt.show()

