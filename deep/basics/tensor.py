import numpy as np
import time

n = 20000

w = np.random.random((n,n))
x = np.random.random((n))
#w = np.array([[0, 1],[2, 3]])
#x = np.array([1, 2])
#print(w)
#print(x)
tic = time.time()
y1 = np.dot(w,x)
y2 = np.dot(w,x)
y3 = np.dot(w,x)
y4 = np.dot(w,x)
y5 = np.dot(w,x)
y6 = np.dot(w,x)
y7 = np.dot(w,x)
y8 = np.dot(w,x)
y9 = np.dot(w,x)
y = y1+y2+y3+y4+y5+y6+y9
toc = time.time()
print('elapsed time =', toc-tic)
print(y[0], y[1], y[n-1])

'''
w = w.tolist()
x = x.tolist()
print("convert done")
tic = time.time()
y = []
for row in range(0, n, 1):
  y.append(0)
  for col in range(0, n, 1):
    y[row] += w[row][col]*x[col]
toc = time.time()
print('elapsed time=', toc-tic)
#print(y)
'''

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Flatten, Dense, Conv2D
from tensorflow.keras.models import Model

input_layer = [Input((n,n)), Input(n)]
y1 = keras.layers.Dot(axes=(2,1))(input_layer)
y2 = keras.layers.Dot(axes=(2,1))(input_layer)
y3 = keras.layers.Dot(axes=(2,1))(input_layer)
y4 = keras.layers.Dot(axes=(2,1))(input_layer)
y5 = keras.layers.Dot(axes=(2,1))(input_layer)
y6 = keras.layers.Dot(axes=(2,1))(input_layer)
y7 = keras.layers.Dot(axes=(2,1))(input_layer)
y8 = keras.layers.Dot(axes=(2,1))(input_layer)
y9 = keras.layers.Dot(axes=(2,1))(input_layer)
output_layer = keras.layers.Add()([y1,y2,y3,y4,y5,y6,y7,y8,y9])
model = Model(input_layer, output_layer)

#print(model.summary())
model.compile()

tic = time.time()
y = model.predict([w.reshape(1,n,n), x.reshape(1,n)])
toc = time.time()
print('elapsed time =', toc-tic)
print(y[0][0], y[0][1], y[0][n-1])


