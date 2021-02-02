import cv2 as cv2
import tensorflow as tf
import numpy as np
import matplotlib as mpl
import imutils as im
from centroidtracker import CentroidTracker
from persondetector import PersonDetector
from camerastream import CameraStream
import time

cv2.startWindowThread()
pDetector = PersonDetector(600, 480, 0)
time.sleep(2)
prevFrameTime =0
newFrameTime=0
while(True):
    newFrameTime = time.time()
    fps = 1/(newFrameTime-prevFrameTime)
    frame = pDetector.detectPerson()
    prevFrameTime = newFrameTime
    cv2.putText(frame, str(fps), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow('frame', frame)
    pDetector.frameAdd()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pDetector.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
