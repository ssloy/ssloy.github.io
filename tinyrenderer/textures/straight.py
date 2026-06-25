import numpy as np, matplotlib.pyplot as plt

P0, P1 = np.array([0,0]), np.array([3,1])
t = np.linspace(0,1,100)[:,None]
P = (1-t)*P0 + t*P1

plt.plot(*P.T)
plt.show()
