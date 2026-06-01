import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],  # matches LaTeX default
})

P0, P1 = np.array([0,0]), np.array([3,1])

t = np.linspace(0,1,100)[:,None]
P = (1-t)*P0 + t*P1

# plot it
plt.scatter(*zip(P0,P1),c='k',s=100)
plt.plot(*P.T,'r',lw=3)
plt.xlim(-1,4)
plt.ylim(-.25,2.25)
plt.gca().set_aspect('equal', adjustable='box')

plt.text(P0[0] - 0.25, P0[1] + 0.15, r"$P_0$", fontsize=24)
plt.text(P1[0] + 0.07, P1[1] + 0.07, r"$P_1$", fontsize=24)
plt.show()
