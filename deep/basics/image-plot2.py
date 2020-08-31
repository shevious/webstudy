#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tensorflow와 tf.keras를 임포트합니다
import tensorflow as tf
from tensorflow import keras

# numpy, matplot 라이브러리를 임포트합니다
import numpy as np
import matplotlib.pyplot as plt

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

'''
'''
plt.figure()
plt.imshow(train_images[0], cmap=plt.cm.binary)
plt.colorbar()
plt.grid(False)
plt.show()

fig = plt.figure(figsize=(10,8))
im1 = plt.imshow(train_images[0], cmap=plt.cm.binary)

ax = plt.gca()
ax.set_xticks(np.arange(0,28,1))
ax.set_yticks(np.arange(0,28,1))
ax.set_xticks(np.arange(-0.5,28,1), minor=True)
ax.set_yticks(np.arange(-0.5,28,1), minor=True)
ax.grid(which='minor', linestyle='-')

plt.colorbar(im1)
plt.show()

print(train_images[0])
