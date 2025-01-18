from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtMultimedia import QCamera, QMediaDevices, QMediaCaptureSession, QImageCapture
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QSize, QDir, QTimer
from PySide6.QtGui import QColor, QPalette
from components.custom_print import print
from time import strftime
import os

class Camera:
    def __init__(self):
        super().__init__()
        self.camera = None
        self.capture_session = None
        self.image_capture = None

    def initialize_camera(self, video_widget:QVideoWidget, resolution:QSize):
        # Select the default camera
        available_cameras = QMediaDevices.videoInputs()
        if not available_cameras:
            raise RuntimeError("No cameras available")

        # Create the camera and capture session
        self.camera = QCamera(available_cameras[0])
        self.capture_session = QMediaCaptureSession()
        self.capture_session.setCamera(self.camera)

        self.video_widget_var = video_widget
        self.resolution_var = resolution


        # Set the video output to the QVideoWidget
        self.capture_session.setVideoOutput(self.video_widget_var)

        # Create an image capture object
        self.image_capture = QImageCapture(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

        self.set_resolution(self.resolution_var)
        print(self.get_available_cameras())
        # Start the camera
        self.camera.start()


    def capture_image(self):

        if not self.image_capture:
            raise RuntimeError("Image capture not initialized")
        
        time_date = strftime('%Y%m%d-%H%M%S')
        dir = QDir.homePath() + f"/Pictures/FastPhotoCaptures"

        if not os.path.exists(dir):
            os.mkdir(dir)
        
        save_file = dir + f'/NAME_{time_date}.jpg'

        self.image_capture.captureToFile(save_file)

        
        self.image_capture.imageCaptured.connect(lambda: print(f"CAPTURED! Saved {save_file}"))

        self.image_capture.errorOccurred.connect(lambda: print("error occured"))

        return save_file

        

    def get_available_cameras(self):
        available_cameras = QMediaDevices.videoInputs()
        list_cameras = []
        for camera in available_cameras:
            camera_id = camera.id().data().decode('utf-8') if camera.id().data() else ''
            cam_info = f'{camera.description()}:{camera_id}"'

            list_cameras.append(cam_info)
        
        return list_cameras
    
    def change_camera(self, index):
        if self.camera:
            self.camera.stop()

        self.camera = QCamera(QMediaDevices.videoInputs()[index])
        self.capture_session.setCamera(self.camera)

        self.capture_session.setVideoOutput(self.video_widget_var)
        self.set_resolution(self.resolution_var)

        self.image_capture = QImageCapture(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

        self.camera.start()
        
    def set_resolution(self, resolution:QSize):
        supported_formats = self.camera.cameraDevice().videoFormats()
        for format in supported_formats:
            res = format.resolution()
            if (resolution == res):
                print(f'resolution {resolution.width()}x{resolution.height()} is available')
                self.camera.setCameraFormat(format)
                return
                
        raise RuntimeError(f"Resolution {resolution.width}x{resolution.height} not supported by this camera")
