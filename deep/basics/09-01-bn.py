import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-4, 4, 21)
y = np.linspace(-3, 3, 21)
z = np.array([np.log(0.1*i**2+0.1*j**2+0.2) for j in y for i in x])

X, Y = np.meshgrid(x, y)
Z = z.reshape(21, 21)

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.contourf(X, Y, Z)
plt.show()
