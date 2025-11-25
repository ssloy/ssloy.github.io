import numpy as np
import matplotlib.pyplot as plt

def charge(a: float, b: float, x: float, y: float) -> float:
#    return 1 / np.hypot(x - a, y - b)
    return -np.log(np.hypot(x - a, y - b))

def potential(x,y):
    return charge( 1,  1, x, y) + \
           charge(-1,  1, x, y) + \
           charge( 1, -1, x, y) + \
           charge(-1, -1, x, y)

x = np.linspace(-2, 2, 300)
y = np.linspace(-2, 2, 300)
X, Y = np.meshgrid(x, y)
Z = np.clip(potential(X, Y), None, 5)
dZ_dy, dZ_dx = np.gradient(Z, y, x)

contour = plt.contourf(X, Y, Z, levels=300)
plt.colorbar(contour, label='potential(x, y)')
plt.contour(X, Y, Z, levels=30, colors='black', linewidths=0.8, linestyles='dashed')
plt.streamplot(X, Y, -dZ_dx, -dZ_dy, color='w', density=1.5, linewidth=.5)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

