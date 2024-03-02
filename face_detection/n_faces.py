import cv2
import numpy as np
import time

faceClassifier = cv2.CascadeClassifier("/home/kkyu/amr_ws/opencv/source/webcam/haarcascade_frontalface_default.xml")

videoCam = cv2.VideoCapture('/dev/video0')

if not videoCam.isOpened():
    print("Cannot access the camera")
    exit()

qButtonPressed = False
while (qButtonPressed == False):
    ret, frame = videoCam.read()

    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faceList = faceClassifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2)

        for (x, y, w, h) in faceList:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        text = "Number of detected faces = " + str(len(faceList))

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (0, 30), font, 1, (255, 0, 0), 1)

        cv2.imshow("Result", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            qButtonPressed = True
            break

videoCam.release()
cv2.destroyAllWindows()
