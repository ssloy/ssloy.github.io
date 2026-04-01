import numpy as np
import matplotlib.pyplot as plt

width, height = 640, 480
image = np.zeros((height, width, 3))

for i in range(height):
    for j in range(width):
        image[i,j] = np.array([j/width, i/height, 0])

plt.imsave('result.png', image)

