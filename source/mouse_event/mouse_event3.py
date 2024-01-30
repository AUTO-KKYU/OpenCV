import sys
import numpy as np
import cv2

# 이전 마우스 좌표를 저장할 전역 변수
oldx = oldy = -1

# 마우스 이벤트에 대한 콜백 함수
def on_mouse(event, x, y, flags, param):
    global oldx, oldy

    # 왼쪽 마우스 버튼을 눌렀을 때
    if event == cv2.EVENT_LBUTTONDOWN:
        oldx, oldy = x, y
        print('EVENT_LBUTTONDOWN: %d, %d' % (x, y))

    # 왼쪽 마우스 버튼을 뗐을 때
    elif event == cv2.EVENT_LBUTTONUP:
        print('EVENT_LBUTTONUP: %d, %d' % (x, y))

    # 마우스가 창 위에서 움직일 때
    elif event == cv2.EVENT_MOUSEMOVE:
        # 왼쪽 마우스 버튼이 눌려 있는 경우 (드래깅 중)
        if flags & cv2.EVENT_FLAG_LBUTTON:
            # 이전 좌표에서 현재 좌표까지 빨간색 선을 그림
            cv2.line(img, (oldx, oldy), (x, y), (0, 0, 255), 4, cv2.LINE_AA)
            # 업데이트된 이미지를 표시
            cv2.imshow('image', img)
            # 다음 반복을 위해 이전 좌표를 현재 좌표로 업데이트
            oldx, oldy = x, y

# 하얀 이미지를 생성 (480x640 픽셀, 3개의 컬러 채널(BGR))
# ones : 하얀 이미지
# zeros : 검은 이미지 
img = np.zeros((480, 640, 3), dtype=np.uint8) * 255

cv2.namedWindow('image')
cv2.setMouseCallback('image', on_mouse, img)

# 초기 이미지를 표시
cv2.imshow('image', img)
cv2.waitKey()
cv2.destroyAllWindows()
