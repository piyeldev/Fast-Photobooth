from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QLabel, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QSize, QTimer, Signal
from PySide6.QtGui import QPixmap, QImage, QImageReader
from components.picture_item import PictureItem
from components.frame import FramePresets
from components.image_overlayer import ImageOverlayer
from components.pixmap_viewer import PixmapViewer
import threading, os
from icecream import ic

class CapturesList(QWidget):
    _instance = None
    new_picture = Signal(str)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized") and self.initialized:
            return
        
        super().__init__()

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
        self.pictures = []

        self.frame_presets = FramePresets()
        self.pixmap_viewer = PixmapViewer()
        self.image_overlayer = ImageOverlayer()
        self.image_overlayer.overlay_image_made.connect(self.displayOverlayedImage)

    def displayOverlayedImage(self, path:str):
        # # ic()
        if len(self.pictures) == 0:
            self.frame_presets.setCurrentOverlayedImage("")
        else:
            self.frame_presets.setCurrentOverlayedImage(path)
        self.pixmap_viewer.setPixmapToView(QPixmap(path))

    def addPicture(self, path:str):
        print("addPicture " + path)
        if path in self.pictures:
            return
        
        frame, placeholder_list = self.instantiateVariablesForOverlaying()
        no_of_placeholders = len(placeholder_list)
        
        self.init_img(path, placeholder_list, frame, no_of_placeholders)
    
    def init_img(self, path, placeholder_list, frame, no_of_placeholders):
        print("init_img " + path)
        # ic()
        if len(self.pictures) >= no_of_placeholders:
            QMessageBox(
                QMessageBox.Information, 
                "No. of pictures exceeded", 
                "Number of pictures cannot exceed no. of placeholders for the frame. Try adding more placeholder if missed.", 
                QMessageBox.Ok
                ).exec()
        else:
            picture = PictureItem(path)
            self.container_layout.addWidget(picture, Qt.AlignTop)
            self.pictures.append(path)
            print(f'PICTURES: {self.pictures}')

            self.threadOverlayImage(placeholder_list, frame, self.pictures)

            # ic(self.pictures)


    def instantiateVariablesForOverlaying(self):
        current_index = self.frame_presets.getCurrentIndex()
        frame = self.frame_presets.getPresets()[current_index]["frame_path"]
        placeholder_list = self.frame_presets.getPresets()[current_index]["placeholders"]

        return frame, placeholder_list
    
    def removeAll(self):
        for i in reversed(range(self.container_layout.count())):
            if self.container_layout.itemAt(i).widget():
                item = self.container_layout.takeAt(i)
                item.widget().deleteLater()

        current_index = self.frame_presets.getCurrentIndex()
        current_frame = self.frame_presets.getPresets()[current_index]["frame_path"]
        self.frame_presets.setCurrentOverlayedImage("")
        self.pixmap_viewer.setPixmapToView(QPixmap(current_frame))
        self.pictures.clear()

    def threadOverlayImage(self, placeholder_list, frame, pictures):
        threading.Thread(
                target=self.image_overlayer.overlay_image, 
                args=(pictures, placeholder_list, frame), 
                daemon=True).start()
        
    def removePicture(self, widget, image_path: str):
        for i in range(self.container_layout.count()):
            if self.container_layout.itemAt(i) and self.container_layout.itemAt(i).widget() == widget:
                item = self.container_layout.takeAt(i)
                item.widget().deleteLater()
        
        if image_path in self.pictures:
            self.pictures.remove(image_path)

        frame, placeholder_list = self.instantiateVariablesForOverlaying()

        self.threadOverlayImage(placeholder_list, frame)

        return -1