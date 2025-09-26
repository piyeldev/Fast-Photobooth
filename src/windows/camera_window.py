from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
from components.camera_view import CameraView
import cv2

class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera")
        self.camera_view = CameraView()

        self.cap = self.camera_view.cap

        self.cam_timer = QTimer()
        self.cam_timer.timeout.connect(self.update_frame)
        self.cam_timer.start(30)  # ~30 FPS

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.cam_placeholder = QLabel()

        layout.addWidget(self.cam_placeholder)

    
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Convert frame to QImage
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.cam_placeholder.setPixmap(QPixmap.fromImage(qimg))