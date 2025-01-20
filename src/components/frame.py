from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, QObject

# Singleton
class Frame(QObject):
    frames_added = Signal(list)
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

        self.frame_list = []
        self._active_frame = ""

        
        if len(self.frame_list) != 0:
            self.setActiveFrame(0)

    def activeFrame(self):
        if self._active_frame == "":
            return
        else: 
            return self._active_frame
    
    def setActiveFrame(self, index):
        self._activeFrame = self.getFrames()[index]

    def addFrame(self, path:str):
        self.frame_list.append(path)
        self.frames_added.emit(self.frame_list)

    def getFrames(self):
        return self.frame_list

    def getFrame(self, index:int):
        return QPixmap(self.frame_list[index])
    

class FramePresets(QObject):
    frame_preset_added = Signal(dict)
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

    def getPresets(self):
        return self._presets
    
    def deletePreset(self, index):
        self._presets.pop(index)

    def createPreset(self, name:str):
        preset = {"name": name, "frame_path": "Add Frame...", "placeholders": []}
        self._presets.append(preset)
        self.frame_preset_added.emit(preset)

    def addFrameToPreset(self, index:int, file_path:str):
        self._presets[index]["frame_path"] = file_path

    def addPlaceholderToPreset(self, index:int, placeholder:dict):
        self._presets[index]["placeholders"].append(placeholder)