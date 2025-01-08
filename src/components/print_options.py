from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QComboBox, QPushButton, QSizePolicy
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt 

class PrintOptions(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 6, 0, 0)


        label = QLabel("Print Options")
        self.font = QFont("Poppins", 16, QFont.Weight.DemiBold)
        label.setFont(self.font)

        self.options()

        process_btn = QPushButton(" Process and Print")
        process_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        process_btn.setStyleSheet("background-color: #1fb141; border-radius: 0.5em; padding: 6px 12px")
        process_btn.setFont(QFont("Poppins", 14, QFont.Weight.Medium))
        process_btn_pxmp = QPixmap("../assets/icons/print_icon.png")
        process_btn_icon = QIcon(process_btn_pxmp)
        process_btn.setIcon(process_btn_icon)
        process_btn.setIconSize(process_btn_pxmp.rect().size())

        process_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(label)
        layout.addWidget(self.options_widget)
        layout.addWidget(process_btn)

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
        

        printer_options = QComboBox()
        size_options = QComboBox()
        orientation_options = QComboBox()

        layout.addRow(printer_lbl, printer_options)
        layout.addRow(size_lbl, size_options)
        layout.addRow(orientation_lbl, orientation_options)




