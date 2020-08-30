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
