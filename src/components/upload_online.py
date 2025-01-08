from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QStyle, QSizePolicy
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt

class OnlineUploader(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        label = QLabel("Online Upload Options")
        label.setFont(QFont("Poppins", 16, QFont.Weight.Medium))

        self.gdrive()

        layout.addWidget(label)
        layout.addWidget(self.gdrive_grp)

    def gdrive(self):
        self.gdrive_grp = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        self.gdrive_grp.setLayout(layout)

        font = QFont("Poppins", 12, QFont.Weight.DemiBold)
        checkbox = QCheckBox("Upload to Google Drive")
        checkbox.setFont(font)
        

        sign_in_btn = QPushButton("  Log In to Google")
        sign_in_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        google_icon = QIcon("../assets/icons/google_icon.png")
        sign_in_btn.setIcon(google_icon)
        sign_in_btn.setFont(font)
        sign_in_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sign_in_btn.setStyleSheet("background-color: white; color: black; border-radius: 1em; padding: 10px 14px; ")

        layout.addWidget(checkbox)
        layout.addWidget(sign_in_btn)
