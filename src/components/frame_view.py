from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from components.frame import Frame
from windows.edit_frame_window import EditFrameWindow
class FrameView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.toolbar()
        self.frame()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.frame_widget, alignment=Qt.AlignTop)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


    def toolbar(self):
        self.toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        self.toolbar.setLayout(toolbar_layout)
        self.toolbar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        toolbar_layout.setContentsMargins(10,0,0,0)

        # label
        label = QLabel("Frame View")
        label.setFont(QFont("Poppins", 12, QFont.Weight.Bold))


        # edit button
        edit_btn = QPushButton("Edit Frame")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
        edit_icon_pxmp = QPixmap("../assets/icons/edit_icon.png")
        edit_icon = QIcon(edit_icon_pxmp)
        edit_btn.setIcon(edit_icon)
        edit_btn.setIconSize(edit_icon_pxmp.rect().size())
        edit_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        edit_btn.clicked.connect(self.open_edit_frame_window)

        edit_btn.setStyleSheet("background-color: #1fb141; padding: 0px 10px; width: 111px; height: 25px; border-radius: 8px;")
        # display elements
        toolbar_layout.addWidget(label)
        toolbar_layout.addWidget(edit_btn)

    def frame(self):
        self.frame_widget = QLabel()
        frame_max_size = QSize(640, 480)
        self.frame_widget.setMaximumWidth(640)

        frame = Frame()
        list_frames = frame.getFrames()
        if len(list_frames) == 0:
            pixmap = QPixmap("../assets/imgs/Rectangle.png")
        else:
            pixmap = QPixmap(frame.activeFrame())

        self.frame_widget.setPixmap(pixmap.scaled(frame_max_size, Qt.KeepAspectRatio))

    def open_edit_frame_window(self):
        self.edit_frame_window = EditFrameWindow()
        self.edit_frame_window.show()
