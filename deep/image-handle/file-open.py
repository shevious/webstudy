from PIL import Image
#import skimage as sk
#from skimage import io as sk_io
#import cv2

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image as mp_image

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

#file_path = filedialog.askopenfilename()
file_path = filedialog.askopenfilenames()

print(file_path)

images = []

for file in file_path:
  print(file)
  pil_image = Image.open(file)
  images.append(pil_image)

# Set up a figure of an appropriate size
fig = plt.figure(figsize=(12, 12))

image_num = 0
num_images = len(images)
# loop through the images
for image_idx in range(num_images):
    # Keep an incrementing count of each image
    a=fig.add_subplot(1, num_images, image_idx+1)
    # Add the image to the plot
    image_plot = plt.imshow(images[image_idx])
    # Add a caption with the folder name
    a.set_title("Image " + str(image_idx+1))
        
# Show the plot
plt.show()

image_num = 0
num_images = len(images)
# loop through the images
for image_idx in range(num_images):
    # Keep an incrementing count of each image
    a=fig.add_subplot(1, num_images, image_idx+1)
    # Add the image to the plot
    image_plot = plt.imshow(images[image_idx])
    # Add a caption with the folder name
    a.set_title("Image " + str(image_idx+1))
plt.show()
