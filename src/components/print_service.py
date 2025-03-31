from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtCore import QObject, Qt, QFile, QIODevice, QDir
from PySide6.QtPdf import QPdfDocument, QPdfPageRenderer
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QImage, QPainter, QPageSize, QPageLayout
import subprocess
from icecream import ic
from pathlib import Path

class PrintService(QObject):
    def set_photo_paper_type(self, printer_name:str, set:bool):
        # Current Implementation: CUPS (Linux and MacOS)
        if set == True:
            subprocess.call(["lpoptions", "-p", printer_name, "-o", "MediaType=Glossy"])
        else:
            subprocess.call(["lpoptions", "-p", printer_name, "-o", "MediaType=Plain"])


    def call(self, image_path:str, printer_instance:QPrinter):
        ic()
        image = QImage(image_path)
        printer = printer_instance

        self.set_photo_paper_type(printer.printerName(), True)
        
        # for debugging
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(f"{Path.home()}Downloads/output.pdf")

        # proceed to printing
        painter = QPainter()
        if not painter.begin(printer):
            print("Error: Failed to begin painting on the printer.")
            return

        # Calculate the scaling to fit the image within the printable area
        rect = painter.viewport()
        size = image.size()
        size.scale(rect.size(), Qt.KeepAspectRatio)
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        painter.setWindow(image.rect())

        self.set_photo_paper_type(printer.printerName(), False)

        # Draw the image on the printer's painter
        painter.drawImage(0, 0, image)
        painter.end()
        print("Printing completed successfully.")
    
        
        



