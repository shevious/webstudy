import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from tensorflow.keras.layers import Input, Flatten, Dense, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

w = -0.1
b = 0.5
x = np.array(([0.2,0.8]))
y = np.array(([0.3,0.9]))

#y = w*x + b

fig, ax = plt.subplots()
ret = ax.scatter(x, y, c=y, cmap=cm.coolwarm)

x = np.linspace(0,1,51)
y = w*x + b
ax.plot(x, y)

ax.set_aspect('equal')
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([0,1,0,1])
plt.show()

x = np.linspace(-0.5, 3, 20)
y = 0.68*(x**2) - 2.56*x + 2.6
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_aspect('equal')
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
plt.show()
