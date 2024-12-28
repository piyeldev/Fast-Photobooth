from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtGui import QFont, QIcon, QPixmap

class FrameView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.toolbar()
        self.frame()
        # layout.addWidget(QLabel("hello"))
        layout.addWidget(self.toolbar)
    
    def toolbar(self):
        self.toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        self.toolbar.setLayout(toolbar_layout)

        # label
        label = QLabel("Frame View")
        label.setFont(QFont("Poppins", 14, QFont.Weight.DemiBold))

        # edit button
        edit_btn = QPushButton("Edit Frame")
        edit_btn.setFont(QFont("Poppins", 12, QFont.Weight.Medium))
        edit_icon_pxmp = QPixmap("../assets/icons/edit_icon.png")
        edit_icon = QIcon(edit_icon_pxmp)
        edit_btn.setIcon(edit_icon)
        edit_btn.setIconSize(edit_icon_pxmp.rect().size())
        edit_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # display elements
        toolbar_layout.addWidget(label)
        toolbar_layout.addWidget(edit_btn)


    def frame(self):
        pass