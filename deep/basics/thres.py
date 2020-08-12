import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import vgg19
import matplotlib.pyplot as plt

base_image_path = keras.utils.get_file("seoul.jpg", "https://i.imgur.com/F28w3Ac.jpg")

import cv2
image = cv2.imread(base_image_path, cv2.IMREAD_GRAYSCALE)
#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = image/1.
_, image = cv2.threshold(image,127,255, cv2.THRESH_BINARY)
#cv2.imwrite("tt.tif", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
#cv2.imwrite("tt.tiff", image, [int(cv2.IMWRITE_TIFF_RESUNIT), 256])
#cv2.imwrite("tt.tiff", image)
#cv2.imwrite("tt.png", image)
#cv2.imwrite("tt.tiff", image, [cv2.IMWRITE_TIFF_COMPRESSION, 5])
cv2.imwrite("tt.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
cv2.imwrite("tt.tiff", image, [cv2.IMWRITE_TIFFTAG_BITSPERSAMPLE, 8])
'''
plt.imshow(image, cmap=plt.cm.gray)
plt.show()
'''
print(image.shape)
