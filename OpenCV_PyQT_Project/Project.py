import sys, time, datetime, os, cv2, imutils, requests, wavio, math, keras
import numpy as np 
from time import sleep
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sounddevice as sd
import ipywidgets as widgets
import IPython.display as display
import mediapipe as mp
import dlib
from keras.models import load_model

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'



from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtMultimedia import *
from PyQt6.uic import load_ui
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6 import QtCore, QtGui, QtWidgets, QtNetwork

from_class = uic.loadUiType("C:\\Users\\dknjy\\.anaconda\\Project.ui")[0]

class BlankWindow(QWidget):
    image_get = pyqtSignal(name='imageGet')
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Show Image")
        self.start_button()
        self.setGeometry(200, 200, 300, 300)
        self.image_screen = QLabel(self)
        self.image_screen.setPixmap(QPixmap())
        self.image_screen.setGeometry(180, -25, 200, 300)
        self.imageGet.connect(self.show_image)
        self.manager = QtNetwork.QNetworkAccessManager()
        self.show()
        
    def start_button(self):
        # Add Input URL label
        label_url = QLabel("input Image URL", self)
        label_url.setGeometry(10, 100, 70, 30)

        label_example = QLabel("Example URL: https://pokeapi.co/api/v2/pokemon/25", self)
        label_example.setGeometry(10, 60, 300, 30)
        
        # Add Input URL text field
        self.input_url = QLineEdit(self)
        self.input_url.setGeometry(90, 100, 200, 30)
        
        # Add Start button
        self.button_s = QPushButton("Search", self)
        self.button_s.clicked.connect(self.start_button_click)
        self.button_s.setStyleSheet("QPushButton"
                                    "{"
                                    "background:red;}"
                                    "QPushButton:pressed"
                                    "{"
                                    "background:green;}"
                                    )                 
        self.button_s.resize(48, 30)
        self.button_s.move(90, 140)

    def start_button_click(self):
        print("start")
        url = self.input_url.text()  # Get URL from input field
        self.site_request(url)
        
    def site_request(self, url):
        req = QtNetwork.QNetworkRequest(QUrl(url))
        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handle_request)
        self.nam.get(req)
        
    def handle_request(self, reply):
        json2qt = QtCore.QJsonDocument.fromJson 
        er = reply.error()
        if er == QtNetwork.QNetworkReply.NetworkError.NoError:
            qbyte = reply.readAll()
            self.json = json2qt(qbyte)
            self.image_get.emit()
            self.image_label.show()
        else:
            print("Error")
            print(reply.errorString())
    
    def sprite_find_official(dict):
        return dict["sprites"]["other"]["official-artwork"]["front_default"].toString()

    def show_image(self):
        json_dict = self.json
        url_image = BlankWindow.sprite_find_official(json_dict)
        print(url_image)
        image = QImage()
        image.loadFromData(requests.get(url_image).content)
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(image))


class CanvasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("그림판")
        self.image = QImage(self.size(), QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)
        self.penColor = QColor(Qt.GlobalColor.black)  # Default pen color
        self.drawingRectangle = False
        self.rectangleStart = QPoint()
        self.rectangleEnd = QPoint()
        self.drawingThickness = 1  # Default drawing thickness

        # Create a button for selecting color
        self.colorButton = QPushButton('Color', self)
        self.colorButton.setGeometry(10, 10, 100, 30)
        self.colorButton.clicked.connect(self.chooseColor)

        # Create a dropdown menu for selecting drawing thickness
        self.thicknessComboBox = QComboBox(self)
        self.thicknessComboBox.setGeometry(120, 10, 150, 30)
        self.thicknessComboBox.addItem('1px')
        self.thicknessComboBox.addItem('3px')
        self.thicknessComboBox.addItem('5px')
        self.thicknessComboBox.addItem('7px')
        self.thicknessComboBox.currentIndexChanged.connect(self.setDrawingThickness)

        # Create a button for saving the image
        self.saveButton = QPushButton('Save', self)
        self.saveButton.setGeometry(280, 10, 100, 30)
        self.saveButton.clicked.connect(self.saveImage)

        # Create a button for uploading an image
        self.uploadButton = QPushButton('Upload Image', self)
        self.uploadButton.setGeometry(390, 10, 120, 30)
        self.uploadButton.clicked.connect(self.uploadImage)

        # Create a button for adding signature
        self.signatureButton = QPushButton('Add Signature', self)
        self.signatureButton.setGeometry(520, 10, 120, 30)
        self.signatureButton.clicked.connect(self.addSignature)

        # Create a button for resetting the canvas
        self.resetButton = QPushButton('Reset', self)
        self.resetButton.setGeometry(650, 10, 100, 30)
        self.resetButton.clicked.connect(self.resetCanvas)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

            # If drawing rectangles is activated, set the starting point
            if self.drawingRectangle:
                self.rectangleStart = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.MouseButton.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.penColor, self.drawingThickness, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False

            # If drawing rectangles is activated, set the ending point and draw the rectangle
            if self.drawingRectangle:
                self.rectangleEnd = event.pos()
                self.drawRectangle()
                self.drawingRectangle = False

    def chooseColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.penColor = color

    def saveImage(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg)")
        if fileName:
            # Convert QImage to QPixmap for saving
            pixmap = QPixmap.fromImage(self.image)

            # Save the QPixmap to a file
            pixmap.save(fileName)

    def uploadImage(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if fileName:
            loadedImage = QImage(fileName)
            if not loadedImage.isNull():
                self.image = loadedImage
                self.update()

    def addSignature(self):
        # Draw signature at a specific position (here, bottom right)
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.GlobalColor.black, self.drawingThickness))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(self.width() - 150, self.height() - 50, "(인 또는 서명)")
        self.update()

    def drawRectangle(self):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.penColor, self.drawingThickness, Qt.PenStyle.SolidLine))
        painter.drawRect(self.rectangleRegion())
        self.update()

    def rectangleRegion(self):
        # Calculate the region covered by the drawn rectangle
        return QRect(self.rectangleStart, self.rectangleEnd).normalized()

    def resetCanvas(self):
        # Clear the image
        self.image.fill(Qt.GlobalColor.white)
        self.update()

    def setDrawingThickness(self):
        thickness_text = self.thicknessComboBox.currentText()
        self.drawingThickness = int(thickness_text.split('px')[0])

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawingRectangle = True


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MemoDialog(QDialog):
    def __init__(self, memo_text):
        super().__init__()
        self.memo_text = memo_text
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.Output = QTextEdit()
        self.Output.setPlainText(self.memo_text)
        self.Output.setFixedSize(500, 300)
        layout.addWidget(self.Output)

        self.FontNanumGothic = QPushButton("NanumGothic")
        self.FontNanumGothic.clicked.connect(lambda: self.setFont("NanumGothic"))
        layout.addWidget(self.FontNanumGothic)
        
        self.color = QPushButton("Color")
        self.color.clicked.connect(lambda: self.setTextColor(255, 255, 255))
        layout.addWidget(self.color)

        self.FontSizeLabel = QLabel("Input Font Size")
        layout.addWidget(self.FontSizeLabel)

        self.FontSize = QLineEdit()
        layout.addWidget(self.FontSize)

        self.SetFontSize = QPushButton("Apply Font Size")
        self.SetFontSize.clicked.connect(self.setTextSize)
        layout.addWidget(self.SetFontSize)
        
        self.SaveMemo = QPushButton("Save Memo")
        self.SaveMemo.clicked.connect(self.saveMemo)
        layout.addWidget(self.SaveMemo)
        
        self.setLayout(layout)
        self.setWindowTitle("메모장")


    def addText(self):
        input_text = self.Input.text()
        self.Input.clear()
        self.Output.moveCursor(QTextCursor.End)
        self.Output.insertPlainText(input_text + "\n")

    def setFont(self, fontName):
        font, ok = QFontDialog.getFont()
        if ok:
            self.Output.setFont(font)

    def setTextColor(self, r, g, b):
        color = QColorDialog.getColor()
        if color.isValid():
            self.Output.setTextColor(color)

    def setTextSize(self):
        size = int(self.FontSize.text())
        self.Output.setFontPointSize(size)
        
    def saveMemo(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Memo", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, "w") as file:
                    file.write(self.Output.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"{str(e)}")
                

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("세계 최고의 카메라 앱")
        
        self.setStyleSheet("QLineEdit { border-radius: 10px; }")
        self.setStyleSheet("QPushButton:pressed { background-color: gray; border: 2px solid darkgray; }")
        self.sliderRed.setStyleSheet("QSlider::handle {background-color: red}")
        self.sliderGreen.setStyleSheet("QSlider::handle {background-color: green}")
        self.sliderBlue.setStyleSheet("QSlider::handle {background-color: blue}")

        self.sliderHue.setStyleSheet("QSlider::handle {background-color: orange}")
        self.sliderSaturation.setStyleSheet("QSlider::handle {background-color: cyan}")
        self.sliderValue.setStyleSheet("QSlider::handle {background-color: magenta}")


        # Resize Image
        min = self.spinBox.minimum()
        max = self.spinBox.maximum()
        step = self.spinBox.singleStep()
        
        self.editMin.setText(str(min))
        self.editMax.setText(str(max))
        self.editStep.setText(str(step))
        
        self.dial.setRange(min, max)
        self.dial.setSingleStep(step)

        self.btnApply.clicked.connect(self.apply)
        self.dial.valueChanged.connect(self.changeDial)
        
        #-------------------------------------------------#
        self.isCameraOn = False
     
        
        self.pixmap = QPixmap()
        
        self.camera = Camera(self)
        self.camera.daemon = True
                                                                                 
        # File open / save
        self.btnOpen.clicked.connect(self.fileOpen)
        self.btnSave.clicked.connect(self.fileSave)
        self.btnCamera.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        
        self.btnCapture.clicked.connect(self.capture)
        self.btnRecord.clicked.connect(self.record_video)
        self.record = False
        self.video_writer = None
        
        # filtering
        self.btnCanny.clicked.connect(self.set_canny_processing)
        self.btnBlur.clicked.connect(self.set_blurring_processing)
        self.btnThresh.clicked.connect(self.set_threshold_processing)
        self.slider.valueChanged.connect(self.process_video)
        
        min = self.threshold_min = 0
        max = self.threshold_max = 255
        self.slider.setRange(min, max)

        # RGB Color
        self.sliderRed.valueChanged.connect(self.RGB_Image)
        self.sliderGreen.valueChanged.connect(self.RGB_Image)
        self.sliderBlue.valueChanged.connect(self.RGB_Image)
        
        # reset color
        self.btnRGB.clicked.connect(self.RGB_Reset)
        self.btnHsv.clicked.connect(self.HSV_Reset)

        # HSV Color
        self.sliderHue.valueChanged.connect(self.adjustHSV)
        self.sliderSaturation.valueChanged.connect(self.adjustHSV)
        self.sliderValue.valueChanged.connect(self.adjustHSV)
        
        # Additional options
        self.btnMask.clicked.connect(self.inputMask)
        self.btnLaplacian.clicked.connect(self.inputLapla)
        self.btnBlended.clicked.connect(self.inputBlended)
        self.btnGaussian.clicked.connect(self.inputGaussian)
        
        self.btnMemo.clicked.connect(self.open_memo)
        self.btnGraph.clicked.connect(self.open_graph)
        self.btnCanvas.clicked.connect(self.open_canvas)

        # 그림 그리기 관련 변수 설정
        self.drawing = False
        self.lastPoint = QPoint()

        ## 녹음 기능
        self.Return = 0
        self.fs = 16000
        self.a = 0
        self.textBrowser.setText('녹화 길이를 언급하고 start버튼을 클릭 후 말하세요')
        self.btnstart.clicked.connect(self.Startvoicerecord)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # 1초마다 타이머가 작동하도록 설정합니다.

        # 초기 시간을 표시합니다.
        self.updateTime()

        self.btnurl.clicked.connect(self.inputurl)

        self.btnface.clicked.connect(self.detect_faces)
        self.btneye.clicked.connect(self.detect_eyes)
        self.btngesture.clicked.connect(self.detect_gesture)

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.btnlook.clicked.connect(self.detect_look)
        self.btnClose.clicked.connect(self.closeIt)

    def closeIt(self): 
            self.close()

    def updateTime(self):

        # 현재 시간을 가져와서 레이블에 표시합니다.
        current_time = QTime.currentTime()
        time_text = current_time.toString('hh:mm:ss')
        self.labeltime.setText(time_text)
    
    @pyqtSlot()
    def Startvoicerecord(self):
        duration = int(self.input.toPlainText())
        try:
            self.a = sd.rec(int(duration * self.fs), samplerate=self.fs, channels=1, dtype='int16')
            sd.wait()  # 녹음이 완료될 때까지 대기합니다.
            wavio.write('output.wav', self.a, self.fs, sampwidth=2)  # sampwidth를 2로 설정하여 16비트 샘플을 사용합니다.
            self.textBrowser.setText('Recording Done')
        except Exception as e:
            self.textBrowser.setText(f'Error: {str(e)}')

    def open_canvas(self):
        self.canvas_window = CanvasWindow()
        self.canvas_window.show()
        
    def open_memo(self):
        memo_text = ""  # 이전 기록을 불러오는 코드가 들어갈 수 있음
        self.memo_dialog = MemoDialog(memo_text)
        self.memo_dialog.exec()

    def open_graph(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        ax.set_title('Sine wave')
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        # Show plot
        plt.show()
        
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
            
            self.cameraStart()
        else:
            self.btnCamera.setText('Camera On')
            self.isCameraOn = False
                        
            self.cameraStop()

    def cameraStart(self):
        self.camera.running = True 
        self.camera.start()
        self.video = cv2.VideoCapture(0)
        
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

    def RGB_Image(self):
        if self.image is not None:
            red_intensity = self.sliderRed.value()
            green_intensity = self.sliderGreen.value()
            blue_intensity = self.sliderBlue.value()
        
            image = self.image.copy()
            image[:, :, 0] = np.clip(image[:, :, 0] * red_intensity, 0, 255).astype(np.uint8)  # Red channel
            image[:, :, 1] = np.clip(image[:, :, 1] * green_intensity, 0, 255).astype(np.uint8)  # Green channel
            image[:, :, 2] = np.clip(image[:, :, 2] * blue_intensity, 0, 255).astype(np.uint8)  # Blue channel
        
            self.updateImage(image)
 
    def RGB_Reset(self):
        if self.image is not None:
            # 기본값으로 초기화된 이미지 생성
            default_image = self.image.copy()
            
            # 이미지 업데이트
            self.updateImage(default_image)
            
            # RGB 슬라이더 및 기타 관련 UI 업데이트
            self.sliderRed.setMinimum(0)
            self.sliderGreen.setMinimum(0)
            self.sliderBlue.setMinimum(0)
            
            self.sliderRed.setValue(1)
            self.sliderGreen.setValue(1)
            self.sliderBlue.setValue(1)
            
    def HSV_Reset(self):
            # 기본값으로 초기화된 이미지 생성
            default_image = self.image.copy()
            
            # 이미지 업데이트
            self.updateImage(default_image)
            
            # RGB 슬라이더 및 기타 관련 UI 업데이트
            self.sliderHue.setMinimum(0)
            self.sliderSaturation.setMinimum(0)
            self.sliderValue.setMinimum(0)
            
            self.sliderHue.setValue(1)
            self.sliderSaturation.setValue(1)
            self.sliderValue.setValue(1)

    def adjustHSV(self):
        if self.image is not None:
            hue_intensity = self.sliderHue.value()
            saturation_intensity = self.sliderSaturation.value()
            value_intensity = self.sliderValue.value()
        
            image = self.image.copy()
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
            hsv_image[:, :, 0] += hue_intensity
            hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * (1 + saturation_intensity / 255.0), 0, 255)
            hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * (1 + value_intensity / 255.0), 0, 255)
        
            hsv_image[:, :, 0] = np.clip(hsv_image[:, :, 0], 0, 179)
        
            image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
            self.updateImage(image)
            
    def inputMask(self):
        if self.image is not None:
            image = self.image.copy()
        
            ret, mask = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
            self.updateImage(mask)
          
    def inputLapla(self):
        if self.image is not None:
            image = self.image.copy()  
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mask = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
            laplacian = cv2.filter2D(gray, -1, mask)
            
            self.updateImage(laplacian)
              
    def inputBlended(self):
        if self.image is not None:
            image = self.image.copy()
        
            sobelx = cv2.Sobel(image, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
            sobely = cv2.Sobel(image, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
        
            sobelx = np.absolute(sobelx)
            sobely = np.absolute(sobely)
        
            sobelx = np.uint8(255 * sobelx / np.max(sobelx))
            sobely = np.uint8(255 * sobely / np.max(sobely))
        
            blended = cv2.addWeighted(src1=sobelx, alpha=0.5, src2=sobely, beta=0.5, gamma=0)
            self.updateImage(blended)
        
    def inputGaussian(self):
        if self.image is not None:
            image = self.image.copy()
        
            blurred = cv2.GaussianBlur(image, (5, 5), 0)
            self.updateImage(blurred)

    def updateImage(self, image):
        h, w, c = image.shape
        qimage = QImage(image.data, w, h, w * c, QImage.Format.Format_RGB888)
        self.pixmap = QPixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.labelPixmap.width(), self.labelPixmap.height())
        self.labelPixmap.setPixmap(self.pixmap)    
        
    def set_canny_processing(self):
        self.selected_processing_method = "canny"
        self.process_video()

    def set_blurring_processing(self):
        self.selected_processing_method = "blurring"
        self.process_video()

    def set_threshold_processing(self):
        self.selected_processing_method = "threshold"
        self.process_video()            
                
    def process_video(self):
        cap = cv2.VideoCapture(0)

        try:
            ret, frame = cap.read()
            if not ret:
                return

            while ret:
                if self.selected_processing_method == "canny":
                    inversed = ~frame
                    edge = cv2.Canny(frame, 50, 150)
                    processed_frame = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
                elif self.selected_processing_method == "blurring":
                    processed_frame = cv2.GaussianBlur(frame, (11, 11), 0)
                elif self.selected_processing_method == "threshold":
                    intensity = self.slider.value()
                    _, thr = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), intensity, 255, cv2.THRESH_BINARY)
                    processed_frame = cv2.cvtColor(thr, cv2.COLOR_GRAY2BGR)

                qimage = QImage(processed_frame.data, processed_frame.shape[1], processed_frame.shape[0], QImage.Format.Format_BGR888)
                pixmap = QPixmap.fromImage(qimage)

                # 이미지 크기 조절
                size = self.dial.value()

                scaled_pixmap = pixmap.scaled(QSize(size, size), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
                self.labelPixmap.setPixmap(scaled_pixmap)

                self.labelPixmap.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.labelSize.setText(f"{size}x{size}")

                QApplication.processEvents()

                ret, frame = cap.read()
        finally:
            cap.release()

    @pyqtSlot()
    def detect_faces(self):
        # Open the webcam
        cap = cv2.VideoCapture(0)

        try:
            # Load the face cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            while True:
                # Read frames from the webcam
                ret, frame = cap.read()

                if not ret:
                    break

                # Convert the frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces
                faces = face_cascade.detectMultiScale(gray, 1.1, 10)

                # Draw rectangles around the detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]

                    face_text = f'Face Probability: {len(faces)}'
                    cv2.putText(frame, face_text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Convert the processed frame to QPixmap
                height, width, channel = frame.shape
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                bytesPerLine = 3 * width
                qImg = QImage(rgb_frame.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)

                # Update self.labelPixmap with the processed image
                self.labelPixmap.setPixmap(pixmap)

                # Update the UI
                QApplication.processEvents()
                QThread.msleep(30)  # Delay for smoother display, adjust this value as needed

        finally:
            # Release the webcam
            cap.release()
        
    def detect_eyes(self):
        cap = cv2.VideoCapture(0)

        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
            
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 4)

                for (x,y,w,h) in faces:
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]
   
                    eyes = eye_cascade.detectMultiScale(roi_gray)

                    eyes_text = f'eyes Probability: {len(faces)}'
                    cv2.putText(frame, eyes_text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
                # Convert the processed frame to QPixmap
                height, width, channel = frame.shape
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                bytesPerLine = 3 * width
                qImg = QImage(rgb_frame.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)

                # Update self.labelPixmap with the processed image
                self.labelPixmap.setPixmap(pixmap)

                # Update the UI
                QApplication.processEvents()
                QThread.msleep(30)  # Delay for smoother display, adjust this value as needed

        finally:
            # Release the webcam
            cap.release()
        
    def detect_gesture(self):
        cap = cv2.VideoCapture(0)

        try:
            with self.mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
                
                while True:
                    success, image = cap.read()

                    if not success:
                        print("Ignoring empty camera frame.")
                        continue

                    # To improve performance, optionally mark the image as not writeable to pass by reference.
                    image.flags.writeable = False
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image)

                    # Draw the hand annotations on the image.
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(
                                image,
                                hand_landmarks,
                                self.mp_hands.HAND_CONNECTIONS,
                                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                self.mp_drawing_styles.get_default_hand_connections_style())

                    # Convert the processed frame to QPixmap
                    height, width, channel = image.shape
                    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                    bytesPerLine = 3 * width
                    qImg = QImage(rgb_frame.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
                    pixmap = QPixmap.fromImage(qImg)

                    # Update self.labelPixmap with the processed image
                    self.labelPixmap.setPixmap(pixmap)

                    # Update the UI
                    QApplication.processEvents()
                    QThread.msleep(30)  # Delay for smoother display, adjust this value as needed

        finally:
            # Release the webcam
            cap.release()

    def detect_look(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        model = load_model('C:\\Users\\dknjy\\.anaconda\\emotion_model.hdf5')
        expression_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        cap = cv2.VideoCapture(0)

        try:
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (64, 64))
                    face_roi = np.expand_dims(face_roi, axis=-1)
                    face_roi = np.expand_dims(face_roi, axis=0)
                    face_roi = face_roi / 255.0

                    output = model.predict(face_roi)[0]
                    expression_index = np.argmax(output)
                    expression_label = expression_labels[expression_index]
                    cv2.putText(frame, expression_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Convert the processed frame to QPixmap
                height, width = frame.shape[:2]  # Get height and width directly from the frame
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                bytesPerLine = 3 * width
                qImg = QImage(rgb_frame.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)

                # Update self.labelPixmap with the processed image
                self.labelPixmap.setPixmap(pixmap)

                # Update the UI
                QApplication.processEvents()
                QThread.msleep(30)  # Delay for smoother display, adjust this value as needed

        finally:
            cap.release()

    def capture(self):
        if self.labelPixmap.pixmap():
            pixmap = self.labelPixmap.pixmap().copy()  
            pixmap.save("captured_frame.png") 
            print("Frame captured and saved as 'captured_frame.png'")

    def record_video(self):
        if self.record:
            now = datetime.datetime.now().strftime("%d_%H-%M-%S")
            frame = self.labelPixmap.pixmap().toImage().convertToFormat(4)
            width, height = frame.width(), frame.height()
            ptr = frame.constBits()
            ptr.setsize(frame.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # Convert to numpy array
            if self.video_writer is None:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.video_writer = cv2.VideoWriter("C:/Users/dknjy/.anaconda/" + str(now) + ".avi", fourcc, 20.0, (width, height))
            self.video_writer.write(arr)

    def start_recording(self):
        self.record = True

    def stop_recording(self):
        self.record = False
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.record_video)
        self.timer.start(33)  

    def inputurl(self):
        # 버튼 클릭 시 호출되는 함수
        self.blank_window = BlankWindow()
        self.blank_window.show()


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