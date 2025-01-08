from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtGui import QPixmap, QIcon, QFont
from PySide6.QtCore import Qt, QSize

class ShutterBtns(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.take_pic_btn()
        self.record_vid_btn()

        self.layout.addWidget(self.take_pic_btn_widg)
        self.layout.addWidget(self.record_btn)


    def take_pic_btn(self):
        self.take_pic_btn_widg = QPushButton()
        self.take_pic_btn_widg.setCursor(Qt.CursorShape.PointingHandCursor)
        self.take_pic_btn_widg.setFixedWidth(53)
        self.take_pic_btn_widg.setFixedHeight(53)
        self.take_pic_pxmp = QPixmap("../assets/icons/camera_icon.png")
        self.take_pic_icon = QIcon()
        self.take_pic_btn_widg.setIconSize(self.take_pic_pxmp.rect().size())
        self.take_pic_icon.addPixmap(self.take_pic_pxmp)
        self.take_pic_btn_widg.setIcon(self.take_pic_icon)
        self.take_pic_btn_widg.setStyleSheet("""
        QPushButton {
            border-radius: 25px; 
            background-color: #1fb141; 
        }
        """)
    def record_vid_btn(self):
        self.record_btn = QPushButton("Record")
        self.record_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        record_pxmp = QPixmap("../assets/icons/video-icon.png")
        record_icon = QIcon()
        record_icon.addPixmap(record_pxmp)

        self.record_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        record_btn_font = QFont("Poppins", 14, QFont.Weight.Bold)
        self.record_btn.setFont(record_btn_font)

        self.record_btn.setIcon(record_icon)
        self.record_btn.setIconSize(record_pxmp.rect().size())

        self.record_btn.setStyleSheet("""
        QPushButton {
            width: 130px;
            height: 53px;
            border-radius: 25px; 
            background-color: #1fb141; 
        }
        """)