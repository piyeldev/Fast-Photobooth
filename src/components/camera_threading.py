from PySide6.QtCore import QThread, Signal
import cv2

class CameraWorker(QThread):
    frame_ready = Signal(object)  # emit numpy frame

    def __init__(self, cam_index=0):
        super().__init__()
        self.cap = cv2.VideoCapture(cam_index)
        # self.cap.set(cv2.CAP_PROP_FPS, 30)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame_ready.emit(frame)

    def stop(self):
        self.running = False
        self.wait()
        if self.cap.isOpened():
            self.cap.release()