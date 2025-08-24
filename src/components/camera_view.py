from PySide6.QtWidgets import (QWidget, 
                               QVBoxLayout, 
                               QHBoxLayout, 
                               QLabel, 
                               QPushButton, 
                               QComboBox, 
                               QSizePolicy,
                               QStackedLayout)
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter
from PySide6.QtCore import Qt, QRect, QSize, QTimer, QElapsedTimer
from PySide6.QtMultimediaWidgets import QVideoWidget
from components.camera import Camera
from components.captures_list import CapturesList
from icecream import ic
from components.resource_path_helper import resource_path

class CameraView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        #init camera class
        self.camera_controller = Camera()
        self.camera_controller.image_captured.connect(self.display_to_captures_list)

        self.cam_feed()
        self.toolbar()
        self.camera_buttons_init()
        

        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.toolbar_widget)
        self.layout.addWidget(self.cam_widg, alignment=Qt.AlignTop)
        self.layout.addWidget(self.camera_buttons_widget, alignment=Qt.AlignCenter)

        

    def toolbar(self):
        self.toolbar_widget = QWidget()
        self.toolbar_widget_layout = QHBoxLayout()
        self.toolbar_widget_layout.setContentsMargins(0,0,0,10)
        self.toolbar_widget.setLayout(self.toolbar_widget_layout)

        # camera view lbl
        self.cam_view_lbl = QLabel("Camera View")
        self.cam_view_lbl_font = QFont("Poppins", 10, QFont.Weight.Bold)
        self.cam_view_lbl.setMargin(3)
        self.cam_view_lbl.setFont(self.cam_view_lbl_font)

        self.toolbar_widget_layout.addWidget(self.cam_view_lbl, alignment=Qt.AlignBottom)

        # detach icon btn
        self.detach_btn = QPushButton()
        self.detach_icon_img = QPixmap(resource_path("assets/icons/detach-icon.png"))
        self.detach_icon = QIcon(self.detach_icon_img)
        self.detach_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.detach_btn.setIcon(self.detach_icon)
        self.detach_btn.setIconSize(self.detach_icon_img.size())
        self.detach_btn.setStyleSheet("width: 36; height: 36; margin-right: 10px; border-radius: 9px; background-color: #1fb141;")

        self.toolbar_widget_layout.addWidget(self.detach_btn, alignment=Qt.AlignRight)

        self.choose_camera_dropdown()
        self.choose_res_dropdown()

        
    def choose_res_dropdown(self):
        supported_resolutions = self.camera_controller.get_supported_formats()
        self.res_dropdown = QComboBox()

        self.res_dropdown.addItems(([item[0] for item in supported_resolutions]))
        self.toolbar_widget_layout.addWidget(self.res_dropdown)

        self.res_dropdown.currentIndexChanged.connect(self.res_change)

    def res_change(self, index):
        print(index)
        self.camera_controller.set_resolution_and_restart(index)


    def choose_camera_dropdown(self):
        # camera list dropdown
        self.camera_list = QComboBox()
        self.camera_list.setMaximumWidth(160)
        self.camera_list.setObjectName("cam_list")

        self.camera_list.addItems(self.camera_controller.get_available_cameras())

        self.camera_list.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.camera_list.view().window().setAttribute(Qt.WA_TranslucentBackground)

        self.camera_list.setFont(QFont("Poppins", 10, QFont.Weight.DemiBold))

        self.toolbar_widget_layout.addWidget(self.camera_list)
        self.camera_list.setStyleSheet("""
        
        QComboBox {
            padding-left: 10px;
            border-radius: 10px; 
            border: 3px solid #565b5e;
            height: 30px;
        }
        
        """)

        self.camera_list.currentIndexChanged.connect(self.camera_controller.change_camera)

    

    def cam_feed(self):
        self.cam_widg = QWidget()
        self.cam_widg.setFixedSize(640, 480)
        layout = QVBoxLayout()
        self.cam_widg.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)
        self.video_widget.setFixedSize(640, 480)

        try:
            self.camera_controller.initialize_camera(self.video_widget, QSize(640, 480))
        except RuntimeError as e:
            print(e)

        
    def camera_buttons_init(self):
        self.camera_buttons_widget = QWidget()
        layout = QHBoxLayout()
        self.camera_buttons_widget.setLayout(layout)

        self.camera_buttons_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.take_pic_btn()
        # self.record_vid_btn()

        layout.addWidget(self.take_pic_btn_widg)
        # layout.addWidget(self.record_btn)

    def take_pic_btn(self):
        self.take_pic_btn_widg = QPushButton()
        self.take_pic_btn_widg.setCursor(Qt.CursorShape.PointingHandCursor)
        self.take_pic_btn_widg.setFixedWidth(53)
        self.take_pic_btn_widg.setFixedHeight(53)
        self.take_pic_pxmp = QPixmap(resource_path("assets/icons/camera_icon.png"))
        self.take_pic_icon = QIcon()
        self.take_pic_btn_widg.setIconSize(self.take_pic_pxmp.rect().size())
        self.take_pic_icon.addPixmap(self.take_pic_pxmp)
        self.take_pic_btn_widg.setIcon(self.take_pic_icon)
        self.take_pic_btn_widg.setStyleSheet("""
        QPushButton {
            border-radius: 25px; 
            background-color: #1fb141; 
        }
        """)

        self.take_pic_btn_widg.clicked.connect(self.capture_img)
    
    def capture_img(self):
        # # ic()
        self.camera_controller.capture_image()

    def display_to_captures_list(self, img_path: str):
        print("display "+img_path)
        captures_list = CapturesList()
        captures_list.addPicture(img_path)

    def record_vid_btn(self):
        self.record_btn = QPushButton("Record")
        self.record_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.record_btn.clicked.connect(self.record_vid)
        record_pxmp = QPixmap(resource_path("assets/icons/video-icon.png"))
        record_icon = QIcon()
        record_icon.addPixmap(record_pxmp)

        self.record_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        record_btn_font = QFont("Poppins", 14, QFont.Weight.Bold)
        self.record_btn.setFont(record_btn_font)

        self.record_btn.setIcon(record_icon)
        self.record_btn.setIconSize(record_pxmp.rect().size())

        self.record_btn.setStyleSheet("""
        QPushButton {
            width: 130px;
            height: 53px;
            border-radius: 25px; 
            background-color: #1fb141; 
        }
        """)
        self.elapsed_timer = QElapsedTimer()
        self.update_interval = 100
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
    
    def start_recording(self):
        self.elapsed_timer.start()
        self.time_button.setText("Stop Timing")
        self.result_label.setText("Timing in progress...")
        self.timer.start(self.update_interval) 

        self.camera_controller.start_recording()

    def stop_recording(self):
        self.timer.stop()  # Stop the update timer
        elapsed_seconds = self.elapsed_timer.elapsed() // 1000
        self.result_label.setText(f"Total time elapsed: {elapsed_seconds} seconds")
        self.time_button.setText("Start Timing")
        self.elapsed_timer.invalidate()

        self.camera_controller.stop_recording()


    def update_display(self):
        if self.elapsed_timer.isValid():
            elapsed_seconds = self.elapsed_timer.elapsed() // 1000
            self.record_btn.setText(f"{elapsed_seconds}")

    def record_vid(self):
        is_recording = self.camera_controller.isRecording()

        if not is_recording:
            self.camera_controller.start_recording()
        else:
            self.camera_controller.stop_recording()
