from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QScrollBar, QSizePolicy, QMainWindow
from PySide6.QtCore import Qt
from components.topbar import TopBar
from PySide6.QtGui import QFontDatabase
from components.left_side import LeftSide
import os
from components.tools_view import ToolsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()

        self.main_view_widget = QWidget()
        self.main_view_widget.setMaximumWidth(screen_width -30)
        self.main_view_layout = QHBoxLayout()
        self.main_view_layout.setContentsMargins(0, 0, 0, 0)
        self.main_view_widget.setLayout(self.main_view_layout)
        self.left_side = LeftSide()

        self.main_view_layout.addWidget(self.left_side, alignment=Qt.AlignTop)
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
        
        print(f'screen width: {screen_width}, current width: {self.width()}')

        

    
        