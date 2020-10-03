import cv2
from tqdm import tqdm
from matplotlib import pyplot as plt

video_reader = cv2.VideoCapture('/Users/shevious/Downloads/Funny-Raccoons.mp4')

nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
print('nb_frames = ', nb_frames)
print('frame_h = ', frame_h)
print('frame_w = ', frame_w)
for i in tqdm(range(nb_frames)):
    _, image = video_reader.read()
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('frame',gray)
    cv2.imshow('frame', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        #cv2.imshow('video with bboxes', image)
        #print(image[3])
        #plt.imshow(image)
        #plt.show()

video_reader.release()
cv2.destroyAllWindows()

