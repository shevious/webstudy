import keras

from keras.layers import Input, Dense
from keras.models import Model
import numpy as np

class MyModel():
  def __init__(self):
    return

  def build(self):
    a = Input(shape=(1,))
    self.b = Dense(1)(a)
    self.model = Model(a, self.b)
  
  def customloss(self):
    a = self.b*1.1
    def loss(y_true, y_pred):
      return a + keras.backend.mean(y_true-y_pred)
    return loss

my = MyModel()
my.build()
my.model.compile(loss=my.customloss(), optimizer='adam')

x = np.random.random((1,1))
y = np.random.random((1,1))
my.model.train_on_batch(x, y)


