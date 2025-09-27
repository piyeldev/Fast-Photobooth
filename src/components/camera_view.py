from PySide6.QtWidgets import (QWidget, 
                               QVBoxLayout, 
                               QHBoxLayout, 
                               QLabel, 
                               QPushButton, 
                               QComboBox, 
                               QSizePolicy,)
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QImage
from PySide6.QtCore import Qt, QTimer, QElapsedTimer ,QDir
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtMultimediaWidgets import QVideoWidget
from components.captures_list import CapturesList
from icecream import ic
from components.resource_path_helper import resource_path
from pygrabber.dshow_graph import FilterGraph

import cv2, os, sys
from time import strftime

class CameraView(QWidget):
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

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        print(sys.platform)
        # OpenCV camera capture
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.aspect_ratio = w / h

        # recording timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_seconds = 0
        self.is_recording = False
        self.out = None

        self.cam_timer = QTimer()
        self.cam_timer.timeout.connect(self.update_frame)
        self.cam_timer.start(30)  # ~30 FPS

        self.cam_placeholder = QLabel()
        self.self_width = self.width()
        self.cam_placeholder.setMaximumWidth(self.width())

        self.toolbar()
        self.camera_buttons_init()
        

        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.toolbar_widget)
        self.layout.addWidget(self.cam_placeholder, alignment=Qt.AlignTop)
        self.layout.addWidget(self.camera_buttons_widget, alignment=Qt.AlignCenter)

    def get_available_cameras(self):
        if sys.platform == 'win32':
            graph = FilterGraph()
            devices = graph.get_input_devices()
            return devices
        else:
            available_cameras = QMediaDevices.videoInputs()
            list_cameras = []
            for camera in available_cameras:
                camera_id = camera.id().data().decode('utf-8') if camera.id().data() else ''
                cam_info = f'{camera.description()}'

                list_cameras.append(cam_info)
            
            return list_cameras
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        # Write frame if recording
        if self.is_recording and self.out:
            self.out.write(frame)

        # convert for display
        w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        height = int((self.self_width * h) /w)
        # print(f'{self.self_width}x{height} ratio: {w/h}, imgW: {w} | imgH: {h}')
        display_frame = cv2.resize(frame, (self.self_width, height), interpolation=cv2.INTER_AREA)

        # Convert frame to QImage
        rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.cam_placeholder.setPixmap(QPixmap.fromImage(qimg))

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
        self.detach_btn.clicked.connect(self.detach_cam)

        self.detach_btn.setIcon(self.detach_icon)
        self.detach_btn.setIconSize(self.detach_icon_img.size())
        self.detach_btn.setStyleSheet("width: 36; height: 36; margin-right: 10px; border-radius: 9px; background-color: #1fb141;")

        self.toolbar_widget_layout.addWidget(self.detach_btn, alignment=Qt.AlignRight)

        self.choose_camera_dropdown()
        # self.choose_res_dropdown()

    def detach_cam(self):
        from windows.camera_window import CameraWindow
        self.cam_window = CameraWindow()
        self.cam_window.show()


    def choose_camera_dropdown(self):
        # camera list dropdown
        self.camera_list = QComboBox()
        self.camera_list.setMaximumWidth(160)
        self.camera_list.setObjectName("cam_list")

        self.camera_list.addItems(self.get_available_cameras())

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
        self.current_camera_index = self.camera_list.currentIndex()
        self.camera_list.currentIndexChanged.connect(self.change_camera)
    
    def change_camera(self, index):
        self.cap.release()
        new_cap = cv2.VideoCapture(index)

        
        new_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        new_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        w = new_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = new_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        print(f'{w}x{h}')
        if not new_cap.isOpened():
            self.camera_list.setCurrentIndex(self.current_camera_index)
            return False
        self.cap = new_cap

        
    def camera_buttons_init(self):
        self.camera_buttons_widget = QWidget()
        layout = QHBoxLayout()
        self.camera_buttons_widget.setLayout(layout)

        self.camera_buttons_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.take_pic_btn()
        self.record_vid_btn()

        layout.addWidget(self.take_pic_btn_widg)
        layout.addWidget(self.record_btn)

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
        QPushButton:hover {
            background-color: #0077b6; 
        }
        """)

        self.take_pic_btn_widg.clicked.connect(self.capture_image)

    def capture_image(self):
        time_date = strftime('%Y%m%d-%H%M%S')
        dir = QDir.homePath() + f"/Pictures/FastPhotoCaptures"

        if not os.path.exists(dir):
            os.mkdir(dir)
        
        save_file = dir + f'/CAPTURED_{time_date}.jpg'
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite(save_file, frame)

        self.display_to_captures_list(save_file)

    def display_to_captures_list(self, img_path: str):
        print("display "+img_path)
        captures_list = CapturesList()
        captures_list.addPicture(img_path)

    def record_vid_btn(self):
        self.record_btn = QPushButton("Record and Auto Capture")
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
            padding: 0 15 0 15;
            height: 53px;
            border-radius: 25px; 
            background-color: #1fb141; 
            color: white;
        }
        QPushButton:hover {
            background-color: #ff7b00; 
            color: white;
        }
        """)
        # self.elapsed_timer = QElapsedTimer()
        # self.update_interval = 100
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_display)

    def record_vid(self):
        if not self.is_recording:
            self.elapsed_seconds = 0
            self.record_btn.setText("Recording: 0s")
            self.timer.start(1000) 
            self.record_btn.setStyleSheet("""
                QPushButton {
                    padding: 0 15 0 15;
                    height: 53px;
                    border-radius: 25px; 
                    background-color: #cd0b0b; 
                    color: white;
                }
                QPushButton:hover {
                    background-color: #ff7b00; 
                    color: white;
                }
                """)
            self.start_recording()
        else:
            self.timer.stop()
            self.record_btn.setText("Start Recording")
            self.stop_recording()

            self.record_btn.setStyleSheet("""
                QPushButton {
                    padding: 0 15 0 15;
                    height: 53px;
                    border-radius: 25px; 
                    background-color: #1fb141; 
                    color: white;
                }
                QPushButton:hover {
                    background-color: #ff7b00; 
                    color: white;
                }
                """)
    
    def update_timer(self):
        self.elapsed_seconds += 1
        self.record_btn.setText(f"Recording: {self.elapsed_seconds}s")

    def start_recording(self):
        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        width  = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps    = self.cap.get(cv2.CAP_PROP_FPS) or 30.0  

        print(f'{width}x{height} @{fps}fps')
        time_date = strftime('%Y%m%d-%H%M%S')
        dir = QDir.homePath() + f"/Pictures/FastPhotoCaptures"

        if not os.path.exists(dir):
            os.mkdir(dir)
        
        save_file = dir + f'/VIDEO_{time_date}.mp4'

        self.out = cv2.VideoWriter(save_file, fourcc, fps, (width, height))
        self.is_recording = True
        print("Recording started...")
    
    def stop_recording(self):
        self.is_recording = False
        if self.out:
            self.out.release()
            self.out = None
        print("Recording stopped.")