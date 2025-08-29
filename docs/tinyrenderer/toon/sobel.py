import numpy as np
import matplotlib.pyplot as plt

# -------------------
# 1D Sobel demo
# -------------------
# A signal with a step edge
x = np.linspace(0, 20, 100)
signal = np.sin(x/2) + (x > 10)  # sinusoid + step

# 1D Sobel kernel
sobel_1d = np.array([-1, 0, 1])

# Manual convolution
edges_1d = np.zeros_like(signal)
for i in range(1, len(signal)-1):
    window = signal[i-1:i+2]       # take [left, center, right]
    edges_1d[i] = np.sum(window * sobel_1d)

plt.figure(figsize=(10,3))
plt.plot(x, signal, label="Signal")
plt.plot(x, edges_1d, label="Edge response")
plt.title("1D Sobel Edge Detection")
plt.legend()
plt.show()

img = np.zeros((100, 100))
img[30:70, 30:70] = 1.0

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
plt.subplot(1,4,1); plt.imshow(img, cmap="gray"); plt.title("Original")
plt.subplot(1,4,2); plt.imshow(gx, cmap="gray"); plt.title("Sobel X (vertical edges)")
plt.subplot(1,4,3); plt.imshow(gy, cmap="gray"); plt.title("Sobel Y (horizontal edges)")
plt.subplot(1,4,4); plt.imshow(edges, cmap="gray"); plt.title("Combined edges")
plt.show()
