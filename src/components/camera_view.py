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

import cv2, os
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

        # OpenCV camera capture
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.aspect_ratio = w / h
        # self.aspect_ratio = 16/9

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

    def get_supported_formats(self):
        supported_formats = self.camera.cameraDevice().videoFormats()

        res_and_formats_list = []
        for res in supported_formats:
            resolution = res.resolution()
            max_frame_rate = res.maxFrameRate()
            print(f'formats {res.pixelFormat()} + {res.resolution()}')
            if res.pixelFormat() is QVideoFrameFormat.PixelFormat.Format_Jpeg:
                item = [f'{resolution.width()} x {resolution.height()} @{max_frame_rate}fps', res]
                if not item in res_and_formats_list:
                    res_and_formats_list.append(item)
            
        # for res, format in res_and_formats_list:
        #     print(f'{res} {format.pixelFormat()}')
        print(f"res and formats list {res_and_formats_list}")
        self.res_change(1)
        return res_and_formats_list
    
    def choose_res_dropdown(self):
        self.supported_resolutions = self.get_supported_formats()
        self.res_dropdown = QComboBox()

        self.res_dropdown.addItems(([item[0] for item in supported_resolutions]))
        self.toolbar_widget_layout.addWidget(self.res_dropdown)

        self.res_dropdown.currentIndexChanged.connect(self.res_change)

    def res_change(self, index):
        # print(index)
        # self.cap.release()
        # new_cap = cv2.VideoCapture(self.current_camera_index)
        resW = self.supported_resolutions[index][1]
        print(resW)
        # new_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # new_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # self.cap = new_cap
        # self.camera_controller.set_resolution_and_restart(index)


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
        if not new_cap.isOpened():
            self.camera_list.setCurrentIndex(self.current_camera_index)
            return False
        new_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        new_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
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
