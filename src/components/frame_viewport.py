from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QMouseEvent, QPen, QColor, QWheelEvent
from PySide6.QtCore import QRectF, Qt, Signal

class FrameViewport(QGraphicsView):
    placeholder_added = Signal(dict)

    def __init__(self, img_path=None):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.start_point = None
        self.current_rect_item = None

        if img_path:
            self.set_pixmap(img_path)
        self.rectangles = []

        self.zoom_factor = 1.05
    
    def set_pixmap(self, img_path:str):
        if img_path and img_path != "":
            self.pixmap = QPixmap(img_path)
        else:
            self.pixmap = QPixmap("../assets/imgs/Rectangle.png")
        self.pixmap_item.setPixmap(self.pixmap)
        self.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        self.fitInView(self.pixmap_item, aspectRadioMode=Qt.KeepAspectRatio)

    def setPlaceholderList(self, placeholders:list):
        # clear the scene of placeholders
        for placeholder_item in self.rectangles:
            self.scene.removeItem(placeholder_item)

        scale_factor_x = self.scene.width() / self.pixmap.width()
        scale_factor_y = self.scene.height() / self.pixmap.height()

        self.rectangles.clear()
        self.resetTransform()

        # go through all placeholders in the list
        for placeholder in placeholders:
            adjusted_rect = QRectF(
                placeholder["x"] * scale_factor_x, 
                placeholder["y"] * scale_factor_y, 
                placeholder["width"] * scale_factor_x, 
                placeholder["height"] *scale_factor_y
                )
            print(f'after: real values: {placeholder} adjusted values: {adjusted_rect}')
            self.rectangles.append(QGraphicsRectItem(adjusted_rect))

        # and add them to the scene
        for placeholder in self.rectangles:
            self.scene.addItem(placeholder)


    def wheelEvent(self, event: QWheelEvent):
        """Handle zooming with the mouse wheel."""
        if event.angleDelta().y() > 0:  # Zoom in
            self.scale(self.zoom_factor, self.zoom_factor)
        else:  # Zoom out
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)

    def mousePressEvent(self, event: QMouseEvent):
        scene_pos = self.mapToScene(event.pos())
        if event.button() == Qt.LeftButton:
            self.start_point = self.mapToScene(event.pos())

            self.start_point.setX(max(0, min(self.start_point.x(), self.pixmap.width())))
            self.start_point.setY(max(0, min(self.start_point.y(), self.pixmap.height())))

            self.current_rect_item = QGraphicsRectItem()
            self.current_rect_item.setPen(QPen(QColor("red")))
            self.scene.addItem(self.current_rect_item)

        elif event.button() == Qt.RightButton:
            # Check if a rectangle was clicked, and remove it if so
            for rect_item in self.rectangles:
                if rect_item.rect().contains(scene_pos):
                    self.scene.removeItem(rect_item)
                    self.rectangles.remove(rect_item)
                    break

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.start_point and self.current_rect_item:
            # Update the rectangle size as the mouse moves, ensuring it stays inside the image bounds
            current_point = self.mapToScene(event.pos())
            current_point.setX(max(0, min(current_point.x(), self.pixmap.width())))
            current_point.setY(max(0, min(current_point.y(), self.pixmap.height())))

            rect = QRectF(self.start_point, current_point).normalized()
            self.current_rect_item.setRect(rect)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.start_point and self.current_rect_item:
            # Finalize the rectangle and print its coordinates relative to the image
            rect = self.current_rect_item.rect()

            # Calculate the scaling factor (image's real resolution to view's resolution)
            scale_x = self.pixmap.width() / self.scene.width()
            scale_y = self.pixmap.height() / self.scene.height()

            # Apply linear interpolation to scale the rectangle coordinates and dimensions
            scaled_rect = QRectF(
                rect.x() * scale_x, 
                rect.y() * scale_y,
                rect.width() * scale_x,
                rect.height() * scale_y
            )

            self.rectangles.append(self.current_rect_item)
            placeholder_dict = {
                "count": str(len(self.rectangles)), 
                "x": scaled_rect.x(), 
                "y": scaled_rect.y(), 
                "width": scaled_rect.width(), 
                "height": scaled_rect.height()
                }
            print(f"before: Rectangle coordinates relative to the image (real resolution): {placeholder_dict}")
            self.placeholder_added.emit(placeholder_dict)
            self.start_point = None
            self.current_rect_item = None
