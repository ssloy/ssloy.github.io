import numpy as np
import matplotlib.pyplot as plt

img = np.zeros((128, 128))
img[32:96, 32:96] = 1.0

# Sobel kernels
sobel_x = np.array([[-1,0,1],
                    [-2,0,2],
                    [-1,0,1]])
sobel_y = np.array([[-1,-2,-1],
                    [ 0, 0, 0],
                    [ 1, 2, 1]])

# Convolution by hand (no SciPy)
gx = np.zeros_like(img)
gy = np.zeros_like(img)

for i in range(1, img.shape[0]-1):
    for j in range(1, img.shape[1]-1):
        region = img[i-1:i+2, j-1:j+2]
        gx[i,j] = np.sum(region * sobel_x)
        gy[i,j] = np.sum(region * sobel_y)

edges = np.sqrt(gx**2 + gy**2)

plt.figure(figsize=(12,4))
plt.subplot(1,4,1); plt.imshow(img, cmap="gray"); plt.title("Original image")
plt.subplot(1,4,2); plt.imshow(gx, cmap="gray"); plt.title("Vertical edges")
plt.subplot(1,4,3); plt.imshow(gy, cmap="gray"); plt.title("Horizontal edges")
plt.subplot(1,4,4); plt.imshow(edges, cmap="gray"); plt.title("Combined edges")
plt.show()
