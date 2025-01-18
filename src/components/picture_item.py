from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt

class PictureItem(QWidget):
    def __init__(self, img:QPixmap):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        if not img:
            raise RuntimeError(f"{__name__}: Invalid image")
        
        self.image = img
        self.lbl = QLabel()
        self.lbl.setPixmap(self.image)
        layout.addWidget(self.lbl)
    
    def setPixmapSize(self, size:QSize):
        self.lbl.setPixmap(self.image.scaled(size, Qt.KeepAspectRatio))

    def overlay(self):
        overlay = QWidget(self.lbl)
        overlay.raise_()
        overlay.setGeometry(self.geometry())
        layout = QHBoxLayout()
        overlay.setLayout(layout)

        overlay.setAutoFillBackground(True)
        overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.8)")

        
