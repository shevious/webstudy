#-*- coding:utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
from tensorflow import keras

img_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Checkerboard_identity.svg/800px-Checkerboard_identity.svg.png'
img_path = keras.utils.get_file("checkerboard.jpg", img_url)
img = cv2.imread(img_path)

rows, cols, ch = img.shape

# 점3개를 변환 전과 변환 후로 나누어 지정
pts1 = np.float32([[200,100],[400,100],[200,200]])
pts2 = np.float32([[200,300],[400,200],[200,400]])

# pts1의 좌표에 표시. Affine 변환 후 이동 점 확인.
cv2.circle(img, (200,100), 10, (255,0,0),-1)
cv2.circle(img, (400,100), 10, (0,255,0),-1)
cv2.circle(img, (200,200), 10, (0,0,255),-1)

# Affine 변환 텐서 얻기
M = cv2.getAffineTransform(pts1, pts2)

# Affine 변환하기
dst = cv2.warpAffine(img, M, (cols,rows))

plt.subplot(121),plt.imshow(img),plt.title('image')
plt.subplot(122),plt.imshow(dst),plt.title('Affine')
plt.show()


center = (cols/2, rows/2)
angle = 90
scale = 1
# 회전 변환
M = cv2.getRotationMatrix2D(center, angle, scale)
# Affine 변환하기
dst = cv2.warpAffine(img, M, (cols,rows))
plt.subplot(121),plt.imshow(img),plt.title('image')
plt.subplot(122),plt.imshow(dst),plt.title('Affine')
plt.show()
