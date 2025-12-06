import numpy as np
import matplotlib.pyplot as plt

m  = 0.5           # banana mass, kg
mu = 0.000001           # kg/s (linear drag coefficient)

g = np.array([0, -9.81]) # gravity, m/s^2
w = np.array([-10, 0])   # wind,    m/s

speed = 30.0  # initial speed (m/s)
theta = 40.0  # launch angle in degrees
v0 = np.array([speed * np.cos(theta * np.pi/180.0),
               speed * np.sin(theta * np.pi/180.0) ])
x0 = np.array([0., 0.])

x = np.copy(x0)
v = np.copy(v0)
dt = 0.1

X = [x[0]]
Y = [x[1]]
T = [0]
E = [m/2*np.dot(v, v)]

GTX = [x[0]]
GTY = [x[1]]

for _ in range(40):
    x += dt * v
    v += dt * (-mu / m*(v - w) + g)

#    E.append(x[1] + np.dot(v,v))

    T.append(T[-1]+dt)
    X.append(x[0])
    Y.append(x[1])

    t = T[-1]
    gtv = w + m/mu*g + (v0 - w - m/mu*g)*np.exp(-t*mu/m)
    gtx = x0 + t*(w + m/mu*g) + m/mu*(v0 - w - m/mu*g)*(1-np.exp(-t*mu/m))
    E.append(-m*np.dot(g, gtx - x0) + m/2*np.dot(gtv,gtv))
    GTX.append(gtx[0])
    GTY.append(gtx[1])


print(v0)
plt.plot(X, Y, 'r-+')
plt.plot(GTX, GTY, 'b')
plt.show()

plt.plot(E)
plt.show()
