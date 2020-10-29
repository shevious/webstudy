import numpy as np
import matplotlib.pyplot as plt
import matplotlib


x = np.linspace(-1, 1, 21)
y = np.linspace(-1, 1, 21)
z = np.array([i*i+j*j for j in y for i in x])

X, Y = np.meshgrid(x, y)
Z = z.reshape(21, 21)

#plt.contourf(X, Y, Z)
#plt.show()

import tensorflow as tf

#opt = tf.keras.optimizers.SGD(learning_rate=0.45)
#opt = tf.keras.optimizers.SGD(learning_rate=0.45, momentum=0.55)
#opt = tf.keras.optimizers.SGD(learning_rate=0.2, momentum=0.55)
#opt = tf.keras.optimizers.SGD(learning_rate=0.2)
opt = tf.keras.optimizers.RMSprop(learning_rate=0.1)
opt = tf.keras.optimizers.RMSprop(learning_rate=0.2)
#opt = tf.keras.optimizers.Adam(learning_rate=0.45)
#opt = tf.keras.optimizers.Adam(learning_rate=0.2)

w1 = tf.Variable(0.45)
w2 = tf.Variable(0.45)
loss = lambda: (4*0.1*w1**2 + 4*w2**2)/2.0       # d(loss)/d(dw) == [w1, w2]

x_stt = -0.5
x_end = 0.5
y_stt = -0.5
y_end = 0.5

x = np.linspace(x_stt, x_end, 21)
y = np.linspace(y_stt, y_end, 21)
z = np.array([(4*0.1*i*i+4*j*j)/2.0 for j in y for i in x])

X, Y = np.meshgrid(x, y)
Z = z.reshape(21, 21)

w1_adam = []
w2_adam = []

for epoch in range(0,100):
  w1_adam.append(w1.numpy())
  w2_adam.append(w2.numpy())
  step_count = opt.minimize(loss, [w1, w2]).numpy()
  # The first step is `-learning_rate*sign(grad)`  
  #print(w1.numpy(), w2.numpy())

fig, ax = plt.subplots()
ax.set_aspect('equal')
#ax.grid(True, which='both')
ax.contourf(X,Y,Z)
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([x_stt,x_end,y_stt,y_end])
#plt.show()
ax2, = ax.plot([], [], color='orange')
ax3, = ax.plot([], [], 'o', color='orange')

def animate(i):
  #ret = ax.scatter(xs, ys, c=ys, cmap=cm.coolwarm)
  #ax.scatter([], [], c=[], cmap=cm.coolwarm)

  #x = np.linspace(0,1,51)
  #global w, b
  #y = w*x + b

  ax2.set_data(w1_adam[0:i], w2_adam[0:i])
  ax3.set_data(w1_adam[i], w2_adam[i])
  return (ax2,)

i = np.arange(len(w1_adam))
ani = matplotlib.animation.FuncAnimation(fig, animate,
                                         frames=i, interval=100)
plt.show()

