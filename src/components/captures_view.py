from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QScrollArea
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

class CapturesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(6, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.toolbar()
        self.captures()

        layout.addWidget(self.toolbar_widget, alignment=Qt.AlignTop)
        layout.addWidget(self.pics_scroll_area)



    def captures(self):
        self.captures_widget = QWidget()
        layout = QHBoxLayout()
        self.captures_widget.setLayout(layout)
        layout.setContentsMargins(6, 0, 0, 0)
        
        self.pics()

        layout.addWidget(self.pics_scroll_area)



    def vid(self):
        pass

    def pics(self):
        self.pics_scroll_area = QScrollArea()
        self.pics_list = QWidget()
        layout = QHBoxLayout()
        self.pics_scroll_area.setWidget(self.pics_list)
        self.pics_list.setLayout(layout)
        self.pics_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout.setContentsMargins(0, 0, 0, 0)

        self.pics_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pics_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pics_scroll_area.setWidgetResizable(True)
        self.pics_scroll_area.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


        pics_list_height = 0
        for i in range (0, 4):
            object = QLabel()
            object.setPixmap(QPixmap("../assets/imgs/Rectangle.png"))
            object.setMaximumWidth(176)
            object.setMaximumHeight(103)
            object.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            pics_list_height = object.height()
            layout.addWidget(object)

        self.pics_scroll_area.setMinimumHeight(pics_list_height)

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
        layout.addWidget(select_all_and_delete_btn, alignment=Qt.AlignTop)