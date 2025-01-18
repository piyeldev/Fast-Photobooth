from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QSize  
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QListView,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QStyledItemDelegate,
    QStyleOptionViewItem,
)

class CustomPixmapModel(QAbstractListModel):
    def __init__(self, pixmaps = None):
        super().__init__()
        self.pixmaps = pixmaps if pixmaps else []

    def rowCount(self, parent=QModelIndex):
        return len(self.pixmaps)
    
    def data(self, index, role):
        if role == Qt.DecorationRole and index.isValid():
            return self.pixmaps[index.row()]

    def addPixmap(self, pixmap):
        self.beginInsertRows(QModelIndex(), len(self.pixmaps), len(self.pixmaps))
        self.pixmaps.append(pixmap)
        self.endInsertRows()

    def removePixmap(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self.pixmaps.pop(row)
        self.endRemoveRows()


class PixmapDelegate(QStyledItemDelegate):
    def paint(self, painter, option: QStyleOptionViewItem, index: QModelIndex):
        # Custom rendering for the pixmap
        painter.save()
        pixmap = index.data(Qt.DecorationRole)
        if pixmap:
            # Draw the pixmap centered in the item's rectangle
            pixmap_rect = pixmap.rect()
            pixmap_rect.moveCenter(option.rect.center())
            painter.drawPixmap(pixmap_rect, pixmap)
        painter.restore()

    def sizeHint(self, option, index):
        # Set a custom size for each item
        return QSize(100, 100)