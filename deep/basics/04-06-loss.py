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
#b = 0.27
#w = -0.01348
#w = 0.1696
#b = 0.04
x = np.array(([0.2,0.8]))
y = np.array(([0.3,0.9]))
xs = x
ys = y

#y = w*x + b
lr = 0.1

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([0,1,0,1])
#plt.show()
ax2, = ax.plot([], [])

def animate(i):
  ret = ax.scatter(xs, ys, c=ys, cmap=cm.coolwarm)
  ax.scatter([], [], c=[], cmap=cm.coolwarm)

  x = np.linspace(0,1,51)
  global w, b
  y = w*x + b

  ax2.set_data(x, y)
  w2 = w - lr*(2*(0.2*w+b-0.3)*0.2 + 2*(0.8*w+b-0.9)*0.8)
  b2 = b - lr*(2*(0.2*w+b-0.3) + 2*(0.8*w+b-0.9))
  print((2*(0.2*w+b-0.3)*0.2 + 2*(0.8*w+b-0.9)*0.8),(2*(0.2*w+b-0.3) + 2*(0.8*w+b-0.9)))
  w = w2
  b = b2
  print('i:',i,w,b)
  return (ax2,)

i = np.arange(50)
import matplotlib
ani = matplotlib.animation.FuncAnimation(fig, animate, 
                                         frames=i, interval=400)
ani.save("loss.gif", writer="imagemagick")
plt.show()

x = np.linspace(-0.5, 4, 30)
y = 0.68*(x**2) - 2.56*x + 2.6
fig, ax = plt.subplots()
ax.plot(x, y)
x0 = -0.1
a = 2*0.68*x0-2.56
x = np.linspace(-0.5, 1, 10)
y = a*(x - x0) + 0.68*(x0**2)-2.56*x0+2.6
ax.plot(x, y, color='orange')
ax.scatter(x0, 0.68*(x0**2)-2.56*x0+2.6, color='red')
x = np.linspace(2, 4, 10)
x0 = 3
a = 2*0.68*x0-2.56
y = a*(x - x0) + 0.68*(x0**2)-2.56*x0+2.6
ax.scatter(x0, 0.68*(x0**2)-2.56*x0+2.6, color='red')
ax.plot(x, y, color='green')
x0 = 2.56/0.68/2
ax.scatter(x0, 0.68*(x0**2)-2.56*x0+2.6, color='red')
ax.set_aspect('equal')
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
plt.show()
