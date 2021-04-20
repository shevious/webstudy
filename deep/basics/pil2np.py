from tensorflow import keras
import numpy as np
from matplotlib import pyplot as plt

# pillow
from PIL import Image

img_url = 'http://sipi.usc.edu/database/preview/misc/4.2.01.png'
img_path = keras.utils.get_file("milk.png", img_url)

img = Image.open(img_path) # use Image.open(image_location)
image = np.array(img.getdata()) # to convert img object to array value use np.array
print(image.shape)
print(img.size[0], img.size[1])
image = image.reshape(img.size[0], img.size[1], 3)

plt.imshow(image)
plt.show()
