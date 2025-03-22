from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtMultimedia import QCamera, QMediaDevices, QMediaFormat, QMediaCaptureSession, QImageCapture, QMediaRecorder
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QSize, QDir, QTimer, QUrl
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
        self.media_recorder = None

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

        # Create a media recorder for video
        self.media_recorder = QMediaRecorder(self.camera)
        self.capture_session.setRecorder(self.media_recorder)

        self.set_resolution(self.resolution_var)
        print(self.get_available_cameras())
        # Start the camera
        self.camera.start()

    def start_recording(self):
        if not self.media_recorder:
            raise RuntimeError("Media recorder not initialized")

        # Define the save location and format
        time_date = strftime('%Y%m%d-%H%M%S')
        dir = QDir.homePath() + "/Videos/FastPhotoVideoCaptures/"

        if not os.path.exists(dir):
            os.mkdir(dir)

        save_file = dir + f'/RECORD_{time_date}.mp4'

        # Set output location and start recording
        self.media_recorder.setOutputLocation(QUrl.fromLocalFile(save_file))
        media_format = QMediaFormat()
        media_format.setVideoCodec(QMediaFormat.VideoCodec.H264)
        media_format.setFileFormat(QMediaFormat.FileFormat.MPEG4)
        self.media_recorder.setMediaFormat(media_format)
        self.media_recorder.record()

        print(f"Recording started: {save_file}")

        # Connect signals for feedback
        self.media_recorder.errorOccurred.connect(lambda error, errorString: print(f"Error occurred during recording: {errorString}"))
        return save_file

    def isRecording(self):
        if self.media_recorder.recorderState() == QMediaRecorder.RecordingState:
            return True
        else:
            return False
    
    def stop_recording(self):
        if not self.media_recorder:
            raise RuntimeError("Media recorder not initialized")

        if self.media_recorder.recorderState() == QMediaRecorder.RecordingState:
            self.media_recorder.stop()
            print("Recording stopped")
        else:
            print("No recording is active")

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
