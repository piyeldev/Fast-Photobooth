from PySide6.QtWidgets import QWidget, QFrame, QSizePolicy, QVBoxLayout, QSpacerItem, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QScrollArea
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QSize, QTimer
from components.picture_item import PictureItem
from components.captures_list import CapturesList

class CapturesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(6, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.pictures = []
        self.captures_list = CapturesList(parent=self)

        self.toolbar()

        layout.addWidget(self.toolbar_widget, alignment=Qt.AlignTop)
        layout.addWidget(self.captures_list)

    def vid(self):
        pass


    def toolbar(self):
        layout = QHBoxLayout()
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.toolbar_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # label
        captures_label = QLabel("Captures")
        captures_label.setFont(QFont("Poppins", 12, QFont.Weight.Bold))

        # button
        select_all_and_delete_btn = QPushButton("Select All and Delete")
        select_all_and_delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        select_all_and_delete_btn.setIcon(QPixmap("../assets/icons/trash_icon.png"))
        select_all_and_delete_btn.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
        select_all_and_delete_btn.setStyleSheet("background-color: #1fb141; padding: 4px 10px; border-radius: 8px;")

        select_all_and_delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        select_all_and_delete_btn.clicked.connect(self.captures_list.removeAll)

        layout.addWidget(captures_label, alignment=Qt.AlignTop)
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        layout.addWidget(select_all_and_delete_btn, alignment=Qt.AlignTop)
    