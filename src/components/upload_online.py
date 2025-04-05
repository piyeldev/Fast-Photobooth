from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QStyle, QSizePolicy, QMessageBox
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt
from icecream import ic
from components.frame import FramePresets


class OnlineUploader(QWidget):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, "initialized") and self.initialized:
            return
        
        super().__init__()
        self.initialized = True

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        label = QLabel("Online Upload Options")
        label.setFont(QFont("Poppins", 16, QFont.Weight.Medium))

        self.gdrive()

        layout.addWidget(label)
        layout.addWidget(self.gdrive_grp)

        self.frame_presets = FramePresets()

    def gdrive(self):
        self.gdrive_grp = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        self.gdrive_grp.setLayout(layout)

        font = QFont("Poppins", 12, QFont.Weight.DemiBold)
        self.checkbox = QCheckBox("Upload to Google Drive")
        self.checkbox.checkStateChanged.connect(self.isUploadState)
        self.checkbox.setFont(font)
        

        # self.sign_in_btn = QPushButton("Log In to Google")
        # self.sign_in_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # google_icon = QIcon("../assets/icons/google_icon.png")
        # self.sign_in_btn.setIcon(google_icon)
        # self.sign_in_btn.setFont(font)
        # self.sign_in_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.sign_in_btn.setStyleSheet("background-color: white; color: black; border-radius: 1em; padding: 10px 14px; ")

        layout.addWidget(self.checkbox)
        # layout.addWidget(self.sign_in_btn)

        self.is_upload_state = self.checkbox.isChecked()

    def getIsUploadState(self):
        return self.is_upload_state

    def isUploadState(self, state):
        isQRPlaceholderEmpty = self.frame_presets.isCurrentPresetQRPlaceholderEmpty()
        if state == Qt.CheckState.Checked and isQRPlaceholderEmpty:
            # Create a QMessageBox with Yes and No buttons
            user_response = QMessageBox.question(
                self,
                "Warning",
                "No QR Code Placeholder set, proceed?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No  # Default button
            )

            # Handle the user's response
            if user_response == QMessageBox.Yes:
                print("User chose to proceed.")
            else:
                print("User chose not to proceed.")
                self.checkbox.setCheckState(Qt.CheckState.Unchecked)  # Uncheck the checkbox
                return
            
        if state == Qt.CheckState.Checked:
            self.is_upload_state = True
            # self.sign_in_btn.setEnabled(True)
        else:
            self.is_upload_state = False
            # self.sign_in_btn.setEnabled(False)