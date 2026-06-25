import numpy as np
import matplotlib.pyplot as plt

def charge(a: float, b: float, x: float, y: float) -> float:
    return -np.log(np.hypot(x - a, y - b))

def potential(x,y):
    return charge(0,  1, x, y) + \
           charge(0, -1, x, y)

def energy(x,y):
    return potential(x+2,y)+potential(x-2,y)


x = np.linspace(-2, 2, 300)
y = np.linspace(-2, 2, 300)
X, Y = np.meshgrid(x, y)
Z = np.clip(energy(X, Y), None, 5)
dZ_dy, dZ_dx = np.gradient(Z, y, x)


plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True
plt.rc('font', size=24)

plt.figure(figsize=(10, 8))

contour = plt.contourf(X, Y, Z, levels=300, cmap='hot')
plt.colorbar(contour, label='$P(x, y)$')
plt.contour(X, Y, Z, levels=30, colors='silver', linewidths=0.8, linestyles='dashed')
#plt.streamplot(X, Y, -dZ_dx, -dZ_dy, color='yellow', density=1.5, linewidth=.5)
plt.xlabel('$x$')
plt.ylabel('$y$')

plt.gca().set_aspect('equal')
plt.tight_layout()
plt.savefig("2d-potential-energy.png")
plt.show()

