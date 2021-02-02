import cv2 as cv2
import imutils as im
import numpy as np
from centroidtracker import CentroidTracker
from camerastream import CameraStream

class PersonDetector():
    def __init__(self, width, height, camPort):
        self.ct=CentroidTracker()
        self.targetID=-1000000
        self.targetCentroid = []
        self.radius=20
        self.cap = CameraStream(width, height, camPort).start()
        self.haar_cascade = cv2.CascadeClassifier("data/HS.xml")
        self.frameCount=0
        self.frameCaptureNumber=7
        self.thresholdX = int(width/2)
        self.thresholdY = (int)(height/2)
        self.width=width
        self.height=height

    def frameAdd(self):
        self.frameCount+=1
    def checkFrameCount(self):
        if self.frameCount%self.frameCaptureNumber==0:
            return True
        return False
    def robotMoveDirection(self, centroid, center):
        print(centroid, " ", center)
        cX = center[0]
        cY = center[1]
        targetX = centroid[0]
        targetY = centroid[1]
        diffX = cX-targetX
        diffY = cY-targetY
        hors = "Move: "
        verts = " and "
        if targetX < cX-self.radius:
            hors += "Left "+str(np.abs(diffX))+" pixels"
        elif targetX > cX+self.radius:
            hors += "Right "+str(np.abs(diffX))+" pixels"
        else:
            hors = ""
            verts = "Move: "
        if targetY < cY-self.radius:
            verts += "Up "+str(np.abs(diffY))+" pixels"
        elif targetY > cY+self.radius:
            verts += "Down "+str(np.abs(diffY))+" pixels"
        else:
            verts = ""
        return hors+verts
    def updateObjectIDs(self, upper_body):
        return self.ct.update(upper_body)
    def detectPerson(self):
        frame = self.cap.getFrame()
        centerX = -10000
        centerY = -100000
        cColor = (0, 0, 255)
        if self.checkFrameCount():
            try:
            # using a greyscale picture, also for faster detection
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                upper_body = self.haar_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=12,
                    # Min size for valid detection, changes according to video size or body size in the video.
                    minSize=(50, 100),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                if len(upper_body) > 0:
                    (x, y, w, h) = upper_body[0]
                    # creates green color rectangle with a thickness size of 1
                    centerX = (int)(x+w/2)
                    centerY = (int)(y+h/2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    cv2.line(frame, (centerX, y), (centerX, y+h), (255, 0, 0), 1)
                    cv2.line(frame, (x, centerY), (x+w, centerY), (255, 0, 0), 1)
                    cv2.circle(frame, (centerX, centerY), 1, (0, 0, 255), 1)
                    # creates green color text with text size of 0.5 & thickness size of 2
                    cv2.putText(frame, "Head and Shoulders Detected", (x + 5, y + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    if np.abs(centerX-self.thresholdX) <= 20 and np.abs(centerY-self.thresholdY) <= 20:
                        cColor = (0, 255, 0)
                    else:
                        cColor = (0, 0, 255)
                objects = self.updateObjectIDs(upper_body)
                # checking if the id is the same as the one detected
                if len(list(objects.items())) > 0:
                    targetID = list(objects.items())[0][0]
                    targetCentroid = list(objects.items())[0][1]
                    if targetCentroid[0] == centerX and targetCentroid[1] == centerY:
                        cv2.putText(frame, str(targetID), (targetCentroid[0], targetCentroid[1]),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        cv2.circle(
                            frame, (targetCentroid[0], targetCentroid[1]), 4, (0, 255, 0), -1)
                else:
                    targetID = -100000
                    targetCentroid = []
                print(self.robotMoveDirection(targetCentroid, (self.width/2, self.height/2)))
            except Exception as e:
                print(str(e))
                return frame
            #threshold center lines
        cv2.circle(frame, (self.thresholdX, self.thresholdY), self.radius, cColor, 3)
        return frame
    def release(self):
        self.cap.release()