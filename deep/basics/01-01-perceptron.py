import tensorflow as tf
from tensorflow.keras import Input, Model, layers, optimizers
import numpy as np

class Perceptron(layers.Layer):
    def __init__(self):
        super().__init__()
        self.w = tf.Variable(initial_value=np.array([[-1., 1.]]), dtype='float32', trainable=True)
        self.b = tf.Variable(initial_value=np.array([[0.]]), dtype='float32', trainable=True)

    def call(self, x):
        return tf.sign(tf.matmul(self.w, tf.transpose(x)) + self.b)

inputs = Input(shape=(2,),dtype='float32')
outputs = Perceptron()(inputs)
model=Model(inputs, outputs)
model.compile(optimizer=optimizers.SGD(lr=0.1), loss='mse')
x_train = np.array(
    [
     [1, -1],
     [-1, 1]
    ]
)
y_train = np.array(
    [[1], [-1]]
)
y_hat = model.predict(x_train)
print(y_hat.shape)
print(y_train.shape)
print(y_hat)

model.fit(x_train[:1], y_train[:1])

