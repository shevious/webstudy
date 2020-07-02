import os
root = 'samples'

try:
    os.mkdir(root)
except Exception:
    pass

try:
    os.mkdir(root+'/laptop')
except Exception:
    pass

try:
    os.mkdir(root+'/person')
except Exception:
    pass

import requests
url = 'https://upload.wikimedia.org/wikipedia/ko/2/24/Lenna.png'
r = requests.get(url, allow_redirects=True)
open(root+'/person/'+'01.jpg', 'wb').write(r.content)

import requests
#url = 'https://file-examples.com/wp-content/uploads/2017/10/file_example_PNG_500kB.png'
url = 'https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_100kB.jpg'
r = requests.get(url, allow_redirects=True)
open(root+'/laptop/'+'02.jpg', 'wb').write(r.content)

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image as mp_image
import cv2

src_folder = "samples"

# Set up a figure of an appropriate size
fig = plt.figure(figsize=(12, 12))

# loop through the subfolders
for root, folders, filenames in os.walk(src_folder):
    print(root, folders, filenames)
    image_num = 0
    num_folders = len(folders)
    for folder in sorted(folders):
        # Keep an incrementing count of each image
        image_num +=1
        # Find the first image file in the folder
        file_name = os.listdir(os.path.join(root,folder))[0]
        # Get the full path from the root folder
        file_path = os.path.join(root,folder, file_name)
        # Open the file using the matplotlib.image library
        # image = mp_image.imread(file_path)
        # Open the file using the opencv library
        image = cv2.imread(file_path)
        # convert opencv RGB for opencv
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Add the image to the figure (which will have a row for each folder, each containing one column for the image)
        a=fig.add_subplot(num_folders, 1, image_num)
        # Add the image to the plot
        image_plot = plt.imshow(image)
        # Add a caption with the folder name
        a.set_title(folder)
        
# Show the plot
plt.show()
