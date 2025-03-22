from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import google.auth.exceptions
import os

from PySide6.QtCore import QObject, Signal
from PIL import Image
from components.frame import FramePresets

import qrcode


class UploadWorker(QObject):
    output = Signal(str)
    
    def __init__(self):
        super().__init__()

        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.SERVICE_ACCOUNT_FILE = 'creds/service_account.json'
        self.PARENT_FOLDER_ID = "1htmtVcGUaz1asid-ABB52arrVDWPRkXa"

        self.frame_presets = FramePresets()

    def authenticate(self):
        creds = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        return creds
    
    def upload_and_overlay(self, img_path:str):
        current_index = self.frame_presets.getCurrentIndex()
        position = self.frame_presets.getPresets()[current_index]["qr_code_placeholder"]

        image_path = img_path
        image = Image.open(image_path)
        file_link = self.upload_photo(image_path)
        qr_code = qrcode.make(file_link)
        qr_code = qr_code.convert(image.mode)

        x, y = int(position["x"]), int(position["y"])
        qr_code = qr_code.resize((int(position["width"]), int(position["height"])))
        box = (x, y, x + int(qr_code.width), y + int(qr_code.height))
        image.paste(qr_code, box)
        base, ext = os.path.splitext(image_path)
        new_img_path = f"{base}-wqr{ext}"
        image.save(new_img_path)

        self.output.emit(new_img_path)

    def upload_photo(self, image_path:str):
        try:
            creds = self.authenticate()
            service = build('drive', 'v3', credentials=creds)


            file_metadata = {
                'name': os.path.basename(image_path),
                'parents': [self.PARENT_FOLDER_ID]
            }

            # Upload the file
            file = service.files().create(
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
            service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()

            # Generate the direct link to the file
            file_link = f"https://drive.google.com/uc?id={file_id}&export=download"

            self.output.emit(file_link)
            return file_link
            

        except google.auth.exceptions.GoogleAuthError as auth_error:
            print("Authentication Error:", auth_error)
            self.output.emit("err")
            return "err"

        except HttpError as http_error:
            print("An error occurred with the API:", http_error)
            self.output.emit("err")
            return "err"

        except FileNotFoundError:
            print("The file was not found. Please check the file path.")
            self.output.emit("err")

            return "err"

        except Exception as e:
            print("An unexpected error occurred:", e)
            self.output.emit("err")

            return "err"
