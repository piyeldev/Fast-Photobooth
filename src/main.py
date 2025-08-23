import os, sys, sysconfig

# PySide6 installation dir to DLL search paths
d = sysconfig.get_path("purelib")  # e.g. C:\...\Lib\site‑packages
os.add_dll_directory(os.path.join(d, "PySide6"))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import qInstallMessageHandler, QtMsgType, QLoggingCategory
import traceback
from windows.main_window import MainWindow
from PySide6.QtGui import QPalette, QColor, QFont, QFontDatabase
from components.queue_worker import QueueWorker

def message_handler(msg_type, context, message):
    if "Corrupt JPEG data" in message:
        return  # ignore these warnings
    # otherwise fallback to default handling
    print(message)

def set_dark_mode(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(42, 42, 42))
    palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)

def load_fonts():
        poppins_dir = '../assets/fonts/Poppins' # use when running from main.py, not vscode debugger
        # poppins_dir = f'{os.getcwd()}/assets/fonts/Poppins'
        poppins_font_files = os.listdir(poppins_dir)

        for font_file in poppins_font_files:
            font_id = QFontDatabase.addApplicationFont(f'{poppins_dir}/{font_file}')
            if font_id == -1:
                raise FileNotFoundError(f"err: font failed to load {font_file}:{font_id}")

def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Custom exception handler to display errors in a QMessageBox.
    """
    # format exception details
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f'Unhandled Exception: \n{error_message}')

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("Application Error")
    msg_box.setText("An unexpected error occured.")
    msg_box.setDetailedText(error_message)
    msg_box.exec()

sys.excepthook = handle_exception

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # set font
    load_fonts()
    app_font = QFont("Poppins")
    app.setFont(app_font)

    window = MainWindow()
    window.showMaximized()

    qInstallMessageHandler(message_handler)
    queue_worker = QueueWorker()
    app.aboutToQuit.connect(queue_worker.stop_worker)
    app.exec()