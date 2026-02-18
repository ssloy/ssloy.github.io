import numpy as np
import matplotlib.pyplot as plt

# Gravity
g = 9.81

# Define the vector field
def f(y, vy):
    return vy, -g*np.ones_like(y)

# Create a grid for phase space
y_vals = np.linspace(-10, 10, 20)
vy_vals = np.linspace(-10, 10, 20)
Y, VY = np.meshgrid(y_vals, vy_vals)
DY, DVY = f(Y, VY)


plt.figure(figsize=(7, 5))
plt.quiver(Y, VY, DY, DVY, angles='xy', width=0.003, headwidth=3, headlength=6, color='silver')
plt.xlabel('y (position)')
plt.ylabel('v_y (velocity)')
plt.title('Phase space vector field of 1D projectile')

# Sample trajectories
def simulate(y0, vy0, dt=0.0497, n_steps=41):
    ys = [y0]
    vys = [vy0]
    y, vy = y0, vy0
    for _ in range(n_steps):
        # RK2 (mid-point)
        k1y, k1vy = f(y, vy)
        y_mid = y + dt/2 * k1y
        vy_mid = vy + dt/2 * k1vy
        k2y, k2vy = f(y_mid, vy_mid)
        y += dt * k2y
        vy += dt * k2vy
        ys.append(y)
        vys.append(vy)
    return ys, vys

# Plot a few trajectories
for vy0 in [10]:
    ys, vys = simulate(y0=0, vy0=vy0)
    plt.plot(ys, vys, label=f'v0={vy0}')

plt.legend()
plt.gca().set_aspect('equal', 'box')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.show()
