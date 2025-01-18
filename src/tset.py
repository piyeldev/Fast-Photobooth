from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)  # Take the item at index 0
        widget = item.widget()  # Get the widget associated with the item
        if widget is not None:
            widget.deleteLater()  # Schedule the widget for deletion
        else:
            del item  # Delete non-widget items (e.g., spacers)

app = QApplication([])

window = QWidget()
layout = QVBoxLayout(window)

# Add some widgets to the layout
for i in range(5):
    layout.addWidget(QPushButton(f"Button {i+1}"))

# Clear the layout
clear_layout(layout)

window.show()
app.exec()
