from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


from PySide6.QtCore import QObject, Signal
import os
from components.resource_path_helper import resource_path
from root_path import BASE_PATH

class Authenticator(QObject):
    _instance = None
    is_sucessful = Signal(bool)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, "initialized") and self.initialized:
            return
        super().__init__()
        self.initialized = True
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive', 
            "openid", 
            "https://www.googleapis.com/auth/userinfo.email", 
            "https://www.googleapis.com/auth/userinfo.profile"]
        self.CREDENTIALS_FILE = resource_path("assets/creds/credentials.json")
        self.TOKEN_FILE = f"{BASE_PATH}/token.json"

        self.service = None

    def token_file_exists(self):
        return os.path.exists(self.TOKEN_FILE)
    def browser_login(self):
            creds = None
            # Load token if it exists
            if self.token_file_exists():
                creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)

            # If no creds or creds invalid, log in again
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())  # Auto refresh
                else:
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.CREDENTIALS_FILE, self.SCOPES
                        )
                        creds = flow.run_local_server(port=0)
                    except Exception as e:
                        print("OAuth Error:", e)
                        return

                # Save token to file
                with open(self.TOKEN_FILE, "w") as token:
                    token.write(creds.to_json())

            self.service = build("drive", "v3", credentials=creds)
            self.is_sucessful.emit(True)

    
    def get_service_var(self):
        return self.service
    
    def get_email_address(self):
        oauth2_service = build("oauth2", "v2", credentials=self.service._http.credentials)
        user_info = oauth2_service.userinfo().get().execute()
        return user_info["email"]