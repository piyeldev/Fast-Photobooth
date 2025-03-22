from PySide6.QtWidgets import QWidget, QInputDialog, QCheckBox, QFormLayout, QFileDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QSizePolicy, QComboBox, QGridLayout
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from components.frame import FramePresets
import os
from components.frame_viewport import FrameViewport
from components.pixmap_viewer import PixmapViewer

class EditFrameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Frame")
        self.resize(400, 300)

        self.frame_presets = FramePresets()

        # Add content to the new window
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        label = QLabel("Frame Editor")
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label.setFont(QFont("Poppins", 28, QFont.Weight.Black))
        label.setStyleSheet("padding-top: 10px; padding-left: 10px;")
        self.layout.addWidget(label, Qt.AlignTop)


        self.main_content()
        self.pixmap_viewer = PixmapViewer()
        # self.setStyleSheet("border: 1px solid red;")



    def main_content(self):
        self.main_content_widget = QWidget()
        self.main_content_layout = QHBoxLayout()
        self.main_content_layout.setAlignment(Qt.AlignTop)
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_widget.setLayout(self.main_content_layout)
        self.layout.addWidget(self.main_content_widget)

        self.viewport()
        self.tools()

    def viewport(self):
        pixmap_path = "../assets/imgs/Rectangle.png"

        self.frame_viewport = FrameViewport(pixmap_path)
        self.frame_viewport.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.main_content_layout.addWidget(self.frame_viewport)
        self.main_content_layout.setStretch(0, 4)
        
    def resizeEvent(self, event):
        window_width = event.size().width()
        # print(f'window_width: {window_width}, tools_widget.width: {self.tools_widget.width()}, difference: {window_width - self.tools_widget.width()}')
        self.frame_viewport.setMaximumWidth(window_width - self.tools_widget.width())
        super().resizeEvent(event)

    def tools_form(self):
        self.frame_presets.frame_preset_added.connect(self.parseNewPreset)

        tools_form_widget = QWidget()
        layout = QFormLayout()
        layout.setContentsMargins(0,0,0,0)
        tools_form_widget.setLayout(layout)
        self.tools_layout.addWidget(tools_form_widget)

        # 1 - start
        frame_label = QLabel("Frame Preset: ")
        frame_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.frame_preset_dropdown = QComboBox()
        self.frame_preset_dropdown.currentIndexChanged.connect(self.switchPreset)
        self.frame_preset_dropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addRow(frame_label, self.frame_preset_dropdown)
        # 1 - end

        # 2 - start
        preset_label = QLabel("Preset Name: ")
        frame_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.preset_name = QLabel()

        layout.addRow(preset_label, self.preset_name)
        # 2 - end

        # 3 - start
        path_label = QLabel("Frame Path: ")
        path_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.path_label_button = QPushButton("Add Frame...")
        self.path_label_button.clicked.connect(self.openFiledialogAndAddFrame)

        layout.addRow(path_label, self.path_label_button)
        # 3 - end

        # 4- start
        new_preset_btn = QPushButton("New Preset")
        new_preset_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.add_icon = QIcon("../assets/icons/add_icon.png")
        new_preset_btn.setIcon(self.add_icon)
        new_preset_btn.setStyleSheet("background-color: #1fb141; padding: 5px 10px; border-radius: 0.4em")
        new_preset_btn.clicked.connect(self.createNewPreset)

        delete_preset_btn = QPushButton()
        delete_preset_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.delete_icon = QIcon("../assets/icons/trash_icon.png")
        delete_preset_btn.setIcon(self.delete_icon)
        delete_preset_btn.setStyleSheet("background-color: #1fb141; padding: 5px 10px; border-radius: 0.4em")
        delete_preset_btn.clicked.connect(self.delete_preset)

        layout.addRow(new_preset_btn, delete_preset_btn)

        self.initializePresetDropdown()


    def initializePresetDropdown(self):
        for preset in self.frame_presets.getPresets():
            self.frame_preset_dropdown.addItem(preset["name"])

    def parseNewPreset(self, preset:dict):
        name = preset["name"]

        self.frame_preset_dropdown.addItem(name)
        print(name)

    def switchPreset(self, index):
        # switches the preset's related settings and configs
        preset_selected = self.frame_presets.getPresets()[index]
        name = preset_selected["name"]
        frame_path = preset_selected["frame_path"]
        placeholders = preset_selected["placeholders"]
        qr_code_placeholder = preset_selected["qr_code_placeholder"]

        self.preset_name.setText(name)
        self.path_label_button.setText(frame_path)
        if frame_path == "Add Frame...":
            self.switchFrameViewportImage("")
        else:
            self.switchFrameViewportImage(frame_path)

        for i in range(0, self.placeholders_list.count()):
            self.placeholders_list.takeItem(i)

        for placeholder in placeholders:
            self.placeholders_list.addItem(QListWidgetItem(placeholder["count"]))
        
        
        self.frame_viewport.setPlaceholderList(placeholders)

        if qr_code_placeholder:
            self.frame_viewport.setQRCodePlaceholderOnViewport(qr_code_placeholder)
        else:
            self.frame_viewport.setQRCodePlaceholderOnViewport({"x": 0, "y": 0, "width": 0, "height": 0})



    def delete_preset(self):
        index = self.frame_preset_dropdown.currentIndex()
        self.frame_presets.deletePreset(index)
        self.frame_preset_dropdown.removeItem(index)

        if self.frame_preset_dropdown.count() == 0:
            self.empty_all_fields()

    def empty_all_fields(self):
        self.preset_name.setText("")

    def updateFramePathAndDisplay(self, path:str, index:int):
        self.path_label_button.setText(path)
        self.switchFrameViewportImage(path)

        if index == self.frame_presets.getCurrentIndex():
            self.pixmap_viewer.setPixmapToView(QPixmap(path))


    def createNewPreset(self):
        name, ok = QInputDialog.getText(self, "Preset Name", "Enter Preset Name: ")

        if ok:
            self.frame_presets.createPreset(name)
        else:
            return None
        
    def openFiledialogAndAddFrame(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files(*);;Image Files (*.png, *.jpg, *.jpeg, *.bmp, *.svg)")

        current_index = self.frame_preset_dropdown.currentIndex()
        if file_path != "":
            self.frame_presets.addFrameToPreset(current_index, file_path)
            self.updateFramePathAndDisplay(file_path, current_index)

    def tools(self):
        self.tools_widget = QWidget(self)
        self.tools_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.tools_layout = QVBoxLayout()
        self.tools_layout.setAlignment(Qt.AlignTop)
        self.tools_widget.setLayout(self.tools_layout)
        self.main_content_layout.addWidget(self.tools_widget)
        self.main_content_layout.setStretch(1, 1)

        self.tools_form()
        self.placeholders()
        self.qrCodeModeSwitcher()

        # save to file feature later

    def qrCodeModeSwitcher(self):
        self.is_qr_code_mode = QCheckBox("Create QR Code Placeholder")
        self.is_qr_code_mode.checkStateChanged.connect(self.switchQRCodeMode)
        self.tools_layout.addWidget(self.is_qr_code_mode)
    
    def switchQRCodeMode(self, state):
        if state == Qt.CheckState.Checked:
            print("yes")
            self.frame_viewport.set_is_qr_code_mode(True)
        else:
            print("yes")
            self.frame_viewport.set_is_qr_code_mode(False)

    def switchFrameViewportImage(self, img_path:str):
        self.frame_viewport.set_pixmap(img_path)

    def update_frame_chooser_dropdown(self, items):
        self.frame_chooser_dropdown.clear()
        self.frame_chooser_dropdown.addItems(items)

    def placeholders(self):
        placeholders_tool = QWidget()
        placeholders_tool.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        placeholders_layout = QVBoxLayout()
        placeholders_layout.setContentsMargins(0,0,0,0)
        placeholders_tool.setLayout(placeholders_layout)
        self.tools_layout.addWidget(placeholders_tool)

        # toolbar ------- start
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(0,0,0,0)
        toolbar.setLayout(toolbar_layout)
        placeholders_layout.addWidget(toolbar)

        label = QLabel("Placeholders")
        toolbar_layout.addWidget(label)

        delete_btn = QPushButton()
        delete_btn.setIcon(self.delete_icon)
        delete_btn.setFlat(True)
        delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        toolbar_layout.addWidget(delete_btn)

        # toolbar ------ end

        # placehoders list ---- start
        self.frame_viewport.placeholder_added.connect(self.parsePlaceholderInformation)
        self.frame_viewport.qr_code_placeholder_added.connect(self.parseQrCodePlaceholderInformation)

        self.placeholders_list = QListWidget()
        placeholders_layout.addWidget(self.placeholders_list)

    def parsePlaceholderInformation(self, placeholder:dict):
        count = placeholder["count"]
        self.placeholders_list.addItem(QListWidgetItem(count))

        current_index = self.frame_preset_dropdown.currentIndex()
        self.frame_presets.addPlaceholderToPreset(current_index, placeholder)

    def parseQrCodePlaceholderInformation(self, qr_code_placeholder:dict):
        current_index = self.frame_preset_dropdown.currentIndex()
        self.frame_presets.setQrCodePlaceholder(current_index, qr_code_placeholder)
        




        
    
