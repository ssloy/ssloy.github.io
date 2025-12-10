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
#   return np.hstack((
#           x0 + t*(w + m/mu*g) + m/mu*(v0 - w - m/mu*g)*(1-np.exp(-t*mu/m)),
#           w + m/mu*g + (v0 - w - m/mu*g)*np.exp(-t*mu/m)
#           ))

def fit(traj):
#    p = np.array([tau, w[0], w[1], g[1]])
    p = np.array([10., 0., -10.])
    p = np.array([  9.15604053, -75.31675916, -10.25633558])

    for _ in range(10):
        S = np.zeros((4,3))
        s = np.hstack((x0, v0))
        dt = 0.001

        j = 0
        t = 0.
        grad = np.zeros(3)

        x = [x0[0]]
        y = [x0[1]]
        A = None
        b = None
        while j<len(traj):
            t += dt
            s = s + dt * np.hstack((s[2:], (np.array([p[1], 0]) - s[2:])/p[0] + np.array([0, p[2]])))
            S = np.array([[1, 0, dt, 0],
                          [0, 1, 0, dt],
                          [0, 0, 1-dt/p[0], 0],
                          [0, 0, 0, 1-dt/p[0]]]) @ S + \
                    dt*np.array([[0,0,0],
                                 [0,0,0],
                                 [(s[2]-p[1])/p[0]**2, 1/p[0], 0],
                                 [s[3]/p[0]**2, 0, 1]])
            if t>traj[j][0]:
                sm = traj[j][1]
                if A is None:
                   A = np.copy(S[:2])
                   b = s[:2] - sm
                else:
                   A = np.vstack((A, S[:2]))
                   b = np.hstack((b, s[:2]-sm))

                grad += np.transpose(S[:2]) @ (s[:2] - sm)
                x.append(s[0])
                y.append(s[1])
                j += 1

#        grad /= np.linalg.norm(grad)
#        p -=  grad
        p -= np.linalg.inv(np.transpose(A)@A) @ np.transpose(A) @ b
        print(p)
    plt.plot(x, y)

#       grad = np.transpose(S) @ (s-sm)
#       grad /= np.linalg.norm(grad)
#       print(s-sm, p)
#       p -= 0.1 * grad 
#       if (p[0]<.01): p[0] = .01
#        p -= np.linalg.inv(np.transpose(S)@S) @ np.transpose(S) @ (s - sm)
#        print(p)
#    print(x, s)
#    print(S)


time_of_flight = 3
nsamples = 30
random.seed(1337)
traj = []

for _ in range(nsamples):
    t = random.uniform(0, time_of_flight) 
    x = x0 + t*(w + m/mu*g) + m/mu*(v0 - w - m/mu*g)*(1-np.exp(-t*mu/m))
    traj.append((t, x))

traj = sorted(traj, key= lambda x: x[0]) 

xs, ys = zip(*(p for _, p in traj))
fit(traj)

plt.scatter(xs, ys)
plt.show()


