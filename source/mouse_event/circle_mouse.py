import cv2
import numpy as np

# 마우스 왼쪽을 클릭하고 위로 스크롤 하고 radius가 커지고 반대는 작아짐
def mouse_event(event, x, y, flags, param):
    global radius
    
    if event == cv2.EVENT_FLAG_LBUTTON:  # 마우스 왼쪽 버튼이 눌려져 있음
        cv2.circle(param, (x, y), radius, (255, 0, 0), 2)
        cv2.imshow("draw", src)

    elif event == cv2.EVENT_MOUSEWHEEL: # 마우스 휠을 좌우로 움직이는 경우
        if flags > 0:
            radius += 1
        elif radius > 1:
            radius -= 1

radius = 3
src = np.full((500, 500, 3), 255, dtype=np.uint8)

cv2.imshow("draw", src)
cv2.setMouseCallback("draw", mouse_event, src)
cv2.waitKey()