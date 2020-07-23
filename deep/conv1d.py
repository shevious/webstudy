import tensorflow as tf
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D

import matplotlib.pyplot as plt

data = np.array([ [0, 0, 0, 255, 255, 255, 0, 0, 0] ], dtype=float)
'''
plt.imshow(image)
plt.xticks(np.arange(-0.5, 8.5, step=1), [])
plt.yticks(np.arange(-0.5, 0.5, step=1), [])
plt.grid(True)
plt.show()
'''
image = np.array([ [0, 0, 0, 255, 255, 255, 0, 0, 0] ], dtype=float)
ax = plt.subplot()
ax.imshow(image, cmap=plt.cm.gray)
ax.grid(True)
ax.set_xticks(np.arange(-0.5, 8.5, step=1))
ax.set_xticklabels([])
ax.set_yticks(np.arange(-0.5, 1.5, step=1))
ax.set_yticklabels([])
ax.tick_params(which='both', length=0)
plt.show()

'''
input_shape = (1, 9, 1)
#x = tf.random.normal(input_shape)
#pred = Conv1D(1, 3, input_shape=input_shape[1:])(x)

x = np.array( [
       [ [0], [0], [0], [1], [1], [1], [0], [0], [0] ], # batch 1
    ], dtype=float)

print(x.shape)

model = Sequential()
model.add(Conv1D(1, 3, input_shape=input_shape[1:]))
model.compile()

print(model.summary())

conv_layer = model.layers[0]
weights = conv_layer.get_weights()
print(weights[0], weights[1])

weights[0][0,0,0] = -1.
weights[0][1,0,0] = 0.
weights[0][2,0,0] = 1.

print(weights[0], weights[1])
conv_layer.set_weights(weights)

pred = model.predict(x)
print(pred)
'''
