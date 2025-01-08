from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
import components.camera_view
from components.frame_view import FrameView
from components.captures_view import CapturesView
from components.name_of_customer_getter import NameForm
from components.upload_online import OnlineUploader
from components.print_options import PrintOptions

class ToolsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,10,0)
        layout.addWidget(FrameView())
        layout.addWidget(CapturesView())
        layout.addWidget(NameForm())
        layout.addWidget(OnlineUploader())
        layout.addWidget(PrintOptions())

        # FOR DEBUGGING
        # self.setStyleSheet("border: 1px solid red;")

