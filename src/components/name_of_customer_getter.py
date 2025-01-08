from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit
from PySide6.QtGui import QFont

class NameForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout(self)
        self.setLayout(layout)

        form_label = QLabel("Name of Customer: ")
        form_label.setFont(QFont("Poppins", 12, QFont.Weight.DemiBold))
        text_field = QLineEdit()
        text_field.setPlaceholderText("Enter here...")
        text_field.setStyleSheet("border-radius: 0.6em; padding: 4px;")
        layout.addRow(form_label, text_field)