import cv2 as cv2
import tensorflow as tf
import numpy as np
import matplotlib as mpl
import imutils as im
from trackableobject import TrackableObject
from centroidtracker import CentroidTracker
import time

#globals
width = 800
height = 600
thresholdX = (int)(width/2)
thresholdY = (int)(height/2)
thresholdradius = (int)((width+height)/2*0.5)

ct = CentroidTracker()
targetID = -100000
targetCentroid = []
# initialize the cascade
# haar_upper_body_cascade = cv2.CascadeClassifier( 
#     "C:/Users/rootw/Documents/Robotics/Senior Lab/Python test/data/HS.xml") #Uncomment these if on Windows and change route name cuz it somehow doesnt work without it
haar_upper_body_cascade = cv2.CascadeClassifier("data/HS.xml")
radius = 20


def robotMoveDirection(centroid, center):
    print(centroid, " ", center)
    cX = center[0]
    cY = center[1]
    targetX = centroid[0]
    targetY = centroid[1]
    diffX = cX-targetX
    diffY = cY-targetY
    hors = "Move: "
    verts = " and "
    if targetX < cX-radius:
        hors += "Left "+str(np.abs(diffX))+" pixels"
    elif targetX > cX+radius:
        hors += "Right "+str(np.abs(diffX))+" pixels"
    else:
        hors = ""
        verts = "Move: "
    if targetY < cY-radius:
        verts += "Up "+str(np.abs(diffY))+" pixels"
    elif targetY > cY+radius:
        verts += "Down "+str(np.abs(diffY))+" pixels"
    else:
        verts = ""
    return hors+verts


def persondetection(cap):
    global targetID, targetCentroid
    # reading the frame
    ret, frame = cap.read()
    centerX = -10000
    centerY = -100000
    cColor = (0, 0, 255)
    # resizing for faster detection
    try:
        frame = cv2.resize(frame, (width, height))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        upper_body = haar_upper_body_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=12,
            # Min size for valid detection, changes according to video size or body size in the video.
            minSize=(50, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
       # print(upper_body)
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
            if np.abs(centerX-thresholdX) <= 20 and np.abs(centerY-thresholdY) <= 20:
                cColor = (0, 255, 0)
            else:
                cColor = (0, 0, 255)
        objects = ct.update(upper_body)
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
        print(robotMoveDirection(targetCentroid, (width/2, height/2)))
    except Exception as e:
        print(str(e))
        return frame
        #threshold center lines
    cv2.circle(frame, (thresholdX, thresholdY), radius, cColor, 3)
    return frame


cv2.startWindowThread()
cap = cv2.VideoCapture(0)
time.sleep(2)

while(True):
    frame = persondetection(cap)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
