import os, sys, sysconfig
from components.resource_path_helper import resource_path

if os.name == 'nt':
    # PySide6 installation dir to DLL search paths
    if not getattr(sys, 'frozen', False):
        # Running in normal Python

        d = sysconfig.get_path("purelib")
        pyside_path = os.path.join(d, "PySide6")
        if os.path.exists(pyside_path):
            os.add_dll_directory(pyside_path)
    else:
        # Running inside a PyInstaller bundle
        # PyInstaller already handles DLL paths
        pass


from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import qInstallMessageHandler
import traceback
from windows.main_window import MainWindow
from PySide6.QtGui import QPalette, QColor, QFont, QFontDatabase
from components.queue_worker import QueueWorker
from components.resource_path_helper import resource_path

def message_handler(msg_type, context, message):
    if "Corrupt JPEG data" in message:
        return  # ignore these warnings
    # otherwise fallback to default handling
    print(message)

def load_fonts():
        poppins_dir = resource_path('assets/fonts/Poppins')
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