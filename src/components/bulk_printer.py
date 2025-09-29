from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QComboBox
from PySide6.QtGui import QFont

class BulkPrinter(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        heading = QLabel("Bulk Printer")
        heading_font = QFont("Poppins", 16, QFont.Weight.DemiBold)
        heading.setFont(heading_font)

        size_chooser = QWidget()
        size_chooser_layout = QFormLayout()
        size_chooser.setLayout(size_chooser_layout)
        size_chooser_lbl = QLabel("Paper Size")
        size_chooser_combo_box = QComboBox()
        size_chooser_combo_box.addItems(['A4', 'Short', 'Long'])
        size_chooser_layout.addRow(size_chooser_lbl, size_chooser_combo_box)

        
        layout.addWidget(heading)
        layout.addWidget(size_chooser)