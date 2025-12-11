import random
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

def f(s,p):
    return np.hstack((s[2:], (np.array([p[1], 0]) - s[2:])/p[0] + np.array([0, p[2]])))

def Fs(s, p):
    return np.array([[0, 0, 1, 0],
                     [0, 0, 0, 1],
                     [0, 0, -1/p[0], 0],
                     [0, 0, 0, -1/p[0]]])
def Fp(s, p):
    return np.array([[0, 0, 0],
                     [0, 0, 0],
                     [(s[2]-p[1])/p[0]**2, 1/p[0], 0],
                     [s[3]/p[0]**2, 0, 1]])

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

'''
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

plt.plot(gtx, gty, 'b')
plt.plot(rk1x, rk1y, 'r+')
plt.plot(rk2x, rk2y, 'g+')
plt.show()

'''

nsamples = 30
random.seed(1337)
traj = []

for _ in range(nsamples):
    t = random.uniform(0, time_of_flight)
    traj.append((t, gt(t)))
traj = sorted(traj, key= lambda x: x[0])

'''
xs, ys = zip(*(p for _, p in traj))
plt.scatter(xs, ys)

p = np.array([tau, w[0], g[1]])
p = np.array([10., 0., -10.])
for _ in range(100):
    rk2x = [x0[0]]
    rk2y = [x0[1]]

    S = np.zeros((4,3))
    s = np.hstack((x0, v0))
    t = 0

    A = np.zeros((2, 3))
    b = np.array([0., 0.])

    for ti,si in traj:
        dt = ti - t
        t = ti

        sm = s + dt/2. * f(s,p)
        s += dt*f(sm, p)

        Sm = S + dt/2. * (Fs(s, p) @ S + Fp(s, p))
        S = S + dt * (Fs(sm, p) @ Sm + Fp(sm, p))

        A = np.vstack((A, S[:2]))
        b = np.hstack((b, s[:2] - si))

        rk2x.append(s[0])
        rk2y.append(s[1])

    plt.plot(rk2x, rk2y)


    dp = (-np.linalg.inv(np.transpose(A)@A) @ np.transpose(A) @ b) / max([np.linalg.norm(b)/10, 1])
    p += dp
    print(dp)

print(p)
plt.show()
'''

maxnorm = 1e20

for tau in np.linspace(.1, 10, 50):
    for wx in np.linspace(-100, 100, 50):
        for g in np.linspace(0, -100, 50):
            p = np.array([tau, wx, g])
            s = np.hstack((x0, v0))
            t = 0
            b = np.array([0., 0.])
            for ti,si in traj:
                dt = ti - t
                t = ti
                sm = s + dt/2. * f(s,p)
                s += dt*f(sm, p)
                b = np.hstack((b, s[:2] - si))
                norm = np.linalg.norm(b)
                if maxnorm>norm:
                    print(norm, p)
                    maxnorm = norm



