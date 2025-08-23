from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from PySide6.QtCore import QObject
import os

class Authenticator(QObject):
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

    def browser_login(self):
            creds = None
            # Load token if it exists
            if os.path.exists(self.TOKEN_FILE):
                creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)

            # If no creds or creds invalid, log in again
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())  # Auto refresh
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.CREDENTIALS_FILE, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)

                # Save token to file
                with open(self.TOKEN_FILE, "w") as token:
                    token.write(creds.to_json())

            self.service = build("drive", "v3", credentials=creds)
    
    def get_service_var(self):
        return self.service