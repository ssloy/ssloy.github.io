import numpy as np
import matplotlib.pyplot as plt

m  = 0.5  # banana mass, kg
g = -9.81 # gravity, m/s^2

speed = 30.0  # launch speed (m/s)
angle = 40.0  # launch angle (degrees)
v0x, v0y = speed * np.cos(angle * np.pi/180.0), \
           speed * np.sin(angle * np.pi/180.0)
x0x, x0y = 0, 0

dt = 0.1
t  = 0
T  = 5

traj_x = []
traj_y = []

x,  y  = x0x, x0y
vx, vy = v0x, v0y

traj2_x = []
traj2_y = []

x2,  y2  = x0x, x0y
vx2, vy2 = v0x, v0y

traj3_x = []
traj3_y = []

E = []
E2 = []

while t<T:
    traj_x.append(x)
    traj_y.append(y)

    E.append(-m*g*y + m*(vx*vx + vy*vy)/2)

    x += vx * dt
    y += vy * dt
    vy += g * dt

    traj3_x.append(x2)
    traj3_y.append(y2)

    E2.append(-m*g*y2 + m*(vx2*vx2 + vy2*vy2)/2)

    x2 += dt * vx2
    y2 += dt * (vy2 + dt/2 * g)
    vy2 += dt * g


    traj2_x.append(x0x + v0x*t)
    traj2_y.append(x0y + v0y*t + g*t**2/2)

    t += dt

plt.plot(E, 'r')
plt.plot(E2, 'g')
plt.plot(traj_x, traj_y, 'r-+')
plt.plot(traj3_x, traj3_y, 'g-+')
plt.plot(traj2_x, traj2_y, 'b-')
plt.show()
