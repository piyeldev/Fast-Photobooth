from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QScrollBar, QSizePolicy, QMainWindow
from PySide6.QtCore import Qt
from components.topbar import TopBar
from PySide6.QtGui import QFontDatabase
from components.camera_view import CameraView
import os
from components.tools_view import ToolsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_fonts()
        self.setWindowTitle("Fast Photo")
        self.widget = QWidget()

        self.setCentralWidget(self.widget)
        self.main_layout = QVBoxLayout()
        self.widget.setLayout(self.main_layout)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.main_layout.setSpacing(0)

        self.top_bar = TopBar()
        self.main_view()

        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addWidget(self.scrollable)




    def main_view(self):
        self.main_view_widget = QWidget()
        self.main_view_layout = QHBoxLayout()
        self.main_view_layout.setContentsMargins(20, 0, 0, 0)
        self.main_view_widget.setLayout(self.main_view_layout)
        self.cam_view = CameraView()

        self.main_view_layout.addWidget(self.cam_view, alignment=Qt.AlignTop)
        self.main_view_layout.addWidget(ToolsView())

        self.scrollable = QScrollArea()
        self.scrollable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollable.setWidgetResizable(True)
        self.scrollable.setWidget(self.main_view_widget)

        # Apply custom scrollbar style
        self.scrollable.setStyleSheet("""
            QScrollArea {
                border: none;
            }

        """)

    def load_fonts(self):
        poppins_dir = '../assets/fonts/Poppins'
        poppins_font_files = os.listdir(poppins_dir)

        for font_file in poppins_font_files:
            font_id = QFontDatabase.addApplicationFont(f'{poppins_dir}/{font_file}')
            if font_id == -1:
                print(f"err: font failed to load {font_file}:{font_id}")
        