import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from tensorflow.keras.layers import Input, Flatten, Dense, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

def prepare_data(n=10, test=0.5, sigma=0.13):
  n1 = int(n/3);
  n2 = int(n/3);
  n3 = n - n1-n2;
  # group1 data
  x1 = np.random.normal(loc=(0.2,0.2), scale=(sigma, sigma), size=(n1,2))
  #y1 = np.random.normal(loc=-1.0, scale=0.0, size=n1)
  y1 = np.random.normal(loc=0.0, scale=0.0, size=n1)
  # group2 data
  x2 = np.random.normal(loc=(0.4,0.8), scale=(sigma, sigma), size=(n2,2))
  y2 = np.random.normal(loc=1.0, scale=0.0, size=n2)
  x3 = np.random.normal(loc=(0.7,0.3), scale=(sigma, sigma), size=(n3,2))
  y3 = np.random.normal(loc=2.0, scale=0.0, size=n3)
  # assemble all data
  x = np.concatenate((x1, x2, x3))
  y = np.concatenate((y1, y2, y3))
  # shuffle
  p = np.random.permutation(n)
  x = x[p]
  y = y[p]
  train = int(n*(1-test))
  return (x[:-train], y[:-train]), (x[train:], y[train:])

NUM_CLASSES = 3

(x_train, y_train), (x_test, y_test) = prepare_data(n=400)

y_train = to_categorical(y_train, NUM_CLASSES)
y_test = to_categorical(y_test, NUM_CLASSES)

#print(y_train[0:10])

#plt.scatter(x_train[:,:1], x_train[:,1:],c=y_train, cmap=cm.coolwarm)
plt.scatter(x_train[:,:1], x_train[:,1:],c=y_train)
#plt.colorbar();
plt.show()

input_layer = Input((2))

x = Flatten()(input_layer)
x = Dense(6, activation = 'relu')(x)
x = Dense(4, activation = 'relu')(x)
x = Dense(4, activation = 'relu')(x)
#output_layer = Dense(NUM_CLASSES, activation = None)(x)
output_layer = Dense(NUM_CLASSES, activation = 'softmax')(x)

model = Model(input_layer, output_layer)

model.summary()

#model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.0005), metrics=['accuracy'])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#model.compile(loss='mse', optimizer='adam', metrics=['mse'])

model.fit(x_train
          , y_train
          #, batch_size=200
          , epochs=4000
          , shuffle=True)


#print(preds)

##print(preds)
n = 400
x = np.linspace(-0.3, 1.2, n)
y = np.linspace(-0.4, 1.4, n)
X, Y = np.meshgrid(x, y)
xy = np.vstack((X.flatten(), Y.flatten())).T
preds = model.predict(xy)
# extract top 1 results
#preds = to_categorical(np.argmax(preds, axis=1), NUM_CLASSES)
preds = np.argmax(preds, axis=1)
preds = preds.reshape(n,n)
#z = np.array([i*i+j*j for j in y for i in x])

#Z = z.reshape(21, 21)

#plt.scatter(xy[:,:1], xy[:,1:],c=preds)
plt.contourf(X, Y, preds)
plt.scatter(x_train[:,:1], x_train[:,1:],c=y_train)
plt.show()

plt.contourf(X, Y, preds)
plt.scatter(x_test[:,:1], x_test[:,1:],c=y_test)
plt.show()
