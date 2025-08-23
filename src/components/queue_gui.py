import os, faulthandler, time

from icecream import ic
from PySide6 import Shiboken
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QFont, QIcon, QMovie, QPixmap
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QListWidget,
                               QListWidgetItem, QPushButton, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QWidget)

from components.queue_worker import QueueWorker, QueueHistory
from components.queue_item_widget import QueueItemWidget


class Queue(QWidget):
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
        
        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # queue label
        label = QLabel("Queue")
        label.setFont(QFont("Poppins", 16, QFont.Weight.DemiBold))

        # queue list
        self.list = QListWidget()      
        self.list.setStyleSheet("background-color: transparent")
        self.list.setSpacing(3)

        # instantiate on the ui
        layout.addWidget(label)
        layout.addWidget(self.list)

        self.queue_worker = QueueWorker()
        self.queue_worker.work_added.connect(self.add_to_list, Qt.QueuedConnection)
        self.queue_worker.progress.connect(self.update_progress_to_specific_queue_num, Qt.QueuedConnection)
        self.queue_worker.notify_current_work_number.connect(self._update_work_number)
        self.queue_worker.current_args.connect(self.setCurrentArgs)

        self.queue_history = QueueHistory()

        self.current_args = {}

    def _update_work_number(self, num:int):
        self.current_work_number = num    


    def add_to_list(self, item_data: list):
        list_item = QListWidgetItem()
        item_widget = QueueItemWidget(item_data[0], item_data[1])
        list_item.setData(Qt.UserRole, item_data[1])
        list_item.setSizeHint(item_widget.sizeHint())
        self.list.addItem(list_item)
        self.list.setItemWidget(list_item, item_widget)

    def find_item_by_value(self, value):
        for index in range(self.list.count()):
            list_item = self.list.item(index)
            if list_item is None:
                continue

            data = list_item.data(Qt.UserRole)
            if data == value:
                return list_item
        return None
    
    def update_progress_to_specific_queue_num(self, progress:str):
        # print(f'{progress}: {self.current_work_number} - {time.strftime('%-M:%-S.%f')}')
        current_queue_item = self.find_item_by_value(self.current_work_number)
        current_queue_item_widget = self.list.itemWidget(current_queue_item)
        if current_queue_item_widget is None:
            # ic('current_queue_item_widget is none')
            current_queue_item_widget.updateIcons(progress)

    def destroy_queue_item_and_retry_operations(self, work_number: int):
        # first, add the job back into the queue using the same args
        list_item_to_destroy = self.find_item_by_value(work_number)

        args = self.queue_history.find_item_from_specific_queue_num(work_number)
        self.queue_worker.addWork(args) # add the job back

        # destroy the widget
        list_item_to_destroy = self.find_item_by_value(work_number)
        if list_item_to_destroy:
            row = self.list.row(list_item_to_destroy)
            removed_item = self.list.takeItem(row)
            
            widget_to_delete = self.list.itemWidget(removed_item)
            if widget_to_delete:
                self.list.removeItemWidget(removed_item)
                widget_to_delete.deleteLater()
                widget_to_delete = None

    def setCurrentArgs(self, args: dict):
        self.current_args = args