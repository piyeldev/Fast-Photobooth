from PySide6.QtCore import QThread, Signal
import queue
from icecream import ic
from components.upload_worker import UploadWorker
from components.print_service import PrintService

class WorkerThread(QThread):
    progress = Signal(str)  # Signal to communicate progress updates to the GUI

    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self._is_running = True
        self.upload_worker = UploadWorker()
        self.upload_worker.output.connect(self.print_img)
        self.print_service = PrintService()

    def run(self):
        while self._is_running:
            try:
                # Attempt to get a task from the queue with a timeout
                args = self.work_queue.get(timeout=1)
            except queue.Empty:
                continue  # No task available, continue the loop

            # Process the task
            result = self.process_image(args)

            # Emit the result to update the GUI
            self.progress.emit(result)

            # Mark the task as done
            self.work_queue.task_done()

    def process_image(self, args):
        self.progress.emit("Getting Ready")
        isUploadOnline = args["isUploadOnline"]
        self.printer_instance = args["printer_instance"]
        img_path = args["path_to_img"]
        ic(isUploadOnline, self.printer_instance, img_path)

        # Initiation of Uploading and/or printing tasks
        if isUploadOnline:
            self.progress.emit("Uploading To Cloud")
            self.upload_worker.upload_and_overlay(img_path)
        else:
            self.print_img(img_path)

    def print_img(self, img_path:str):
        self.progress.emit("Printing")
        self.print_service.call(img_path, self.printer_instance)
        self.progress.emit("Done")

    def stop(self):
        self._is_running = False
        self.quit()
        self.wait()
