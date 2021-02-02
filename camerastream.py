import cv2 as cv2
import imutils as im
from threading import Thread
class CameraStream():
    def __init__(self, width, height, camPort):
        self.width = width
        self.height=height
        self.cap = cv2.VideoCapture(camPort)
        (self.grabbed, self.frame) = self.cap.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed,self.frame)=self.cap.read()
    def read(self):
        return cv2.resize(self.frame, (self.width, self.height))
    def getFrame(self):
        rev, frame=self.cap.read()
        return cv2.resize(frame, (self.width, self.height))
    def release(self):
        self.cap.release()