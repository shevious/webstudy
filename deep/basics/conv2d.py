import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from matplotlib import image as mp_image

img_file = keras.preprocessing.image.load_img('Vd-Orig.png')
width,height = img_file.size
kernel = np.array([ [ 0, 0, 0],
                    [-1, 0, 1],
                    [ 0, 0, 0] ])
'''
kernel = np.array([ [ 1, 1, 1],
                    [ 1, 1, 1],
                    [ 1, 1, 1] ])/9
'''

img_arr = keras.preprocessing.image.img_to_array(img_file)
#img = np.array(img_arr)
img = mp_image.imread('Vd-Orig.png')

out = np.zeros((height-2,width-2,3))

for j in range(0, height-2, 1):
  for i in range(0, width-2, 1):
    for l in range(0, 3, 1):
      for k in range(0, 3, 1):
        out[j][i] += img[j+l][i+k]*kernel[l][k]

out = np.abs(out)*2
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
