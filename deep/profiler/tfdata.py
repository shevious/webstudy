import tensorflow as tf
from tensorflow.keras.layers import Input, Concatenate, Dot, Add, ReLU, Activation
from tensorflow.keras.layers import Dense
from tensorflow import keras
import time

import numpy as np
from tensorflow import keras

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, dim=(57), batch_size=32):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.x = np.random.random_sample((self.batch_size, dim*2)).astype('float32')
        self.y = np.random.random_sample((self.batch_size, dim)).astype('float32')

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(128/self.batch_size)

    def __getitem__(self, index):
        'Generate one batch of data'
        #print('index =', index)
        #x = np.random.random_sample((self.batch_size, dim*2)).astype('float32')
        #y = np.random.random_sample((self.batch_size, dim)).astype('float32')
        #return x, y
        return self.x, self.y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        return

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
batch_size = 128
dim = 57

train_generator = DataGenerator(dim, batch_size)

(x, y) = train_generator.__getitem__(0)
print(len(x))
print(len(y))
print(x[0].shape)
print(x[1].shape)
#print(x.dtype, x.shape)
#print(y.dtype, y.shape)

ds = tf.data.Dataset.from_generator(
    lambda: train_generator.__iter__(),
    output_types=(tf.float32, tf.float32), 
    output_shapes=([batch_size,114], [batch_size,57])
)
print(ds.element_spec)

print('####')

for x, y in ds.take(1):
  print('x.shape: ', x.shape)
  print('y.shape: ', y.shape)
print('####')

#warming up
#for i in range(100):
  #generator.fit(x, y)
generator.fit(
    ds,
    epochs=10,
)
'''
for i in range(3):
    generator.fit(train_generator, 
        use_multiprocessing=True,
        workers=6)
'''

tf.profiler.experimental.start('logdir')
tick = time.time()
#generator.fit(x, y)
'''
generator.fit(train_generator, 
    epochs=10,
    use_multiprocessing=True,
    workers=6)
'''
generator.fit(
    ds,
    epochs=100,
)
#for i in range(100):
  #y = generator.predict(x)
tock = time.time()
print('#######')
print((tock-tick)*1000, "ms")

tf.profiler.experimental.stop()
