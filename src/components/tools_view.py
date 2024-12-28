from PySide6.QtWidgets import QWidget, QVBoxLayout
from components.frame_view import FrameView

class ToolsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(FrameView())