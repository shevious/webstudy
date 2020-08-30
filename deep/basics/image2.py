from tensorflow import keras
import matplotlib.pyplot as plt
import cv2
image_path = keras.utils.get_file("seoul.jpg", "http://data.si.re.kr/photo_ndownload/21555")
image = cv2.imread(image_path)
# convert opencv RGB for opencv
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(10,7))
plt.imshow(image)
plt.show()

