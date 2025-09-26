import sys
import cv2
from PySide6.QtCore import QTimer, Qt, QObject
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenCV Camera")

        self.label = QLabel("Camera feed here")
        self.label.setAlignment(Qt.AlignCenter)
        self.start_btn = QPushButton("Start Recording")
        self.stop_btn = QPushButton("Stop Recording")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        self.setLayout(layout)

        # OpenCV camera capture
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FPS, 30)       # control FPS
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.is_recording = False
        self.out = None

        # Timer to grab frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # ~30 FPS

        self.start_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        # Write frame if recording
        if self.is_recording and self.out:
            self.out.write(frame)

        # Convert frame to QImage
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def start_recording(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter("output.mp4", fourcc, 30.0, (1280, 720))
        self.is_recording = True
        print("Recording started...")

    def stop_recording(self):
        self.is_recording = False
        if self.out:
            self.out.release()
            self.out = None
        print("Recording stopped.")

    def closeEvent(self, event):
        self.cap.release()
        if self.out:
            self.out.release()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CameraWidget()
    win.show()
    sys.exit(app.exec())

class CameraNew(QObject):
    def __init__(self):
        super().__init__()

        self.is_recording = False
        self.out = None

    def closeEvent(self, event):
        self.cap.release()
        if self.out:
            self.out.release()
        super().closeEvent(event)
        
    def initialize(self, cam_index: int, fps: int, resW: int, resH: int):
        # OpenCV camera capture
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FPS, cam_index)       # control FPS
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resW)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resH)

    def update_frame(self, label):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        # Write frame if recording
        if self.is_recording and self.out:
            self.out.write(frame)

        # Convert frame to QImage
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qimg))