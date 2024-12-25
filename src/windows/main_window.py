from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt
from components.topbar import TopBar
from PySide6.QtGui import QFontDatabase
from components.camera_view import CameraView
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.load_fonts()
        self.setWindowTitle("Fast Photo")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.setWindowFlags(Qt.Widget)  # Correct flag for normal widgets

        self.main_layout.setSpacing(0)

        self.top_bar = TopBar()
        self.main_view()

        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addWidget(self.scrollable)




    def main_view(self):
        self.main_view_widget = QWidget()
        self.main_view_layout = QHBoxLayout()
        self.main_view_layout.setContentsMargins(20, 0, 20, 0)
        self.main_view_widget.setLayout(self.main_view_layout)
        self.cam_view = CameraView()
        self.main_view_layout.addWidget(self.cam_view, alignment=Qt.AlignLeft)

        self.scrollable = QScrollArea()
        self.scrollable.setWidgetResizable(True)
        self.scrollable.setWidget(self.main_view_widget)

        # Apply custom scrollbar style
        self.scrollable.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background-color: transparent;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #292929;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical {
                background: none;
                height: 14px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background: none;
                height: 14px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
                background: none;
            }
            QScrollBar::handle:vertical:hover {
                background: #383838;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def load_fonts(self):
        poppins_dir = '../assets/fonts/Poppins'
        poppins_font_files = os.listdir(poppins_dir)

        for font_file in poppins_font_files:
            font_id = QFontDatabase.addApplicationFont(f'{poppins_dir}/{font_file}')
            if font_id == -1:
                print(f"err: font failed to load {font_file}:{font_id}")
        