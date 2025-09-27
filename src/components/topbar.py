from PySide6.QtWidgets import QHBoxLayout, QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtGui import QFont, QFontDatabase, QPainter, QColor, QPixmap, QIcon
from PySide6.QtCore import Qt
from components.resource_path_helper import resource_path

class TopBar(QWidget):
    def __init__(self):
        super().__init__()
        # topbar layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.setObjectName("topbar")
        #set constraints
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)

        self.layout.setContentsMargins(0,0,0,0)

        self.heading_banner()
        self.settings_btn()
        self.layout.addWidget(self.heading_banner)
        self.layout.addWidget(self.settings_btn_widget, alignment=Qt.AlignRight)


    def heading_banner(self):
        self.heading_banner = QWidget()
        self.heading_banner_layout = QHBoxLayout()
        self.heading_banner.setLayout(self.heading_banner_layout)

        # vertical heading text
        self.heading_texts_widget = QWidget()
        self.heading_texts_layout = QVBoxLayout()
        self.heading_texts_widget.setLayout(self.heading_texts_layout)

        self.heading = QLabel("Fast Photo")
        self.heading_font = QFont('Poppins', 20, QFont.Weight.ExtraBold)
        self.heading.setObjectName("heading_name")

        self.version_label = QLabel("v1.2beta-dev")
        self.version_label_font = QFont('Poppins', 10, QFont.Weight.Light)

        self.heading.setFont(self.heading_font)
        self.version_label.setFont(self.version_label_font)

        self.heading_texts_layout.setSpacing(0)
        self.heading_texts_layout.addWidget(self.heading, alignment=Qt.AlignTop)
        self.heading_texts_layout.addWidget(self.version_label, alignment=Qt.AlignTop)

        #with the icon - PARTIAL
        self.heading_circle_lbl = QLabel()
        self.heading_circle_lbl.setPixmap(QPixmap(resource_path("assets/imgs/logo.png")))
        
        self.heading_banner_layout.setAlignment(Qt.AlignLeft)
        self.heading_banner_layout.addWidget(self.heading_circle_lbl)
        self.heading_banner_layout.addWidget(self.heading_texts_widget)

    def settings_btn(self):
        self.settings_btn_widget = QPushButton()
        self.settings_btn_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn_widget.setObjectName("settings_btn")

        self.settings_icon_img = QPixmap(resource_path("assets/icons/settings-icon.png"))
        self.settings_icon = QIcon(self.settings_icon_img)
        self.settings_btn_widget.setStyleSheet("background-color: #1fb141; height: 60; width: 60; border-radius: 30px;")

        self.settings_btn_widget.setIcon(self.settings_icon)
        self.settings_btn_widget.setIconSize(self.settings_icon_img.size())


        


