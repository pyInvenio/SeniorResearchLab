import cv2 as cv2
import imutils as im
from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

class PiCameraStream():
    def __init__(self, width, height, framerate):
        self.width = width
        self.height = height
        self.camera = PiCamera()
        self.camera.resolution = (width, height)
        self.camera.framerate=framerate
        self.rawCapture = PiRGBArray(self.camera, size = self.camera.resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format ="bgr", use_video_port=True)
        self.frame = None
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        for f in self.stream:
            self.frame = f.array
            self.rawCapture.truncate(0)
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def getFrame(self):
        return self.frame

    def stop(self):
        self.stopped = True
