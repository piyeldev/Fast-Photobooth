from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QListWidget, QSpacerItem, QPushButton, QListWidgetItem, QLabel
from PySide6.QtGui import QIcon, QFont
from components.queue_worker import QueueWorker
from PySide6.QtCore import Qt, QTimer
import itertools

class Queue(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Queue")
        label.setFont(QFont("Poppins", 16, QFont.Weight.DemiBold))

        self.list = QListWidget()      
        self.list.setStyleSheet("background-color: transparent;")

        layout.addWidget(label)
        layout.addWidget(self.list)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        queue_worker = QueueWorker()
        queue_worker.work_added.connect(self.add_to_list)
        queue_worker.progress.connect(self.update_progress)
        self.progress = ""


    def add_to_list(self, item_data):
        list_item = QListWidgetItem()

        item_widget = QWidget()
        item_widget.setStyleSheet("background-color: #242424;")
        item_layout = QHBoxLayout()
        item_layout.setContentsMargins(20, 5, 0, 5)
        item_widget.setLayout(item_layout)

        # label = QLabel(f"{item_data['name']} - {item_data['frame']} - {item_data['size']}")
        label = QLabel(item_data)

        self.status_label = QLabel("Status")
        self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        delete_btn = QPushButton('X')
        delete_btn.setStyleSheet("background-color: transparent")
        delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        delete_btn.setFlat(True)   

        item_layout.addWidget(label)
        item_layout.addWidget(self.status_label, alignment=Qt.AlignRight)
        item_layout.addWidget(delete_btn)

        list_item.setSizeHint(item_widget.sizeHint())
        self.list.addItem(list_item)
        self.list.setItemWidget(list_item, item_widget)

        self.loop_dots()


    def update_progress(self, progress:str):
        self.progress = progress

    def loop_dots(self):
        self.dots_cycle = itertools.cycle([".", "..", "..."])
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_progress)
        self.timer.start(1000)

    def show_progress(self):
        if self.progress != "Done":
            self.status_label.setText(f'{self.progress}{next(self.dots_cycle)}')
        else: 
            self.status_label.setText(f'{self.progress}!')

