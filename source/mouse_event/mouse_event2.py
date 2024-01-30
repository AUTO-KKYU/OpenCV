import cv2 
import numpy as np 

img = np.ones((512,512,3), np.uint8)

def draw_circle(event, x, y, flags, param): 
    if event == cv2.EVENT_LBUTTONDOWN: 
        cv2.circle(img, (x,y), 30, (50,50,200), -1)
        
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(img, (x,y), 30, (200,50,50), -1)

cv2.namedWindow(winname = 'my_first_drawing')  # 윈도우 생성
cv2.setMouseCallback('my_first_drawing', draw_circle, img) # cv2.setMouseCallback(윈도우, 콜백 함수, 사용자 정의 데이터)을 의미


while True:
    cv2.imshow('my_first_drawing', img) # 어떤 이미지를 계속 보여줌 
    
    if cv2.waitKey(10) == 27: # key를 기다리겠다(10 ms 동안, 0.1초), 입력받는 값이 27이면 무한루프 빠져나가겠다
        break

cv2.destroyAllWindows()  # 모든 창들을 꺼줘라