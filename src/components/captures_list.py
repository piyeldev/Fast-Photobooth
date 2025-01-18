from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QSize
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
        self.scroll.setWidgetResizable(True)

        self.container = QWidget(self)
        self.container_layout = QHBoxLayout(self.container)
        self.container.setLayout(self.container_layout)
        self.scroll.setWidget(self.container)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.scroll)
        self.setLayout(self.main_layout)

        self.setMaximumHeight(280)

        self.setStyleSheet("border: 2px solid red;")
        

    def addPicture(self, path:str):
        print(f'captures_list: {path}')
        
        # pic = QPixmap(path)
        # print(pic)
        picture = PictureItem(QPixmap(path, "1"))
        picture.setPixmapSize(QSize(214, 160))
        self.container_layout.addWidget(picture)
        

