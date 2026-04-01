import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],  # matches LaTeX default
})



# Hermite control points and normals
P0, P1, N0, N1 = np.array([0,0]), np.array([3,1]), np.array([-4.5,3]), np.array([3,3])

# Hermite curve
t = np.linspace(0,1,100)[:,None]
P = (2*t**3-3*t**2+1)*P0 + (-2*t**3+3*t**2)*P1 + (t**3-2*t**2+t)*(np.array([[0,1],[-1,0]])@N0) + (t**3-t**2)*(np.array([[0,1],[-1,0]])@N1)

# plot it
plt.scatter(*zip(P0,P1),c='k',s=100)
plt.quiver(*P0,*N0,color='k',angles='xy',scale_units='xy',scale=5)
plt.quiver(*P1,*N1,color='k',angles='xy',scale_units='xy',scale=5)
plt.plot(*P.T,'r',lw=3)
plt.xlim(-1,4)
plt.ylim(-.25,2.25)
plt.gca().set_aspect('equal', adjustable='box')
plt.text(P0[0] + 0.13, P0[1] - 0.08, r"$P_0$", fontsize=24)
plt.text(P0[0] - 0.65, P0[1] + 0.55, r"$\vec{n_0}$", fontsize=24)
plt.text(P1[0] - 0.47, P1[1] - 0.10, r"$P_1$", fontsize=24)
plt.text(P1[0] - 0.03, P1[1] + 0.47, r"$\vec{n_1}$", fontsize=24)
plt.show()
