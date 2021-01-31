import cv2 as cv2
import imutils as im

class CameraStream():
    def __init__(self, width, height, camPort):
        self.width = width
        self.height=height
        self.cap = cv2.VideoCapture(camPort)
        self.stopped = False
    def getFrame(self):
        frame=self.cap.read()
        return cv2.resize(frame, (self.width, self.height))
