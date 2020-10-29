import face_recognition
import time
import cv2

image = face_recognition.load_image_file("clinton003.jpg")
print(image.shape)
print('recog start')
tick = time.time()
n = 1
for i in range(n):
    face_locations = face_recognition.face_locations(image)
tock = time.time()
print(face_locations)
print('averate recog time=', (tock-tick)/100)

#cv2.rectangle(image, face_locations[0][0:2], face_locations[0][2:4], (0,0,255), 3)
cv2.rectangle(image, (face_locations[0][1], face_locations[0][0]),
    (face_locations[0][3], face_locations[0][2]), (0,0,255), 3)
cv2.imshow('clinton', image)
print(face_locations[0][0:2])
while cv2.waitKey(1) != ord("q"):
    pass
