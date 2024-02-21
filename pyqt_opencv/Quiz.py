import sys
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtMultimedia import *
from PyQt6 import uic 
import cv2, imutils
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import *
from PyQt6.QtMultimediaWidgets import QVideoWidget
from playsound import playsound
import time
import datetime
import numpy as np 


from_class = uic.loadUiType('C:\\Users\\dknjy\\.anaconda\\Quiz.ui')[0]

    
class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setStyleSheet(
            "QLineEdit { border-radius: 10px; }"
            "QPushButton { border-radius: 10px;"
            "              background-color: lightgray;"
            "              border: 2px solid gray;"
            "              padding: 5px;"
            "}"
            "QPushButton:pressed {"
            "              background-color: gray;"
            "              border: 2px solid darkgray;"
            "}"
        )
     
        vbox = QVBoxLayout()
        
        min = self.spinBox.minimum()
        max = self.spinBox.maximum()
        step = self.spinBox.singleStep()
        
        self.editMin.setText(str(min))
        self.editMax.setText(str(max))
        self.editStep.setText(str(step))
        
        self.dial.setRange(min, max)
        self.dial.setSingleStep(step)

        # Resize Image
        self.btnApply.clicked.connect(self.apply)
        self.dial.valueChanged.connect(self.changeDial)
        
        #####3--------------------#####3
        
        self.isCameraOn = False
        self.isRecStart = False
        self.btnRecord.hide()
        
        self.pixmap = QPixmap()
        
        self.camera = Camera(self)
        self.camera.daemon = True
        
        self.record = Camera(self)
        self.record.daemon = True
        
        # File open / save
        self.btnOpen.clicked.connect(self.fileOpen)
        self.btnSave.clicked.connect(self.fileSave)
        self.btnCamera.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        self.btnRecord.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)
        self.btnCapture.clicked.connect(self.capture)
        

        # filtering
        self.btnCanny.clicked.connect(self.canny)
        self.btnBlur.clicked.connect(self.blurring)
        self.btnThresh.clicked.connect(self.threshold)
        self.slider.valueChanged.connect(self.threshold)
        
        min = self.threshold_min = 0
        max = self.threshold_max = 255
        self.slider.setRange(min, max)

        # color
        self.sliderRed.valueChanged.connect(self.inputRed)
        self.sliderGreen.valueChanged.connect(self.inputGreen)
        self.sliderBlue.valueChanged.connect(self.inputBlue)
        
        self.sliderHue.valueChanged.connect(self.inputHue)
        self.sliderSaturation.valueChanged.connect(self.inputSaturation)
        self.sliderValue.valueChanged.connect(self.inputValue)
        
        self.labelPixmap.installEventFilter(self)
        self.drawing = False
        self.lastPoint = QPoint()
        
    def eventFilter(self, obj, event):
        if obj == self.labelPixmap:
            if event.type() == QEvent.Type.MouseButtonPress:
                self.drawing = True
                self.lastPoint = event.pos()
                return True
            elif event.type() == QEvent.Type.MouseMove:
                if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
                    self.drawLineTo(event.pos())
                    self.lastPoint = event.pos()
                    return True
            elif event.type() == QEvent.Type.MouseButtonRelease:
                if event.button() == Qt.MouseButton.LeftButton and self.drawing:
                    self.drawLineTo(event.pos())
                    self.drawing = False
                    return True
        return super().eventFilter(obj, event)
    
    def drawLineTo(self, endPoint):
        painter = QPainter(self.pixmap)
        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.lastPoint = endPoint
        self.labelPixmap.setPixmap(self.pixmap)

    def eventFilter(self, obj, event):
        if obj == self.labelPixmap:
            if event.type() == QEvent.Type.MouseButtonPress:
                self.drawing = True
                self.lastPoint = event.pos()
                self.checkCornerPress(event.pos())
                return True
            elif event.type() == QEvent.Type.MouseMove:
                if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
                    self.drawLineTo(event.pos())
                    self.lastPoint = event.pos()
                    return True
            elif event.type() == QEvent.Type.MouseButtonRelease:
                if event.button() == Qt.MouseButton.LeftButton and self.drawing:
                    self.drawLineTo(event.pos())
                    self.drawing = False
                    return True
        return super().eventFilter(obj, event)
    
    def checkCornerPress(self, pos):
        image_width = self.pixmap.width()
        image_height = self.pixmap.height()
        corner_threshold = 20  # Adjust this threshold as needed
        
        if pos.x() <= corner_threshold and pos.y() <= corner_threshold:
            # Top-left corner pressed
            self.applyCornerEffect("top-left")
        elif pos.x() >= image_width - corner_threshold and pos.y() <= corner_threshold:
            # Top-right corner pressed
            self.applyCornerEffect("top-right")
        elif pos.x() <= corner_threshold and pos.y() >= image_height - corner_threshold:
            # Bottom-left corner pressed
            self.applyCornerEffect("bottom-left")
        elif pos.x() >= image_width - corner_threshold and pos.y() >= image_height - corner_threshold:
            # Bottom-right corner pressed
            self.applyCornerEffect("bottom-right")
    
    def applyCornerEffect(self, corner):
        # Implement the effect you desire for each corner here
        # Example: Apply a rotation or bending effect to the image
        if corner == "top-left":
            # Apply transformation to simulate bending or folding
            # Example: Rotate the image slightly
            rotated_pixmap = self.pixmap.transformed(QTransform().rotate(10))
            self.labelPixmap.setPixmap(rotated_pixmap)
        elif corner == "top-right":
            pass
        elif corner == "bottom-left":
            pass
        elif corner == "bottom-right":
            pass



    def apply(self):
        min = self.editMin.text()
        max = self.editMax.text()
        step = self.editStep.text()
        
        self.spinBox.setRange(int(min), int(max))
        self.spinBox.setSingleStep(int(step))

        self.dial.setRange(int(min), int(max))
        self.dial.setSingleStep(int(step))
        
        
    def changeSpinbox(self):
        actualValue = self.spinBox.value()
        self.dial.setValue(actualValue)
        self.updateImageSize(actualValue)
        

    def changeDial(self):
        actualValue = self.dial.value()
        self.spinBox.setValue(actualValue)
        self.updateImageSize(actualValue)


    def updateImageSize(self, size):
        if self.pixmap:
            scaled_pixmap = self.pixmap.scaled(QSize(size, size), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.labelPixmap.setPixmap(scaled_pixmap)
            self.labelPixmap.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.labelSize.setText(f"{size}x{size}")
  

    def capture(self):
        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')       
        filename = self.now + '.png'
        
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, self.image)
        
                
    def updateRecording(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.writer.write(self.image)
        
        
    def clickRecord(self):
        if self.isRecStart == False:
            self.btnRecord.setText('Rec Stop')
            self.isRecStart = True
            
            self.recordingStart()
        else:
            self.btnRecord.setText('Rec Start')
            self.isRecStart = False    

            self.recordingStop()
            
            
    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.avi'
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    


        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (width, height))
        self.fourcc = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        
    def recordingStop(self):
        self.record.running = False
        
        if self.isRecStart == True:
            self.writer.release()
    
    
    def updateCamera(self):
        retval, image = self.video.read()
        if retval:
            self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
            h, w, c = self.image.shape
            qimage = QImage(self.image.data, w, h, w*c, QImage.Format.Format_RGB888)
        
            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.labelPixmap.width(), self.labelPixmap.height())
        
            self.labelPixmap.setPixmap(self.pixmap)
            
    def clickCamera(self):
        if self.isCameraOn == False:
            self.btnCamera.setText('Camera Off')
            self.isCameraOn = True
            self.btnRecord.show()
            self.btnCapture.show()
            
            self.cameraStart()
        else:
            self.btnCamera.setText('Camera On')
            self.isCameraOn = False
            self.btnRecord.hide()
            self.btnCapture.hide()
            
            self.cameraStop()
            self.recordingStop()

            
    def cameraStart(self):
        self.camera.running = True 
        self.camera.start()
        self.video = cv2.VideoCapture("/dev/video0")
        
    def cameraStop(self):
        self.camera.running = False
        self.count = 0
        self.video.release

        
    def fileOpen(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', '/home/kkyu/amr_ws/opencv/data', 'Image (*.*)')
        if file:
            self.image = cv2.imread(file)
            if self.image is not None:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                self.updateImage(self.image)
        
                    
    def fileSave(self):
        # 파일 형식자도 같이 적어줘야 함
        filename = QFileDialog.getSaveFileName(self, 'save image', './', 'img')
        self.pixmap.save(filename[0])

    def inputRed(self, intensity):
        if self.image is not None:
            image = self.image.copy()
            image[:, :, 0] = np.clip(image[:, :, 0] * intensity , 0, 255).astype(np.uint8)  # Red channel
            self.updateImage(image)

    def inputGreen(self, intensity):
        if self.image is not None:
            image = self.image.copy()
            image[:, :, 1] = np.clip(image[:, :, 1] * intensity , 0, 255).astype(np.uint8)  # Green channel
            self.updateImage(image)

    def inputBlue(self, intensity):
        if self.image is not None:
            image = self.image.copy()
            image[:, :, 2] = np.clip(image[:, :, 2] * intensity , 0, 255).astype(np.uint8)  # Blue channel
            self.updateImage(image)

    def updateImage(self, image):
        h, w, c = image.shape
        qimage = QImage(image.data, w, h, w * c, QImage.Format.Format_RGB888)
        self.pixmap = QPixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.labelPixmap.width(), self.labelPixmap.height())
        self.labelPixmap.setPixmap(self.pixmap)    
        
    def inputHue(self, intensity):
        if self.image is not None:
            image = self.image.copy()
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv_image[:, :, 0] += intensity
            image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
            self.updateImage(image)
            
    def inputSaturation(self, intensity):
        if self.image is not None:
            image = self.image.copy()
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv_image[:, :, 1] += intensity
            image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
            self.updateImage(image)
            
    def inputValue(self, intensity):
        if self.image is not None:
            image = self.image.copy()
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv_image[:, :, 2] += intensity
            image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
            self.updateImage(image)
            


        
        
        
    def canny(self):
        cap = cv2.VideoCapture("/dev/video0")

        try:
            while True:
                ret, frame = cap.read()

                if not ret:  # ret이 False면 중지
                    break

                inversed = ~frame  # 반전

                edge = cv2.Canny(frame, 50, 150)  # 윤곽선

                # 윤곽선은 그레이스케일 영상이므로 저장이 안된다. 컬러 영상으로 변경
                edge_color = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

                qimage = QImage(edge_color.data, edge_color.shape[1], edge_color.shape[0], QImage.Format.Format_BGR888)
                pixmap = QPixmap.fromImage(qimage)
                pixmap = pixmap.scaled(self.labelPixmap.size(), Qt.AspectRatioMode.KeepAspectRatio)
                self.labelPixmap.setPixmap(pixmap)
                QApplication.processEvents()  # Process events to update GUI
        finally:
            cap.release()
            
    def blurring(self):
        cap = cv2.VideoCapture("/dev/video0")  # Use index 0 for default camera
        
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                image = cv2.GaussianBlur(frame, (11, 11), 0)
                
                qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_BGR888)
                pixmap = QPixmap.fromImage(qimage)
                pixmap = pixmap.scaled(self.labelPixmap.size(), Qt.AspectRatioMode.KeepAspectRatio)
                # Assuming self.labelPixmap is a QLabel
                self.labelPixmap.setPixmap(pixmap)
                QApplication.processEvents()  # Update the GUI
        finally:
            cap.release()
            
            
    def threshold(self, intensity):
        cap = cv2.VideoCapture("/dev/video0")
        
        try:
            while True:
                actualValue = self.slider.value()  # 슬라이더로부터 실제 값 가져오기

                ret, frame = cap.read()

                if not ret:
                    break
 
                ret, thr = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), actualValue, 255,
                                         cv2.THRESH_BINARY)

                height, width = thr.shape
                qimage = QImage(thr.data, width, height, width, QImage.Format.Format_Grayscale8)

                pixmap = QPixmap.fromImage(qimage)
                pixmap = pixmap.scaled(self.labelPixmap.size(), Qt.AspectRatioMode.KeepAspectRatio)

                self.labelPixmap.setPixmap(pixmap)
                QApplication.processEvents()

        finally:
            cap.release()

                

class Camera(QThread):
    update = pyqtSignal()
    
    # parent 지워도 됨
    def __init__(self, sec = 0, parent = None):
        super().__init__()
        self.main = parent
        self.running = True
        
    def run(self):
        count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(0.05)
            
    def stop(self):
        self.running = False 
        
        

    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)  # 프로그램 실행
    myWindows = WindowClass()     # 화면 클래스 생성
    myWindows.show()              # 프로그램 화면 보이기
    sys.exit(app.exec())          # 프로그램을 종료까지 동작시킴
