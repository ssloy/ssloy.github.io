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

while t<T:
    traj_x.append(x)
    traj_y.append(y)

    x += vx * dt
    y += vy * dt
    vy += g * dt

    traj2_x.append(x0x + v0x*t)
    traj2_y.append(x0y + v0y*t + g*t**2/2)

    t += dt

plt.plot(traj_x, traj_y, 'r-+')
plt.plot(traj2_x, traj2_y, 'b-')
plt.show()
