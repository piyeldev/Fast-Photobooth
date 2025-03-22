from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QPainter, QImage
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.printer = QPrinter()
        self.button = QPushButton("Print", self)
        self.button.clicked.connect(self.open_print_dialog)
        self.setCentralWidget(self.button)

    def open_print_dialog(self):
        image = QImage("/home/fieled/Projects/PhotoBoothAutomation/src/out/framed/photo_27-framed-250124-130708.png")
        self.dialog = QPrintDialog(self.printer, self)
        if self.dialog.exec() == QPrintDialog.Accepted:
            self.handle_print()
            painter = QPainter()
            if not painter.begin(self.printer):
                print("Error: Failed to begin painting on the printer.")
                return

            # Calculate the scaling to fit the image within the printable area
            rect = painter.viewport()
            size = image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(image.rect())

            # Draw the image on the printer's painter
            painter.drawImage(0, 0, image)
            painter.end()
            print("Printing completed successfully.")
        else:
            print("Printing was canceled by the user.")

    def handle_print(self):
        # Retrieve selected print settings
        printer = self.dialog.printer()
        printer_name = printer.printerName()
        paper_size = printer.pageLayout()
        resolution = printer.resolution()
        color_mode = printer.colorMode()  # 0 = GrayScale, 1 = Color

        # Print settings for debugging
        print(f"Printer: {printer_name}")
        print(f"Paper Size: {paper_size}")
        print(f"Resolution: {resolution} DPI")
        print(f"Color Mode: {'Color' if color_mode else 'Grayscale'}")

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
