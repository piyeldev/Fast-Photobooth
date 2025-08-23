from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtMultimedia import QCamera, QMediaDevices, QMediaFormat, QMediaCaptureSession, QImageCapture, QMediaRecorder, QVideoFrameFormat
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QSize, QDir, Signal, QUrl, QObject
from PySide6.QtGui import QColor, QPalette, QImage, QPixelFormat
from components.custom_print import print
from time import strftime
import os
from icecream import ic

class Camera(QObject):
    image_captured = Signal(str)
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
        

        # pick first camera
        self.camera = QCamera(available_cameras[0])

        # setup capture session
        self.capture_session = QMediaCaptureSession()
        self.capture_session.setCamera(self.camera)
        self.capture_session.setVideoOutput(video_widget)


        # image capture + recorder
        self.image_capture = QImageCapture()
        self.media_recorder = QMediaRecorder()

        self.capture_session.setImageCapture(self.image_capture)
        self.capture_session.setRecorder(self.media_recorder)

        # Debug error signals
        self.camera.errorOccurred.connect(
            lambda error, errorString: print(f"[Camera Error] {errorString}")
        )
        self.media_recorder.errorOccurred.connect(
            lambda error, errorString: print(f"[Recorder Error] {errorString}")
        )
        self.image_capture.errorOccurred.connect(
            lambda id, error, errorString: print(f"[ImageCapture Error] {errorString}")
        )

        # REMINDER: if camera change, then change the supported format
        supported_formats = self.get_supported_formats()
        if supported_formats:
            self.camera.setCameraFormat(supported_formats[0][1])

        # Start the camera
        self.camera.start()

    def get_supported_formats(self):
        supported_formats = self.camera.cameraDevice().videoFormats()

        res_and_formats_list = []
        for res in supported_formats:
            resolution = res.resolution()
            max_frame_rate = res.maxFrameRate()

            if res.pixelFormat() is QVideoFrameFormat.PixelFormat.Format_Jpeg:
                item = [f'{resolution.width()} x {resolution.height()} @{max_frame_rate}fps', res]
                if not item in res_and_formats_list:
                    res_and_formats_list.append(item)
            
        # for res, format in res_and_formats_list:
        #     print(f'{res} {format.pixelFormat()}')
        return res_and_formats_list

    def set_resolution_and_restart(self, index):
        self.camera.stop()

        supported_formats = self.get_supported_formats()
        print(self.camera.isActive())
        if supported_formats:
            self.camera.setCameraFormat(supported_formats[index][1])
            print(supported_formats[index][1])
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

        # print(f"Recording started: {save_file}")

        # Connect signals for feedback
        # self.media_recorder.errorOccurred.connect(lambda error, errorString: print(f"Error occurred during recording: {errorString}"))
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
        # # ic()
        if not self.image_capture:
            raise RuntimeError("Image capture not initialized")
        
        time_date = strftime('%Y%m%d-%H%M%S')
        dir = QDir.homePath() + f"/Pictures/FastPhotoCaptures"

        if not os.path.exists(dir):
            os.mkdir(dir)
        
        save_file = dir + f'/CAPTURED_{time_date}.jpg'
        self.image_capture.captureToFile(save_file)
        self.image_capture.errorOccurred.connect(lambda: print("error occured"))
        self.image_capture.imageCaptured.connect(lambda id, image: self.handle_return_image_captured(id, image, save_file))

    def handle_return_image_captured(self, id: int, image: QImage, save_path):
        if image.save(save_path):
            print(f"Image saved successfully: {save_path}")
        else:
            print(f'Failed to save image to: {save_path}')
        
        self.image_captured.emit(save_path)

        self.image_capture.imageCaptured.disconnect()


    
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
        
    