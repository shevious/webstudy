import multiprocessing

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        #other initialization stuff

    def run(self):
        while True:
            image = self.task_queue.get()
            print('image-get')
            #Do computations on image
            self.result_queue.put("text")
        return

import cv2

if __name__ == '__main__':
    tasks = multiprocessing.Queue()
    results = multiprocessing.Queue()
    consumer = Consumer(tasks,results)
    consumer.start()

    #Creating window and starting video capturer from camera
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    #Try to get the first frame
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        if not rval or cv2.waitKey(1) == ord("q"):
            break

        if tasks.empty() and results.empty():
           tasks.put(frame)
        else:
           if not results.empty():
             text = results.get()
             #Add text to frame
             print(text)
           cv2.putText(frame,text,(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

        #Showing the frame with all the applied modifications
        cv2.imshow("preview", frame)

        #Getting next frame from camera
        rval, frame = vc.read()
