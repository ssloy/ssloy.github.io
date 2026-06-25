import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G = 1000 # gravity strength
dt = 1e-5

# Planet
planet_pos = np.array([0.0, 0.0])
planet_vel = np.array([1.0, 0.0])   # moving to the right

# Spacecraft
ship_pos = np.array([-10.0, -2.0])
#ship_vel = np.array([.0, 7.0])

ship_speed = 7.0
angle = 90    # launch angle in degrees

ship_vel= np.array([ship_speed * np.cos(angle * np.pi/180),
                    ship_speed * np.sin(angle * np.pi/180)])

planet_path = []
ship_path = []

fig, ax = plt.subplots()
ax.set_xlim(-15, 25)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')

planet_dot, = ax.plot([], [], 'bo', markersize=10)
ship_dot, = ax.plot([], [], 'ro', markersize=5)
planet_line, = ax.plot([], [], 'b--', alpha=0.5)
ship_line, = ax.plot([], [], 'r-')

STEPS_PER_FRAME = 1000

def update(frame):
    global planet_pos, ship_pos, ship_vel

    for _ in range(STEPS_PER_FRAME):
        planet_pos += planet_vel * dt # move the planet

        # Gravity on spacecraft
        r = planet_pos - ship_pos
        dist = np.linalg.norm(r)
        accel = G * r / dist**3

        ship_vel += accel * dt
        ship_pos += ship_vel * dt # move the ship

    planet_path.append(planet_pos.copy())
    ship_path.append(ship_pos.copy())

    pp = np.array(planet_path)
    sp = np.array(ship_path)

    planet_dot.set_data([planet_pos[0]], [planet_pos[1]])
    ship_dot.set_data([ship_pos[0]], [ship_pos[1]])

    planet_line.set_data(pp[:, 0], pp[:, 1])
    ship_line.set_data(sp[:, 0], sp[:, 1])

    return planet_dot, ship_dot, planet_line, ship_line

ani = FuncAnimation(fig, update, frames=3000, interval=1, blit=True)
plt.show()

