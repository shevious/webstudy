import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

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

NUM_CLASSES = 2

(x_train, y_train), (x_test, y_test) = prepare_data(n=200)

plt.scatter(x_train[:,:1], x_train[:,1:],c=y_train, cmap=cm.coolwarm)
plt.colorbar();
plt.show()

y_train = to_categorical(y_train, NUM_CLASSES)
y_test = to_categorical(y_test, NUM_CLASSES)

input_layer = Input((2))

x = Flatten()(input_layer)

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
diff = np.subtract(preds[:,1:], preds[:,:1])
#print(x_test.shape)
#print(x_test)

#plt.scatter(x_test[:,:1], x_test[:,1:],c=preds[:,:1])
plt.scatter(x_test[:,:1], x_test[:,1:],c=diff, cmap=cm.coolwarm)
plt.colorbar();
plt.show()

# Make data.
X = np.arange(0, 1, 0.1)
Y = np.arange(0, 1, 0.1)

X, Y = np.meshgrid(X, Y)
xy = np.vstack((X.flatten(), Y.flatten())).T
preds = model.predict(xy)
diff = np.subtract(preds[:,1:], preds[:,:1])

Z = diff.reshape((len(X), len(Y)))

fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.00, 1.00)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
