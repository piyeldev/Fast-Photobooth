from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

class NameForm(QWidget):
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
        layout = QFormLayout(self)
        self.setLayout(layout)

        form_label = QLabel("Name of Customer: ")
        form_label.setFont(QFont("Poppins", 12, QFont.Weight.DemiBold))
        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText("Enter here...")
        self.text_field.setStyleSheet("border-radius: 0.6em; padding: 4px;")
        layout.addRow(form_label, self.text_field)
    
    def get_text(self):
        return self.text_field.text()
