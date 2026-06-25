import numpy as np
import matplotlib.pyplot as plt

# Beta range: from 0 to pi/2 (in radians)
beta = np.linspace(0, np.pi / 2, 500)
cos_beta = np.cos(beta)

# Different shininess exponents
n_values = [1, 2, 4, 8, 16, 32, 64]

plt.figure(figsize=(8, 5))
for n in n_values:
    y = cos_beta ** n
    plt.plot(beta, y, label=f"e = {n}")

plt.xlabel(r"$\beta$ (radians)")
plt.ylabel(r"$(\cos \beta)^e$")
plt.title(r"Specular Term Shape for Different $e$")
plt.legend()
plt.grid(True)
plt.show()

