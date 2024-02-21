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



from_class = uic.loadUiType('/home/kkyu/amr_ws/opencv/pyqt_opencv/opencv.ui')[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    
        self.isCameraOn = False
        self.isRecStart = False
        self.btnRecord.hide()
        self.btnCapture.hide()
        
        self.pixmap = QPixmap()
        
        self.camera = Camera(self)
        self.camera.daemon = True
        
        self.record = Camera(self)
        self.record.daemon = True
        
        self.btnOpen.clicked.connect(self.openFile)
        self.btnCamera.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        self.btnRecord.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)
        self.btnCapture.clicked.connect(self.capture)
        # self.btnVideo.clicked.connect(self.openVideo)

        
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
            self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())
        
            self.label.setPixmap(self.pixmap)

                
        
    def openFile(self):
        file = QFileDialog.getOpenFileName(self, 'Open File','/home/kkyu/amr_ws/opencv/data', 'Image (*.*)')
            
        image = cv2.imread(file[0])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
        h, w, c = image.shape 
        qimage = QImage(image.data, w, h, w*c, QImage.Format.Format_RGB888)
            
        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())
            
        self.label.setPixmap(self.pixmap)

        
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
            time.sleep(0.07)
            
    def stop(self):
        self.running = False 



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec())