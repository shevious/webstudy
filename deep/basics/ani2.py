import numpy as np
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow import keras
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import cm
from tensorflow.keras.optimizers import Adam, SGD

x_train = np.array([[0.2], [0.8], [0.3], [0.7], [0.4], [0.5]])
y_train = np.array([[0.3], [0.9], [0.6], [0.9], [0.4], [0.6]])

input_layer = Input((1))
output_layer = Dense(1, activation = None)(input_layer)
model = Model(input_layer, output_layer)

class wbHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs=None):
        self.wb = []
    def on_batch_end(self, batch, logs=None):
        layer = self.model.layers[1]
        weights = layer.get_weights()
        self.wb.append(weights)
        
#model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
model.compile(loss='mean_squared_error', optimizer=SGD(lr=0.05), metrics=['mse'])
history = wbHistory()
model.fit(x_train, y_train, epochs=200, callbacks=[history])

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
#fig.colorbar(ret, ax=ax);
ax.axis([0,1,-1,1])
#plt.show()
ax2, = ax.plot([], [])

def animate(i):
  ret = ax.scatter(x_train, y_train, c=y_train, cmap=cm.coolwarm)
  #ax.scatter([], [], c=[], cmap=cm.coolwarm)

  x = np.linspace(0,1,51)
  #global w, b
  w = history.wb[i][0][0][0]
  b = history.wb[i][1][0]
  y = w*x + b

  ax2.set_data(x, y)
  print('i:',i,w,b)
  return (ax2,)

ani = matplotlib.animation.FuncAnimation(fig, animate,
                                         frames=len(history.wb), interval=400)
plt.show()
