from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QPixmap, QImage, QImageReader
from components.picture_item import PictureItem
import os

class CapturesList(QWidget):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, parent = ...):
        if hasattr(self, "initialized") and self.initialized:
            return
        
        super().__init__(parent)

        self.initialized = True

        self.scroll = QScrollArea(self)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)

        self.container = QWidget(self)
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setAlignment(Qt.AlignLeft)
        self.container.setLayout(self.container_layout)
        self.scroll.setWidget(self.container)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.scroll, Qt.AlignLeft)
        self.setLayout(self.main_layout)

        self.setFixedHeight(190)


    def addPicture(self, path:str):
        print(f'captures_list: {path}')
        
        def init_img():
            picture = PictureItem(path)
            picture.setPixmapSize(QSize(214, 160))
            self.container_layout.addWidget(picture, Qt.AlignTop)


        QTimer.singleShot(100, init_img)
    
    def removeAll(self):
        for i in reversed(range(self.container_layout.count())):
            print(f'{i} - {self.container_layout.itemAt(i).widget()}')
            if self.container_layout.itemAt(i).widget():
                item = self.container_layout.takeAt(i)
                item.widget().deleteLater()

    def removePicture(self, widget):
        for i in range(self.container_layout.count()):
            if self.container_layout.itemAt(i).widget() == widget:
                item = self.container_layout.takeAt(i)
                item.widget().deleteLater()
        return -1