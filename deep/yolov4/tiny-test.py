from yolov4.tf import YOLOv4
import cv2
import time

#yolo = YOLOv4()
yolo = YOLOv4(tiny=True)

yolo.classes = "coco.names"
yolo.input_size = (640, 480)

yolo.make_model()
#yolo.load_weights("yolov4.weights", weights_type="yolo")
yolo.load_weights("yolov4-tiny.weights", weights_type="yolo")

#yolo.inference(media_path="kite.jpg")

#yolo.inference(media_path="road.mp4", is_image=False)
n = 100
tick = time.time()
for i in range(n):
  #print(i)
  image = cv2.imread('kite.jpg')
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  y = yolo.predict(image)
tock = time.time()
print((tock-tick)/n)
