import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from tensorflow.keras.layers import Input, Flatten, Dense, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# too slow for two data
#x_train = np.array([[0.2], [0.8]])
#y_train = np.array([[0.3], [0.9]])
x_train = np.array([[0.2], [0.8], [0.9]])
y_train = np.array([[0.3], [0.9], [1.0]])

input_layer = Input((1))
output_layer = Dense(1, activation = None)(input_layer)
model = Model(input_layer, output_layer)

model.summary()
model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['mse'])

model.fit(x_train
          , y_train
          , epochs=2
          , batch_size=1
          )
# check weights
layer = model.layers[1]
weights = layer.get_weights()
print('w = ', weights[0]) # w
print('b = ', weights[1]) # b
preds = model.predict(x_train)
print(preds)

'''

opt = Adam(lr=0.0005)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

conv_layer = model.layers[2]
weights = conv_layer.get_weights()
print('####')
print(weights[0])
print(weights[1])

import tensorflow as tf
#a = np.array(1., dtype=np.float32)
#b = tf.keras.Input(())
from tensorflow.keras import backend as K
inp = model.input                                           # input placeholder
outputs = [layer.output for layer in model.layers]          # all layer outputs
#functors = [K.function([inp, K.learning_phase()], [out]) for out in outputs]    # evaluation functions
functors = [K.function([inp], [out]) for out in outputs]    # evaluation functions

# Testing
#layer_outs = [func([x_test[0:1], 1.]) for func in functors]
layer_outs = [func([x_test[0:1]]) for func in functors]
print('### input=', x_test[0])
print('### results')
for i in range(0, len(layer_outs),1):
  print(layer_outs[i][0])       # i: layer_id, 0: first test data

model.fit(x_train
          , y_train
          , batch_size=32
          , epochs=200
          , shuffle=True)

print('---- fit done -----')
weights = conv_layer.get_weights()
print('####')
print(weights[0])
print(weights[1])
print('### results')
for i in range(0, len(layer_outs),1):
  print(layer_outs[i][0])       # i: layer_id, 0: first test data

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
'''
