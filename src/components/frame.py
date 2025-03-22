from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, QObject

# Singleton
class FramePresets(QObject):
    frame_preset_added = Signal(dict)
    frame_preset_deleted = Signal(int)
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

        self._presets = []
        self._current_index = 0

        self._current_image_overlayed_path = None

    def getPresets(self):
        return self._presets
    
    def setCurrentActivePreset(self, index):
        self._current_index = index
    
    def getCurrentIndex(self):
        return self._current_index;
    
    def deletePreset(self, index):
        self._presets.pop(index)
        self.frame_preset_deleted.emit(index)

    def createPreset(self, name:str):
        preset = {"name": name, "frame_path": "Add Frame...", "placeholders": [], "qr_code_placeholder": None}
        self._presets.append(preset)
        self.frame_preset_added.emit(preset)

    def addFrameToPreset(self, index:int, file_path:str):
        self._presets[index]["frame_path"] = file_path

    def addPlaceholderToPreset(self, index:int, placeholder:dict):
        self._presets[index]["placeholders"].append(placeholder)
    
    def setCurrentOverlayedImage(self, path:str):
        self._current_image_overlayed_path = path

    def getCurrentOverlayedImage(self):
        return self._current_image_overlayed_path 

    def setQrCodePlaceholder(self, index:int, placeholder:dict):
        self._presets[index]["qr_code_placeholder"] = placeholder
