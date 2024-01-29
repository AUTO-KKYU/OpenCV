# 카메라 사용해야 함

import cv2

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = capture.read()
    cv2.imshow("VideoFrame", frame)
    
    if cv2.waitKey(10) == 27:
        break
    
capture.release()
cv2.destroyAllWindows()