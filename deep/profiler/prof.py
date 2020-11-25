import tensorflow as tf
from tensorflow.keras.layers import Input, Concatenate, Dot, Add, ReLU, Activation
from tensorflow.keras.layers import Dense
from tensorflow import keras
import numpy as np
import time

dim = 57
# Train the model here
inputs = Input(shape=(dim*2,), name='input_x')
a = Dense(dim, activation='relu')(inputs)
a = Dense(dim, activation='relu')(a)
G_prob = Dense(dim, activation='sigmoid')(a)
generator = keras.models.Model(inputs, G_prob, name='generator')
generator.compile(optimizer='adam', loss='binary_crossentropy')

n = 128
x = np.random.random_sample((n, dim*2))
y = np.random.random_sample((n, dim))

#warming up
for i in range(100):
  generator.fit(x, y)

tf.profiler.experimental.start('logdir')
tick = time.time()
#generator.fit(x, y)
for i in range(100):
  y = generator.predict(x)
tock = time.time()
print('#######')
print((tock-tick)*1000, "ms")

tf.profiler.experimental.stop()
