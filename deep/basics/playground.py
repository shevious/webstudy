import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.layers import Input, Flatten, Dense, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

def prepare_data(n=10, test=0.5, sigma=0.1):
  n1 = int(n/2);
  n2 = n - n1;
  train = int(n*(1-test))
  x1 = np.random.normal(loc=(0.2,0.2), scale=(sigma, sigma), size=(n1,2))
  y1 = np.random.normal(loc=0.0, scale=0.0, size=n1)
  x2 = np.random.normal(loc=(0.8,0.8), scale=(sigma, sigma), size=(n2,2))
  y2 = np.random.normal(loc=1.0, scale=0.0, size=n2)
  x = np.concatenate((x1, x2))
  y = np.concatenate((y1, y2))
  # shuffle
  p = np.random.permutation(n)
  x = x[p]
  y = y[p]
  return (x[:-train], y[:-train]), (x[train:], y[train:])

(x_train, y_train), (x_test, y_test) = prepare_data(n=200)

'''
plt.scatter(x_train[:,:1], x_train[:,1:],c=y_train)
plt.colorbar();
plt.show()
'''

NUM_CLASSES = 2


#print(x_train)
#print(y_train)
y_train = to_categorical(y_train, NUM_CLASSES)
y_test = to_categorical(y_test, NUM_CLASSES)


#input_layer = Input((32,32,3))
input_layer = Input((2))

x = Flatten()(input_layer)

x = Dense(4, activation = 'relu')(x)
x = Dense(4, activation = 'relu')(x)

output_layer = Dense(NUM_CLASSES, activation = 'softmax')(x)

model = Model(input_layer, output_layer)

model.summary()


opt = Adam(lr=0.0005)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])


model.fit(x_train
          , y_train
          , batch_size=32
          , epochs=200
          , shuffle=True)

print('---- fit done -----')
loss, accuracy = model.evaluate(x_test, y_test)
preds = model.predict(x_test)

plt.scatter(x_test[:,:1], x_test[:,1:],c=preds[:,:1])
plt.colorbar();
plt.show()
