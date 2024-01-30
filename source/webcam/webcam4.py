import cv2 

cap = cv2.VideoCapture("/dev/video0")

if not cap.isOpened():
    raise RuntimeError("ERROR! Unable to open camera")

try:
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f'width = {width}, height = {height}')
    
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('./text__.avi', fourcc, 20,
                          (width,height), isColor = False)
    
    while True:
        ret, frame = cap.read()
        
        if not ret: #ret이 False면 중지
            break

        inversed = ~frame # 반전

        edge = cv2.Canny(frame, 50, 150) # 윤곽선

        # 윤곽선은 그레이스케일 영상이므로 저장이 안된다. 컬러 영상으로 변경
        edge_color = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

        out.write(edge_color) # 영상 데이터만 저장. 소리는 X
        
        cv2.imshow('frame', edge_color)
        

        if cv2.waitKey(1) == 27:
            break

finally:
    cap.release()
    out.release()
    cv2.destroyAllWindows()