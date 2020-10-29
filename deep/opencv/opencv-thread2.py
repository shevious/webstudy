
from datetime import datetime

class CountsPerSec:
    """
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """

    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0

    def start(self):
        self._start_time = datetime.now()
        return self

    def increment(self):
        self._num_occurrences += 1

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        if (elapsed_time == 0):
            return 0
        return self._num_occurrences / elapsed_time

import argparse
import cv2
#from CountsPerSec import CountsPerSec
#from VideoGet import VideoGet
#from VideoShow import VideoShow

def putIterationsPerSec(frame, iterations_per_sec, boxes=[]):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    for box in boxes:
        #cv2.rectangle(frame, (box[0], box[2]), (box[1], box[3]), (0,0,255), 3)
        cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), (0,0,255), 3)
    return frame

def noThreading(source=0):
    """Grab and show video frames without multithreading."""

    cap = cv2.VideoCapture(source)
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or cv2.waitKey(1) == ord("q"):
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        cps.increment()


from threading import Thread
import cv2

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True

from threading import Thread
import cv2

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True

def threadVideoShow(source=0):
    """
    Dedicated thread for showing video frames with VideoShow object.
    Main thread grabs video frames.
    """

    cap = cv2.VideoCapture(source)
    (grabbed, frame) = cap.read()
    video_shower = VideoShow(frame).start()
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or video_shower.stopped:
            video_shower.stop()
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

import face_recognition
import multiprocessing

class RecogFaceMulti(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        #other initialization stuff
        self.recogcps = None

    def run(self):
        while True:
            image = self.task_queue.get()
            #Do computations on image
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(image)
            if self.recogcps == None:
                self.recogcps = CountsPerSec()
                self.recogcps.start()
            self.recogcps.increment()
            print('recog fps=',self.recogcps.countsPerSec())

            #self.result_queue.put("text")
            self.result_queue.put(face_locations)
        return


def threadBothRecog(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    tasks = multiprocessing.Queue()
    results = multiprocessing.Queue()

    consumer = RecogFaceMulti(tasks,results)
    consumer.start()

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()
    boxes = []

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            consumer.terminate()
            break

        frame = video_getter.frame

        if tasks.empty() and results.empty():
            tasks.put(frame)
        else:
            if not results.empty():
                boxes = results.get()

        frame = putIterationsPerSec(frame, cps.countsPerSec(), boxes)
        video_shower.frame = frame
        cps.increment()

#noThreading()
#threadVideoShow()
#threadBoth()

if __name__ == '__main__':
    threadBothRecog()
