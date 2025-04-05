from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, Signal
from windows.edit_frame_window import EditFrameWindow
from components.frame import FramePresets
from components.pixmap_viewer import PixmapViewer
from components.captures_list import CapturesList
class FrameView(QWidget):
    frame_dropdown_added = Signal(bool)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.rectangle_path = "../assets/imgs/Rectangle.png"

        self.toolbar()
        self.frame()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.frame_widget, alignment=Qt.AlignTop)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.captures_list = CapturesList()




    def toolbar(self):
        self.toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        self.toolbar.setLayout(toolbar_layout)
        self.toolbar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        toolbar_layout.setContentsMargins(10,0,0,0)

        # label
        label = QLabel("Frame View")
        label.setFont(QFont("Poppins", 12, QFont.Weight.Bold))


        # edit button
        edit_btn = QPushButton("Edit Frame")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
        edit_icon_pxmp = QPixmap("../assets/icons/edit_icon.png")
        edit_icon = QIcon(edit_icon_pxmp)
        edit_btn.setIcon(edit_icon)
        edit_btn.setIconSize(edit_icon_pxmp.rect().size())
        edit_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        edit_btn.clicked.connect(self.open_edit_frame_window)

        edit_btn.setStyleSheet("background-color: #1fb141; padding: 0px 10px; width: 111px; height: 25px; border-radius: 8px;")

        self.frame_presets = FramePresets()
        self.presets_list = self.frame_presets.getPresets()
        self.frame_presets.frame_preset_added.connect(self.getPresets)
        self.frame_presets.frame_preset_deleted.connect(self.removePresetFromList)

        self.frame_choose = QComboBox(self.toolbar)
        self.frame_choose.setMaximumWidth(self.frame_choose.width())
        self.frame_choose.currentIndexChanged.connect(self.changeFrames)
        


        # display elements
        toolbar_layout.addWidget(label)
        toolbar_layout.addWidget(self.frame_choose, Qt.AlignRight)
        toolbar_layout.addWidget(edit_btn)

    def removePresetFromList(self, index:int):
        self.frame_choose.removeItem(index)

    def getPresets(self):
        self.presets_list = self.frame_presets.getPresets()

        self.frame_choose.clear()
        for preset in self.presets_list:
            self.frame_choose.addItem(preset["name"])

    

    def changeFrames(self, index):
        self.captures_list.removeAll()
        path = self.frame_presets.getPresets()[index]["frame_path"]
        print(self.frame_presets.getPresets()[index])
        if path != "":
            self.frame_widget.setPixmapToView(QPixmap(path))
        else:
            self.frame_widget.setPixmapToView(QPixmap(self.rectangle_path))

        self.frame_presets.setCurrentActivePreset(index)

    def frame(self):
        self.frame_widget = PixmapViewer()

    def open_edit_frame_window(self):
        self.edit_frame_window = EditFrameWindow()
        self.edit_frame_window.show()
