import numpy as np, matplotlib.pyplot as plt

# Hermite control points and normals
P0, P1, N0, N1 = np.array([0,0]), np.array([3,1]), np.array([-4.5,3]), np.array([3,3])

# Hermite curve
t = np.linspace(0,1,100)[:,None]
P = (2*t**3-3*t**2+1)*P0 + (-2*t**3+3*t**2)*P1 + (t**3-2*t**2+t)*(np.array([[0,1],[-1,0]])@N0) + (t**3-t**2)*(np.array([[0,1],[-1,0]])@N1)

# plot it
plt.plot(*P.T)
plt.show()
