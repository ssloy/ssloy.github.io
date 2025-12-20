import numpy as np
import matplotlib.pyplot as plt

from launcher import *

vx, vy = 20,30
t, x, y = BananaLauncher.launch(vx, vy)

plt.scatter(*zip(*BananaLauncher.targets))

plt.scatter(x,y)
plt.show()

g = 0.
for ti, yi in zip(t,y):
    gi = 2*(yi-vy*ti)/ti**2
    g += gi
g /= len(t)

print(g)


print(2*(y[-1]-vy*t[-1])/t[-1]**2)

