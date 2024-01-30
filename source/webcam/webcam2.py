import cv2

cap = cv2.VideoCapture("/dev/video0")

src = cv2.imread('/home/kkyu/amr_ws/opencv/data/sky.bmp')

resize_cap = cv2.resize(src, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        dst = cv2.addWeighted(frame, 0.5, resize_cap, 0.5, 0)

        cv2.imshow('Original', frame)
        cv2.imshow('Grayscale', gray)
        cv2.imshow('Blended', dst)

        if cv2.waitKey(1) == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
