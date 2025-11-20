import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 16, 100)
signal = np.sin(x/2) + (x > 10) # sinusoid + step

sobel = np.array([-1, 0, 1]) # 1D Sobel kernel
edges = np.zeros_like(signal)
for i in range(1, len(signal)-1):
    window = signal[i-1:i+2]    # take [left, center, right]
    edges[i] = np.sum(window * sobel)

plt.figure(figsize=(10,3))
plt.step(x, signal, label="Pixel intensities")
plt.step(x, edges, label="Edge response")
plt.title("1D Sobel edge detection")
plt.legend()
plt.show()

