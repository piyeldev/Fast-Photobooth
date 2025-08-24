from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPixmap, QWheelEvent
from PySide6.QtCore import Qt
from components.resource_path_helper import resource_path

class PixmapViewer(QGraphicsView):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, pixmap = None):
        if hasattr(self, "initialized") and self.initialized:
            return
        
        super().__init__()
        self.initialized = True

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Add the pixmap to the scene
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        # Enable scaling
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        if not pixmap:
            self.setPixmapToView(QPixmap(resource_path("assets/imgs/Rectangle.png")))
        else:
            self.setPixmapToView(pixmap)

        self.zoom_factor = 1.05

    def setPixmapToView(self, pixmap:QPixmap):
        # print(pixmap.size())
        self.pixmap_item.setPixmap(pixmap)
        self.fitInView(self.pixmap_item, aspectRadioMode=Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        # Automatically scale the pixmap to fit the view
        self.fitInView(self.pixmap_item, aspectRadioMode=Qt.KeepAspectRatio)
        super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        """Handle zooming with the mouse wheel."""
        if event.angleDelta().y() > 0:  # Zoom in
            self.scale(self.zoom_factor, self.zoom_factor)
        else:  # Zoom out
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)
