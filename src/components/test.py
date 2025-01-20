import sys
from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
)
from PySide6.QtGui import QPixmap, QMouseEvent, QPen, QColor
from PySide6.QtCore import QRectF, QPointF, Qt


class ImageRectDrawer(QGraphicsView):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

        # Set up the scene and image
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        pixmap = QPixmap(self.image_path)
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.setFixedSize(pixmap.size())
        self.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.scene.addItem(self.pixmap_item)

        # For rectangle drawing
        self.start_point = None
        self.current_rect_item = None

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # Start drawing the rectangle
            self.start_point = self.mapToScene(event.pos())
            self.current_rect_item = QGraphicsRectItem()
            self.current_rect_item.setPen(QPen(QColor("red")))
            self.scene.addItem(self.current_rect_item)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.start_point and self.current_rect_item:
            # Update the rectangle size as the mouse moves
            current_point = self.mapToScene(event.pos())
            rect = QRectF(self.start_point, current_point).normalized()
            self.current_rect_item.setRect(rect)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.start_point and self.current_rect_item:
            # Finalize the rectangle and print its coordinates relative to the image
            rect = self.current_rect_item.rect()
            image_rect = self.pixmap_item.mapFromScene(rect).boundingRect()
            info = {"count": "1", "height": f"{image_rect.size().height()}", "width": f"{image_rect.size().width()}", "x": f"{image_rect.x()}", "y": f"{image_rect.y()}"}

            print(info)
            print(f"Rectangle coordinates relative to the image: {image_rect}")
            self.start_point = None
            self.current_rect_item = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageRectDrawer("/home/fieled/Pictures/book-month-pc.png")
    viewer.show()
    sys.exit(app.exec())
