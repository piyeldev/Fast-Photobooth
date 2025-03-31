from icecream import ic
from PySide6.QtCore import QSizeF, Qt
from PySide6.QtGui import (QDoubleValidator, QFont, QIcon, QPageLayout,
                           QPageSize, QPixmap)
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFormLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QSizePolicy,
                               QVBoxLayout, QWidget)

from components.acquire_name import NameForm
from components.frame import FramePresets
from components.printer import Printer
from components.queue_worker import QueueWorker
from components.upload_online import OnlineUploader
from components.worker import WorkerThread


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
        process_btn = QPushButton("Process and Print")
        process_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        process_btn.setStyleSheet("background-color: #1fb141; border-radius: 0.5em; padding: 6px 12px")
        process_btn.setFont(QFont("Poppins", 14, QFont.Weight.Medium))
        process_btn_pxmp = QPixmap("../assets/icons/print_icon.png")
        process_btn_icon = QIcon(process_btn_pxmp)
        process_btn.setIcon(process_btn_icon)
        process_btn.setIconSize(process_btn_pxmp.rect().size())
        process_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        process_btn.clicked.connect(self.process_to_queue_worker)
        
        # variables for other widgets
        self.frame_presets = FramePresets()
        self.queue_worker = QueueWorker()
        self.online_uploader = OnlineUploader()
        self.name_form = NameForm()
        self.printer = Printer()
        self.frame_presets = FramePresets()

        # the function for options gui
        self.options()

        # instantiate the widgets in the layout
        layout.addWidget(label)
        layout.addWidget(self.options_widget)
        layout.addWidget(process_btn)

    def process_to_queue_worker(self):
        path = self.frame_presets.getCurrentOverlayedImage()
        printer_name = self.printer_options.currentText()
        orientation = self.orientation_options.currentText()
        isUploadOnline = self.online_uploader.getIsUploadState()
        name = self.name_form.get_text()
        current_frame_index = self.frame_presets.getCurrentIndex()
        current_frame_name = self.frame_presets.getPresets()[current_frame_index]["name"]

        printer_instance = QPrinter(QPrinter.HighResolution)
        printer_instance.setPrinterName(printer_name)
        printer_instance.setPageOrientation(getattr(QPageLayout, orientation, None))
        
        custom_size = QSizeF(float(self.width_custom.text()), float(self.height_custom.text()))
        page_size = QPageSize(custom_size, QPageSize.Unit.Inch, "CustomSize")
        printer_instance.setPageSize(page_size)

        ic()
        self.queue_worker.addWork({
            "path_to_img": path, 
            "printer_instance": printer_instance, 
            "isUploadOnline": isUploadOnline, 
            "name": name if name else "No Name", 
            "size_str": f'{custom_size.width()}x{custom_size.height()}',
            "frame_name": current_frame_name
            })


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






    