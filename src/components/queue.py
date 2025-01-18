from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QListWidget, QSpacerItem, QPushButton, QListWidgetItem, QLabel
from PySide6.QtGui import QIcon, QFont

class Queue(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Example data
        data = [
            {"name": "bella", "frame": "photostrip", "size": "2x6in", "icon": "error.png"},
            {"name": "fiel", "frame": "photocard", "size": "4x5in", "icon": "drive.png"},
            {"name": "bella", "frame": "photostrip", "size": "2x6in", "icon": "error.png"},
            {"name": "fiel", "frame": "photocard", "size": "4x5in", "icon": "drive.png"},
            {"name": "bella", "frame": "photostrip", "size": "2x6in", "icon": "error.png"},
            {"name": "fiel", "frame": "photocard", "size": "4x5in", "icon": "drive.png"},
        ]

        label = QLabel("Queue")
        label.setFont(QFont("Poppins", 16, QFont.Weight.DemiBold))

        self.list = QListWidget()      
        self.list.setStyleSheet("background-color: transparent;")

        for item in data:
            self.add_to_list(item)

        layout.addWidget(label)
        layout.addWidget(self.list)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        # self.setStyleSheet("border: 1px solid red;")


    def add_to_list(self, item_data):
        list_item = QListWidgetItem()

        item_widget = QWidget()
        item_widget.setStyleSheet("background-color: #242424;")
        item_layout = QHBoxLayout()
        item_layout.setContentsMargins(20, 5, 0, 5)
        item_widget.setLayout(item_layout)

        label = QLabel(f"{item_data['name']} - {item_data['frame']} - {item_data['size']}")
        # spacer = QSpacerItem()
        delete_btn = QPushButton('X')
        delete_btn.setStyleSheet("background-color: transparent")
        delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        delete_btn.setFlat(True)

        item_layout.addWidget(label)
        # item_layout.addSpacerItem(spacer)
        item_layout.addWidget(delete_btn)

        list_item.setSizeHint(item_widget.sizeHint())
        list_item.setSizeHint(item_widget.sizeHint())
        self.list.addItem(list_item)
        self.list.setItemWidget(list_item, item_widget)