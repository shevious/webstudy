import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-1, 1, 21)
y = np.linspace(-1, 1, 21)
z = np.array([i*i+j*j for j in y for i in x])

X, Y = np.meshgrid(x, y)
Z = z.reshape(21, 21)

plt.contourf(X, Y, Z)
plt.show()
