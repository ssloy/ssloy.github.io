import numpy as np
import matplotlib.pyplot as plt

import numpy as np

g     = -9.81 # gravity, m/s^2
x_star, y_star = 34, 23


plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=28)
'''
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.plot(xs, ys, marker='.')
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.gca().set_aspect('equal', 'box')
plt.savefig("plot-euler.png")
plt.show()
'''

plt.title('Hit a target with least effort:\n constrained minimization')

VX, VY = np.meshgrid(np.linspace(.01, 50, 1000),
                     np.linspace(.01, 50, 1000))

contour = plt.contourf(VX, VY, np.hypot(VX, VY), levels=200, cmap='viridis')
plt.colorbar(contour, label='$\\sqrt{v_{x,0}^2 + v_{y,0}^2}$')
plt.contour(VX, VY, np.hypot(VX, VY), levels=30, colors='silver', linewidths=0.8, linestyles='dashed')

VX = np.linspace(0.01, 50, 1000)
VY = [ vx*y_star/x_star - g/2*(x_star/vx) for vx in VX ]

plt.plot(VX, VY, linewidth=3, color='black')

plt.xlabel('$v_{x,0}$')
plt.ylabel('$v_{y,0}$')

plt.xlim(0, 50)
plt.ylim(0, 50)


plt.gca().set_aspect('equal')
plt.tight_layout()


plt.savefig("plot1.png")
plt.show()

