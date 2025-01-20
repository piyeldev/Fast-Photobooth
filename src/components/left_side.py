from PySide6.QtWidgets import QVBoxLayout, QWidget
from components.camera_view import CameraView
from components.queue import Queue
from PySide6.QtCore import Qt

class LeftSide(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(CameraView(), Qt.AlignLeft)
        layout.addWidget(Queue())

