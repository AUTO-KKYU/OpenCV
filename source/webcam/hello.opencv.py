# 카메라 사용해야 함

import cv2

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = capture.read()
    # frame = cv2.flip(frame,0)  상하 반전
    
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("VideoFrame", gray) # frame  -> gray
    
    if cv2.waitKey(10) == 27:
        break

capture.release()
cv2.destroyAllWindows()