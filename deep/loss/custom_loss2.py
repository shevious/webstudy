import keras

from keras.layers import Input, Dense
from keras.models import Model
import numpy as np

class MyModel():
  def __init__(self):
    return

  def build(self):
    a = Input(shape=(1,))
    b = Dense(2)(a)
    c = Dense(1)(b)
    self.model = Model(a, [b,c])
  
  def customloss(self):
    def loss(y_true, y_pred):
      print('y_pred.shape = ', y_pred.shape)
      print('y_true.shape = ', y_pred.shape)
      return keras.backend.mean(y_true-y_pred)
    return loss

my = MyModel()
my.build()
my.model.compile(loss=my.customloss(), optimizer='adam')

x = np.random.random((2,1))
y = np.random.random((2,1,1))
my.model.train_on_batch(x, y)

