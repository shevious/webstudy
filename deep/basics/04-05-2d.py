import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from tensorflow.keras.layers import Input, Flatten, Dense, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

'''
# relu plotting
w = np.array([0.8,0.7])
b = 0
x1 = np.linspace(-1, 1, num=50)
x2 = np.linspace(-1, 1, num=50)

x1, x2 = np.meshgrid(x1, x2)
x = np.vstack((x1.flatten(), x2.flatten())).T
#print(x)

y = np.tensordot(w, x, axes=(0, 1))
y[y<0] = 0
y = y.reshape(len(x1), len(x2))
#print(y)

fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(x1, x2, y, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
plt.show()
'''
w = np.array([1.2,1.0])
b = 0
x1 = np.linspace(-5, 5, num=50)
x2 = np.linspace(-5, 5, num=50)

x1, x2 = np.meshgrid(x1, x2)
x = np.vstack((x1.flatten(), x2.flatten())).T
#print(x)

y = np.tensordot(w, x, axes=(0, 1))
#y[y<0] = 0
#y = 1/(1+np.exp(-y))
y = y.reshape(len(x1), len(x2))
#print(y)

fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(x1, x2, y, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
plt.show()

#y = w*x + b

'''
fig, ax = plt.subplots()
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)
ax.set_aspect('equal')
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([0,1,0,1])
plt.show()
'''
