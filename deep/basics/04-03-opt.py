import tensorflow as tf
from tensorflow import keras
import numpy as np


# Create an optimizer with the desired parameters.
opt = keras.optimizers.SGD(learning_rate=0.1)
# `loss` is a callable that takes no argument and returns the value
# to minimize.
loss = lambda: 3 * var1 * var1 + 2 * var2 * var2
# In graph mode, returns op that minimizes the loss by updating the listed
# variables.
#opt_op = opt.minimize(loss, var_list=[var1, var2])
#opt_op.run()
# In eager mode, simply call minimize to update the list of variables.
var1 = np.array([0.7])
var2 = np.array([0.7])
var1 = tf.convert_to_tensor(var1)
var2 = tf.convert_to_tensor(var2)
var_list = [var1, var2]

var1 = tf.Variable(0.7, name='var1', trainable=True, dtype=tf.float32)
var2 = tf.Variable(0.7, name='var1', trainable=True, dtype=tf.float32)
opt.minimize(loss, var_list=[var1, var2])
print(var1.numpy(), var2.numpy())
opt.minimize(loss, var_list=[var1, var2])
print(var1.numpy(), var2.numpy())

