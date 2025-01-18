from PySide6.QtWidgets import QWidget, QFrame, QSizePolicy, QVBoxLayout, QSpacerItem, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QScrollArea
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QSize
from components.picture_item import PictureItem
from components.captures_list import CapturesList

class CapturesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(6, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.toolbar()

        self.pictures = []
        self.captures_list = CapturesList(parent=self)

        layout.addWidget(self.toolbar_widget, alignment=Qt.AlignTop)
        layout.addWidget(self.captures_list)

    def vid(self):
        pass

        
    def pics(self):
        pass
        # self.pics_scroll_area = QScrollArea()
        # self.pics_list = QWidget()
        # self.pics_layout = QHBoxLayout()
        # self.pics_scroll_area.setWidget(self.pics_list)
        # self.pics_list.setLayout(self.pics_layout)
        # self.pics_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        

        # self.pics_layout.setContentsMargins(0, 0, 0, 0)

        # self.pics_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.pics_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.pics_scroll_area.setWidgetResizable(True)
        # self.pics_scroll_area.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


        # max_size = QSize(214, 160)
        # pic1 = PictureItem(QPixmap("../assets/imgs/test.png"))
        # pic1.setPixmapSize(max_size)
        # self.pics_layout.addWidget(pic1)


        # for i in range (0, 4):
        #     object = QLabel()
        #     object.setPixmap(QPixmap("../assets/imgs/Rectangle.png"))
        #     object.setMaximumWidth(176)
        #     object.setMaximumHeight(103)
        #     object.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #     pics_list_height = object.height()
        #     layout.addWidget(object)


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

        layout.addWidget(captures_label, alignment=Qt.AlignTop)
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        layout.addWidget(select_all_and_delete_btn, alignment=Qt.AlignTop)