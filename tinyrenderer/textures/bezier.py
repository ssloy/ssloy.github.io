import numpy as np, matplotlib.pyplot as plt

# Bézier control points
P0, P1, P2, P3 = np.array([0,0]), np.array([1,1.5]), np.array([2,2]), np.array([3,1])

# Bézier curve
t = np.linspace(0,1,100)[:,None]
P = (1-t)**3*P0 + 3*(1-t)**2*t*P1 + 3*(1-t)*t**2*P2 + t**3*P3

# plot it
plt.plot(*P.T)
plt.show()
