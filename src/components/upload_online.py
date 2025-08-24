from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QPushButton, QCheckBox, QStyle, QSizePolicy, QMessageBox
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt
from icecream import ic
from components.frame import FramePresets
from components.authenticator import Authenticator
from components.resource_path_helper import resource_path
import re


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
        self.frame_presets = FramePresets()
        self.authenticator = Authenticator()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        label = QLabel("Online Upload Options")
        label.setFont(QFont("Poppins", 16, QFont.Weight.Medium))
        
        self.gdrive()

        layout.addWidget(label)
        layout.addWidget(self.gdrive_grp)

        self.authenticator.is_sucessful.connect(self.updateDriveButton)

        
    def updateDriveButton(self):
        email_address = self.authenticator.get_email_address()
        self.sign_in_btn.setText(f'  {email_address}')

    def gdrive(self):
        self.gdrive_grp = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        self.gdrive_grp.setLayout(layout)

        font = QFont("Poppins", 12, QFont.Weight.DemiBold)
        self.checkbox = QCheckBox("Upload to Google Drive")
        self.checkbox.checkStateChanged.connect(self.isUploadState)
        self.checkbox.setFont(font)
        layout.addWidget(self.checkbox)

        login_and_drive_link = QWidget()
        login_and_drive_link_layout = QHBoxLayout()
        login_and_drive_link.setLayout(login_and_drive_link_layout)
        layout.addWidget(login_and_drive_link)

        self.sign_in_btn = QPushButton("  Log In to Google")
        self.sign_in_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        google_icon = QIcon(resource_path("assets/icons/google_icon.png"))
        self.sign_in_btn.setIcon(google_icon)
        self.sign_in_btn.setFont(font)
        self.sign_in_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sign_in_btn.setStyleSheet("background-color: white; color: black; border-radius: 1em; padding: 10px 14px; ")
        self.sign_in_btn.clicked.connect(self.authenticator.browser_login)
        login_and_drive_link_layout.addWidget(self.sign_in_btn)

        self.drive_link_field = QLineEdit()
        self.drive_link_field.setPlaceholderText("Enter google drive link destination here...")
        self.drive_link_field.setStyleSheet("border-radius: 0.6em; padding: 4px;")
        login_and_drive_link_layout.addWidget(self.drive_link_field)

        self.is_upload_state = self.checkbox.isChecked()

    def get_drive_folder_id(self):
        url = self.drive_link_field.text().strip()
        match = re.search(r'/folders/([a-zA-Z0-9_-]+)', url)

        return match.group(1) if match else None
    
    
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