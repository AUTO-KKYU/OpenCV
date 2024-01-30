import cv2 
import numpy as np 

# img라는 변수에 주어진 모양의 배열을 1로 가득차게 
# 512 x 512 size의 컬러색상
img = np.ones((512,512,3), np.uint8)

def draw_circle(event, x, y, flags, param): # pass를 지우면 문장의 시작 위치가 맞지 않음 
    if event == cv2.EVENT_LBUTTONDOWN: # 마우스 왼쪽 버튼이 눌려지는 경우
        cv2.circle(img, (x,y), 30, (50,50,200), -1)
# interpreter : 함수에 종속되었다고 보겠다 pass를 쓰지 않으면

cv2.namedWindow(winname = 'my_first_drawing')  # 윈도우 생성
cv2.setMouseCallback('my_first_drawing', draw_circle, img) # cv2.setMouseCallback(윈도우, 콜백 함수, 사용자 정의 데이터)을 의미


while True:
    cv2.imshow('my_first_drawing', img) # 어떤 이미지를 계속 보여줌 
    
    if cv2.waitKey(10) == 27: # key를 기다리겠다(10 ms 동안, 0.1초), 입력받는 값이 27이면 무한루프 빠져나가겠다
        break

cv2.destroyAllWindows()  # 모든 창들을 꺼줘라

# ASCII 코드 형식
# esc 누르면 창에서 빠져나감 -> 27
# enter 누르면 창에서 빠져나감 -> 13
# TAB 누르면 창에서 빠져나감 -> 9

# 터미널에서 환경에 진입한 후 직접 실행 가능
# ex) python mouse_event.py  -> 상위 폴더에서 실행해야 함 (이 파일을 가지고 있는 폴더 위치)





