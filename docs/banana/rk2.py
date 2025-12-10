import numpy as np
import matplotlib.pyplot as plt

m  = 0.5           # banana mass, kg
mu = 0.1           # kg/s (linear drag coefficient)
tau = m/mu

g = np.array([0, -9.81]) # gravity, m/s^2
w = np.array([-40, 0])   # wind,    m/s

speed = 30.0  # initial speed (m/s)
theta = 40.0  # launch angle in degrees
v0 = np.array([speed * np.cos(theta * np.pi/180.0),
               speed * np.sin(theta * np.pi/180.0) ])
x0 = np.array([0., 0.])

def gt(t):
    return x0 + t*(w + m/mu*g) + m/mu*(v0 - w - m/mu*g)*(1-np.exp(-t*mu/m))

def f(s):
    return np.hstack((s[2:], (w - s[2:])/tau + g))

ta = 0.
tb = 1.
while gt(tb)[1] > 0: # bracketing
    tb *= 2

while tb-ta > 1e-3:  # bisection
    tm = (ta + tb)/2.
    if gt(tm)[1] > 0:
        ta = tm
    else:
        tb = tm

time_of_flight = (ta + tb)/2.

gtx = [x0[0]]
gty = [x0[1]]
rk1x = [x0[0]]
rk1y = [x0[1]]
rk2x = [x0[0]]
rk2y = [x0[1]]

dt = .1
t = 0
rk1s = np.hstack((x0, v0))
rk2s = np.hstack((x0, v0))

while t < time_of_flight:
    t += dt

    rk1s += dt*f(rk1s)
    rk1x.append(rk1s[0])
    rk1y.append(rk1s[1])

    rk2m = rk2s + dt/2. * f(rk2s)
    rk2s += dt*f(rk2m)

    rk2x.append(rk2s[0])
    rk2y.append(rk2s[1])

    gts = gt(t)
    gtx.append(gts[0])
    gty.append(gts[1])

plt.plot(gtx, gty)
plt.plot(rk1x, rk1y, 'r-')
plt.plot(rk2x, rk2y, 'g-')
plt.show()


