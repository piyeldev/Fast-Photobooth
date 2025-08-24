from PySide6.QtWidgets import (QWidget,
                                QHBoxLayout, 
                                QPushButton, 
                                QLabel,
                                QSizePolicy)
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import QSize, Qt, Signal
from icecream import ic

from components.worker import WorkerThread
from components.resource_path_helper import resource_path

class QueueItemWidget(QWidget):

    def __init__(self, label:str, work_num):
        super().__init__()
        

        # initialize variables ============
        layout = QHBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)
        # self.setBaseSize(QSize(10, 75))

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.label_widget = QLabel(label)
        icons_widget = QWidget()
        icons_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.icons_widget_layout = QHBoxLayout()
        icons_widget.setLayout(self.icons_widget_layout)

        self.worker_thread = WorkerThread.getInstance()
        
        self.close_btn = QPushButton("×")
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.close_btn.setStyleSheet("color: red;")
        self.close_btn.setFlat(True)
        self.close_btn.clicked.connect(self.cancel_operation)

        layout.addWidget(self.label_widget)
        layout.addWidget(icons_widget)
        layout.addWidget(self.close_btn)

        self._initIcons()

        self.work_number = work_num

    def _initIcons(self):
        drive_icon = QPixmap(resource_path("assets/icons/google_drive.png"))
        self.drive_icon_placeholder_label = QLabel()
        self.drive_icon_placeholder_label.setPixmap(drive_icon)
        self.drive_icon_placeholder_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        printing_icon = QPixmap(resource_path("assets/icons/printer.png"))
        self.printing_icon_placeholder_label = QLabel()
        self.printing_icon_placeholder_label.setPixmap(printing_icon)
        self.printing_icon_placeholder_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        loading_gif = QMovie(resource_path("assets/icons/loading.gif"))
        loading_gif.setScaledSize(QSize(25, 25))
        loading_gif.start()
        self.loading_gif_placeholder_label = QLabel()
        self.loading_gif_placeholder_label.setMovie(loading_gif)
        self.loading_gif_placeholder_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        finished_icon = QPixmap(resource_path("assets/icons/ep_finished.png"))
        self.finished_icon_placeholder_label = QLabel()
        self.finished_icon_placeholder_label.setPixmap(finished_icon)
        self.finished_icon_placeholder_label.setFixedSize(QSize(25, 25))
        self.finished_icon_placeholder_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        error_icon = QPixmap(resource_path("assets/icons/material-symbols_error.png"))
        self.error_icon_placeholder_label = QLabel()
        self.error_icon_placeholder_label.setPixmap(error_icon)
        self.error_icon_placeholder_label.setFixedSize(QSize(25, 25))
        self.error_icon_placeholder_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        retry_icon = QPixmap(resource_path("assets/icons/stash_arrow-retry.png"))
        self.retry_btn = QPushButton(icon=retry_icon)
        self.retry_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.retry_btn.setFlat(True)
        self.retry_btn.setFixedSize(QSize(25, 25))
        self.retry_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.retry_btn.clicked.connect(self.retry_operation)

        self.icons_widget_layout.addWidget(self.loading_gif_placeholder_label)
        self.icons_widget_layout.addWidget(self.drive_icon_placeholder_label)
        self.icons_widget_layout.addWidget(self.printing_icon_placeholder_label)
        self.icons_widget_layout.addWidget(self.finished_icon_placeholder_label)
        self.icons_widget_layout.addWidget(self.error_icon_placeholder_label)
        self.icons_widget_layout.addWidget(self.retry_btn)

        self.loading_gif_placeholder_label.hide()
        self.drive_icon_placeholder_label.hide()
        self.printing_icon_placeholder_label.hide()
        self.finished_icon_placeholder_label.hide()
        self.error_icon_placeholder_label.hide()
        self.retry_btn.hide()




    def updateIcons(self, progress:str):
        if progress == "Uploading":
            print(f'uploading: {self.work_number}')
            self.loading_gif_placeholder_label.show()
            self.drive_icon_placeholder_label.show()

            self.error_icon_placeholder_label.hide()
            self.printing_icon_placeholder_label.hide()
            self.finished_icon_placeholder_label.hide()
            self.retry_btn.hide()

            self.printing_icon_placeholder_label.hide()
            self.finished_icon_placeholder_label.hide()

            self.close_btn.setDisabled(True)
            self.close_btn.setStyleSheet("color: white")

        elif "failed" in progress.lower() or "error" in progress.lower():
            print(f'failed: {self.work_number}')
            self.loading_gif_placeholder_label.hide()
            self.error_icon_placeholder_label.show()
            self.retry_btn.show()

        elif "canceled" in progress.lower():
            if not "canceled" in self.label_widget.text().lower():
                self.label_widget.setText(self.label_widget.text() + " - CANCELED")

            self.label_widget.setStyleSheet("color: rgba(255, 255, 255, 255)")
            self.loading_gif_placeholder_label.hide()

        else:
            print(f'finished: {self.work_number}')
            self.loading_gif_placeholder_label.hide()
            self.printing_icon_placeholder_label.show()
            self.finished_icon_placeholder_label.show()

            self.retry_btn.show()

            self.close_btn.setDisabled(True)
            self.close_btn.setStyleSheet("color: white")
    

    def retry_operation(self):
        from components.queue_gui import Queue
        queue = Queue()
        queue.destroy_queue_item_and_retry_operations(self.work_number)

    def cancel_operation(self):
        self.worker_thread.cancelWork(self.work_number)
        self.close_btn.setDisabled(True)
        self.close_btn.setStyleSheet("color: white")

        self.label_widget.setText(self.label_widget.text() + " - CANCELED")

        self.label_widget.setStyleSheet("color: rgba(255, 255, 255, 175)")
        
        


