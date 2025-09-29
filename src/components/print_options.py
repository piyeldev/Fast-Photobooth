from icecream import ic
from PySide6.QtCore import QSizeF, Qt
from PySide6.QtGui import (QDoubleValidator, QFont, QIcon, QPageLayout,
                           QPageSize, QPixmap)
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFormLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QSizePolicy,
                               QVBoxLayout, QWidget, QMessageBox)

from components.acquire_name import NameForm
from components.frame import FramePresets
from components.printer import Printer
from components.queue_worker import QueueWorker
from components.upload_online import OnlineUploader
from components.worker import WorkerThread
from components.resource_path_helper import resource_path
from components.authenticator import Authenticator

import os

class PrintOptions(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 6, 0, 0)

        # heading of section
        label = QLabel("Print Options")
        self.font = QFont("Poppins", 16, QFont.Weight.DemiBold)
        label.setFont(self.font)

        # process and print btn
        process_btn = QPushButton("Process")
        process_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        process_btn.setStyleSheet("background-color: #1fb141; border-radius: 0.5em; padding: 6px 12px; color: white")
        process_btn.setFont(QFont("Poppins", 14, QFont.Weight.Medium))
        process_btn_pxmp = QPixmap(resource_path("assets/icons/print_icon.png"))
        process_btn_icon = QIcon(process_btn_pxmp)
        process_btn.setIcon(process_btn_icon)
        process_btn.setIconSize(process_btn_pxmp.rect().size())
        process_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        process_btn.clicked.connect(self.process_to_queue_worker)
        
        # variables for other widgets
        self.frame_presets = FramePresets()
        self.frame_presets.frame_preset_added.connect(lambda: process_btn.setDisabled(False))
        self.frame_presets.frame_preset_deleted.connect(lambda: {
            process_btn.setDisabled(True) if len(self.frame_presets.getPresets()) == 0 else process_btn.setDisabled(False)
        })

        self.queue_worker = QueueWorker()
        self.online_uploader = OnlineUploader()
        self.name_form = NameForm()
        self.printer = Printer()
        self.frame_presets = FramePresets()
        self.authenticator = Authenticator()

        # the function for options gui
        self.options()

        # instantiate the widgets in the layout
        layout.addWidget(label)
        layout.addWidget(self.options_widget)
        layout.addWidget(process_btn)

        # check if frame presets are empty, then deactivate the process button if so
        frames = self.frame_presets.getPresets()
        if len(frames) > 0:
            pass
        else:
            process_btn.setDisabled(True)


    def validate(self, path: str, sizeH: float, sizeW: float, drive_link: str):
        vars = {'Framed Image': path, 'Height': sizeH, 'Width': sizeW}
        invalidItems = []

        for varName, varValue in vars.items():
            if not varValue or varValue == "":
                invalidItems.append(varName)
        
        if self.online_uploader.getIsUploadState():
            logged_in = bool(self.authenticator.get_service_var())
            if not logged_in:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Not Signed in")
                msg_box.setText("Please sign in to google first.")
                msg_box.exec()
                return False
            else:
                if drive_link:
                    return True
                else:
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setWindowTitle("Empty Fields Error")
                    msg_box.setText("Please put a drive link first. This will be used as the upload destination.")
                    msg_box.exec()
                    return False
            
        if len(invalidItems) > 0:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Empty Fields Error")
            msg_box.setText(f"The following are empty or invalid: {', '.join(invalidItems)}. Please set before proceeding.")
            msg_box.exec()
            return False
        else:
            
            return True
        
        

    def process_to_queue_worker(self):
        path = self.frame_presets.getCurrentOverlayedImage()
        printer_name = self.printer_options.currentText()
        orientation = self.orientation_options.currentText()
        isUploadOnline = self.online_uploader.getIsUploadState()
        name = self.name_form.get_text()
        current_frame_index = self.frame_presets.getCurrentIndex()
        current_frame_name = self.frame_presets.getPresets()[current_frame_index]["name"]
        printer_instance = QPrinter(QPrinter.HighResolution)
        print_to_pdf = False
        pageHeight = self.height_custom.text()
        pageWidth = self.width_custom.text()
        drive_link = self.online_uploader.get_drive_folder_id()

        valid = self.validate(path, pageHeight, pageWidth, drive_link)

        if not valid:
            return
            
        # print to pdf switch
        if printer_name == "Print to PDF":
            print_to_pdf = True
            printer_instance.setPrinterName("")
        else:
            if printer_name:
                printer_instance.setPrinterName(printer_name)
            else:
                printer_instance.setPrinterName("")

        
        printer_instance.setPageOrientation(getattr(QPageLayout, orientation, None))
        base, ext = os.path.splitext(os.path.basename(path))
        docName = f'{name}-{base}'
        printer_instance.setDocName(docName)
        
        custom_size = QSizeF(float(pageWidth), float(pageHeight))
        page_size = QPageSize(custom_size, QPageSize.Unit.Inch, "CustomSize")
        printer_instance.setPageSize(page_size)
        

        if path:
            self.queue_worker.addWork({
                "path_to_img": path, 
                "printer_instance": printer_instance, 
                "isUploadOnline": isUploadOnline, 
                "name": name if name else "No Name", 
                "size_str": f'{custom_size.width()}x{custom_size.height()}',
                "frame_name": current_frame_name,
                "print_to_pdf": print_to_pdf,
                "drive_link": drive_link
                })
        else:
            QMessageBox(
                QMessageBox.Warning,
                "No Framed Image",
                "There is currently no framed image. Please proceed to create one first.",
                QMessageBox.Ok
            ).exec()



    def options(self):
        self.options_widget = QWidget()
        layout = QFormLayout()
        layout.setContentsMargins(6, 0, 0, 0)
        self.options_widget.setLayout(layout)

        lbl_font = QFont(self.font)
        lbl_font.setPointSize(12)

        printer_lbl = QLabel("Printer: ")
        size_lbl = QLabel("Size: ")
        orientation_lbl = QLabel("Orientation: ")

        printer_lbl.setFont(lbl_font)
        size_lbl.setFont(lbl_font)
        orientation_lbl.setFont(lbl_font)
        

        self.printer_options = QComboBox()
        self.printer_options.addItem("Print to PDF")
        self.printer_options.addItems(self.printer.getPrinterNames())
        # self.printer_options.currentIndexChanged.connect(self.switchPrinter)

        # custom size fields
        self.custom_size_label = QLabel("Size: ")
        self.custom_size_label.setFont(lbl_font)
        self.custom_size_fields = QWidget()
        self.custom_size_fields_layout = QHBoxLayout()
        self.custom_size_fields.setLayout(self.custom_size_fields_layout)
        self.custom_size_fields_layout.setContentsMargins(0,0,0,0)
        self.custom_size_fields_layout.setAlignment(Qt.AlignLeft)


        self.width_custom = QLineEdit()
        self.width_custom.setValidator(QDoubleValidator())
        self.height_custom = QLineEdit()
        self.height_custom.setValidator(QDoubleValidator())
        self.w_in_lbl = QLabel("in.")
        self.h_in_lbl = QLabel("in.")
        self.x_lbl = QLabel("x")
        self.custom_size_fields_layout.addWidget(self.width_custom)
        self.custom_size_fields_layout.addWidget(self.w_in_lbl)
        self.custom_size_fields_layout.addWidget(self.x_lbl)
        self.custom_size_fields_layout.addWidget(self.height_custom)
        self.custom_size_fields_layout.addWidget(self.h_in_lbl)
        

        self.orientation_options = QComboBox()
        self.orientation_options.addItems(["Portrait", "Landscape"])

        layout.addRow(printer_lbl, self.printer_options)
        layout.addRow(self.custom_size_label, self.custom_size_fields)
        layout.addRow(orientation_lbl, self.orientation_options)






    