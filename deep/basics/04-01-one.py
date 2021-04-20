import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from tensorflow.keras.layers import Input, Flatten, Dense, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

w = 0.8
b = 0.2
x = np.linspace(0, 1, num=50)

y = w*x + b

fig, ax = plt.subplots()
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)
ax.set_aspect('equal')
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([0,1,0,1])
plt.show()

w = 1
b = 0
x = np.linspace(-1, 1, num=50)
y = w*x + b
fig, ax = plt.subplots()
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)
ax.set_aspect('equal')
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([-1,1,-1,1])
plt.show()

x = np.linspace(-5, 5, num=50)
y = 1/(1+np.exp(-x))
fig, ax = plt.subplots()
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([-1,1,-0.25,1])
plt.show()

x = np.linspace(-5, 5, num=50)
y = np.linspace(-5, 5, num=50)
y[x<0] = 0
fig, ax = plt.subplots()
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([-5,5,-0.4,5])
plt.show()

x = np.linspace(-5, 5, num=50)
y = x*np.tanh(np.log(1+np.exp(x)))
fig, ax = plt.subplots()
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([-5,5,-0.4,5])
plt.show()

w = 1
b = 0
x = np.linspace(-1, 1, num=51)
y = np.zeros(51)
y[x > 0] = 1

fig, ax = plt.subplots()
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)

w = 1
b = 0
x = np.linspace(-1, 1, num=51)
y = np.zeros(51)
y[x > 0] = 1

fig, ax = plt.subplots()
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)
x = np.zeros(21)
y = np.linspace(0, 1, num=len(x))
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)
ax.set_aspect('equal')
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([-1,1,-0.25,1])
plt.show()

w = np.array([0.8, 0.7])
b = np.array(0)
x1,x2 = np.mgrid[0:1.1:0.1, 0:1.1:0.1]
x = np.vstack((x1.flatten(), x2.flatten())).T
z = np.tensordot(w, x, axes=(0,1))
z = z.reshape(len(x1), len(x2))
fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(x1, x2, z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
plt.show()
