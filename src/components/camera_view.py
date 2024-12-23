from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class CameraView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.toolbar()
        self.layout.addWidget(self.toolbar_widget)

    def toolbar(self):
        self.toolbar_widget = QWidget()
        self.toolbar_widget_layout = QHBoxLayout()
        self.toolbar_widget.setLayout(self.toolbar_widget_layout)

        self.cam_view_lbl = QLabel("Camera View")
        # self.cam_view_lbl.setStyleSheet("padding-left: 5px;")
        # self.cam_view_lbl_font = QFont("Poppins", 14, QFont.Weight.Bold)

        self.toolbar_widget_layout.addWidget(self.cam_view_lbl, alignment=Qt.AlignLeft)

