from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QGraphicsView, QWidget, QSizePolicy
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QResizeEvent

class ExpandingGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        )

    def resizeEvent(self, event: QResizeEvent):
        # Optional: Respond to resizing if needed
        print(f"New size: {event.size()}")
        super().resizeEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create the expanding graphics view
        graphics_view = ExpandingGraphicsView()
        layout.addWidget(graphics_view)

        # Add a second widget for comparison
        another_widget = QWidget()
        another_widget.setStyleSheet("background-color: lightblue;")
        another_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        )
        layout.addWidget(another_widget)

        # Set some constraints for the main window
        self.setMinimumSize(400, 300)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
