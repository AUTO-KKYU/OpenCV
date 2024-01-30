import cv2 

cap = cv2.VideoCapture("/dev/video0")
src = cv2.imread('/home/kkyu/amr_ws/opencv/data/sky.bmp')

resize_cap = cv2.resize(src, (cap.shape[1], cap.shape[0]))
dst = cv2.addWeighted(cap = cap, alpha = 0.5, src= resize_cap,
                      beta = 0.5, gamma=0)

if not cap.isOpened():
    raise RuntimeError("ERROR! Unadble to open camera")

try:
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f'width = {width}, height = {height}')
    
    while True:
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        
        cv2.imshow('origin', frame)
        cv2.imshow('frame', gray)
        
        if cv2.waitKey(1) == 27:
            break
finally:
    cap.release()
    cv2.destroyAllWindows()