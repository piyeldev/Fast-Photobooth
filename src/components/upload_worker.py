from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google.auth.exceptions
from PIL import Image
from icecream import ic
import os

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from components.frame import FramePresets
from components.authenticator import Authenticator


import qrcode


class UploadWorker(QObject):
    output = Signal(str)
    errorSig = Signal(str)
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
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.CREDENTIALS_FILE = '../assets/credentials/credentials.json'
        self.TOKEN_FILE = "token.json"

        self.frame_presets = FramePresets()
        self.authenticator = Authenticator()

        # TASK: try to authenticate in init when already signed in, 
        # but if theres no login token, then let user sign in using button
        # put user gmail when already signed in

    
    
    def upload_and_overlay(self, img_path:str, name: str, drive_link: str):
        current_index = self.frame_presets.getCurrentIndex()
        position = self.frame_presets.getPresets()[current_index]["qr_code_placeholder"]
        image_path = img_path
        image = Image.open(image_path)
        file_link = self.upload_photo(image_path, name, drive_link)
        if not file_link:
            return
        
        if position:
            qr_code = qrcode.make(file_link)
            qr_code = qr_code.convert(image.mode)

            x, y = int(position["x"]), int(position["y"])
            qr_code = qr_code.resize((int(position["width"]), int(position["height"])), Image.Resampling.LANCZOS)
            box = (x, y, x + int(qr_code.width), y + int(qr_code.height))
            image.paste(qr_code, box)
            base, ext = os.path.splitext(image_path)
            new_img_path = f"{base}-wqr{ext}"
            image.save(new_img_path)
            return new_img_path
        else:
            return image_path
        
    def upload_photo(self, image_path:str, name: str, drive_id: str, retries: int = 3):
        try:
            self.service = self.authenticator.get_service_var()
            file_name = f'{name}-{os.path.basename(image_path)}'
            file_metadata = {"name": file_name, "parents": [drive_id]}

            # Upload the file
            file = self.service.files().create(
                body=file_metadata,
                media_body=image_path,
                fields="id"  # Only requesting the file ID in response
            ).execute()

            file_id = file.get('id')

            # Set the permissions to make it shareable
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            self.service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()

            # Generate the direct link to the file
            file_link = f"https://drive.google.com/uc?id={file_id}&export=download"
             
            return file_link            

        except (google.auth.exceptions.GoogleAuthError, HttpError, FileNotFoundError) as e:
            if retries > 0:
                print(f"Error occurred: {e}. Retrying... ({retries} retries left)")
                 
                return self.upload_photo(image_path, name, drive_id, retries - 1)
            else:
                 
                err = f"Operation failed after multiple retries: {e}"
                self.errorSig.emit(err)

        except Exception as e:
            err = f"An unexpected error occurred: {e}"
            self.errorSig.emit(err)
