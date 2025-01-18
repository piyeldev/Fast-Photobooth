import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtMultimedia import QCamera, QImageCapture, QMediaCaptureSession, QMediaDevices
from PySide6.QtMultimediaWidgets import QVideoWidget

# Camera logic encapsulated in a separate class
class CameraController:
    def __init__(self):
        self.camera = None
        self.capture_session = None
        self.image_capture = None

    def initialize_camera(self, video_widget):
        # Select the default camera
        available_cameras = QMediaDevices.videoInputs()
        if not available_cameras:
            raise RuntimeError("No cameras available")

        # Create the camera and capture session
        self.camera = QCamera(available_cameras[0])
        self.capture_session = QMediaCaptureSession()
        self.capture_session.setCamera(self.camera)

        # Set the video output to the QVideoWidget
        self.capture_session.setVideoOutput(video_widget)

        # Create an image capture object
        self.image_capture = QImageCapture(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

        # Start the camera
        self.camera.start()

    def capture_image(self, callback):
        if not self.image_capture:
            raise RuntimeError("Image capture not initialized")

        def on_image_captured(image_id, image):
            callback(image)

        # Connect the capture signal
        self.image_capture.imageCaptured.connect(on_image_captured)
        self.image_capture.capture()

# Main UI class
class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera App")
        self.setGeometry(100, 100, 800, 600)

        self.camera_controller = CameraController()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Set up the QVideoWidget for live camera feed
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)

        try:
            self.camera_controller.initialize_camera(self.video_widget)
        except RuntimeError as e:
            self.statusBar().showMessage(str(e))
            return

        # Add capture button and display label
        self.capture_button = QPushButton("Capture Image")
        self.capture_button.clicked.connect(self.capture_image)
        layout.addWidget(self.capture_button)

        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def capture_image(self):
        def display_captured_image(image):
            qimage = QImage(image)
            pixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(pixmap.scaled(400, 300))

        self.camera_controller.capture_image(display_captured_image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec())
