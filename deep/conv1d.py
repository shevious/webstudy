import tensorflow as tf
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D

input_shape = (1, 9, 1)
#x = tf.random.normal(input_shape)
#pred = Conv1D(1, 3, input_shape=input_shape[1:])(x)

x = np.array( [[[0], [0], [0], [1], [1], [1], [0], [0], [0]]], dtype=float)

print(x.shape)

model = Sequential()
model.add(Conv1D(1, 3, input_shape=input_shape[1:]))
model.compile()

print(model.summary())

conv_layer = model.layers[0]
weights = conv_layer.get_weights()

weights[0][0,0,0] = -1.
weights[0][1,0,0] = 0.
weights[0][2,0,0] = 1.

print(weights[0], weights[1])
conv_layer.set_weights(weights)

pred = model.predict(x)
print(pred)
