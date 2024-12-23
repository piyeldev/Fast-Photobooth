from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
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

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.top_bar = TopBar()
        self.main_view()
        self.layout.addWidget(self.top_bar, alignment=Qt.AlignTop)
        self.layout.addWidget(self.main_view_widget)



    def main_view(self):
        self.main_view_widget = QWidget()
        self.main_view_layout = QHBoxLayout()
        self.main_view_widget.setLayout(self.main_view_layout)

        self.main_view_layout.addWidget(CameraView(), alignment=Qt.AlignLeft)
    def load_fonts(self):
        poppins_dir = '../assets/fonts/Poppins'
        poppins_font_files = os.listdir(poppins_dir)

        for font_file in poppins_font_files:
            font_id = QFontDatabase.addApplicationFont(f'{poppins_dir}/{font_file}')
            if font_id == -1:
                print(f"err: font failed to load {font_file}:{font_id}")
        