from PySide6.QtCore import QObject
from PySide6.QtPrintSupport import QPrinterInfo

class Printer(QObject):
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

        self._printers = QPrinterInfo.availablePrinters()

    def count(self):
        return len(self._printers)
    
    def getSupportedPageSizes(self, index):
        supported_page_sizes = self._printers[index].supportedPageSizes()
        sizes = []
        for size in supported_page_sizes:
            sizes.append(size.key())
        return sizes
    
    def getPrinterNames(self):
        names = []
        for printer in self._printers:
            names.append(printer.printerName())
        
        return names
    
