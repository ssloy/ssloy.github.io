import numpy as np, matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],  # matches LaTeX default
})


# Bézier control points
P0, P1, P2, P3 = np.array([0,0]), np.array([1,1.5]), np.array([2,2]), np.array([3,1])

# Bézier curve
t = np.linspace(0,1,100)[:,None]
P = (1-t)**3*P0 + 3*(1-t)**2*t*P1 + 3*(1-t)*t**2*P2 + t**3*P3

# plot it
plt.scatter(*zip(P0,P1,P2,P3),c='k',s=100)
plt.plot(*zip(P0,P1,P2,P3),'k--')
plt.plot(*P.T,'r',lw=3)
plt.xlim(-1,4)
plt.ylim(-.25,2.25)
plt.gca().set_aspect('equal', adjustable='box')

plt.text(P0[0] - 0.25, P0[1] + 0.15, r"$P_0$", fontsize=24)
plt.text(P1[0] - 0.47, P1[1] + 0.07, r"$P_1$", fontsize=24)
plt.text(P2[0] + 0.13, P2[1] - 0.05, r"$P_2$", fontsize=24)
plt.text(P3[0] + 0.07, P3[1] + 0.07, r"$P_3$", fontsize=24)
plt.show()
