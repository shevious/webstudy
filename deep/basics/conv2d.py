import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from matplotlib import image as mp_image
import cv2

img_url = 'https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png'
img_path = keras.utils.get_file("lena.png", img_url)

#img_file = keras.preprocessing.image.load_img(img_path)
img = cv2.imread(img_path)
img = cv2.resize(img, dsize=(100,100), interpolation=cv2.INTER_AREA)
cv2.imwrite('lena100.png', img)
img = mp_image.imread('lena100.png')

width,height,_ = img.shape

'''
'''
kernel = np.array([ [-1, 0, 1],
                    [-1, 0, 1],
                    [-1, 0, 1] ])
kernel = np.array([ [ 1, 1, 1],
                    [ 1, 1, 1],
                    [ 1, 1, 1] ])/9

out = np.zeros((height-2,width-2,3))

for j in range(0, height-2, 1):
  for i in range(0, width-2, 1):
    for l in range(0, 3, 1):
      for k in range(0, 3, 1):
        out[j][i] += img[j+l][i+k]*kernel[l][k]

#out = np.abs(out)*2
out = np.clip(out, 0, 1)
#out *= 200
#out += 128
#plt.imshow(out)
#plt.show()
mp_image.imsave('filter.png', out)

print(out)
'''
from PIL import Image

img = Image.open('myImage.png') # use Image.open(image_location) 
image_data = np.array(img) # to convert img object to array value use np.array

'''
