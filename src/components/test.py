from PySide6.QtWidgets import QApplication, QListWidget, QPushButton, QVBoxLayout, QWidget, QListWidgetItem

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.list_widget = QListWidget()
        self.button = QPushButton("Add Item")
        self.button.clicked.connect(self.add_item)
        
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def add_item(self):
        item_text = f"Item {self.list_widget.count() + 1}"
        new_item = QListWidgetItem(item_text)  # Create the item without a parent
        self.list_widget.insertItem(0, new_item)  # Insert at the top

app = QApplication([])
window = MyWindow()
window.show()
app.exec()
