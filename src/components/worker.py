from PySide6.QtCore import QThread, Signal
import queue, os
from icecream import ic
from components.upload_worker import UploadWorker
from components.print_service import PrintService

class WorkerThread(QThread):
    progress = Signal(str)  # Signal to communicate progress updates to the GUI
    queue_number_notifier = Signal(int)
    current_args_of_operation = Signal(dict)

    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self._is_running = True
        self.upload_worker = UploadWorker()
        self.upload_worker.output.connect(self.print_img)
        self.upload_worker.errorSig.connect(self.notify_error)
        self.print_service = PrintService()
        self.current_args = None

    def run(self):
        try:
            while self._is_running:
                try:
                    ic()
                    # Attempt to get a task from the queue with a timeout
                    self.args = self.work_queue.get(timeout=1)
                except queue.Empty:
                    continue  # No task available, continue the loop

                # Notify the GUI of the queue number
                queue_num = self.args["queue_num"]
                self.queue_number_notifier.emit(queue_num)
                self.current_args = self.args

                ic()
                ic(self.args, os.path.basename(__file__))
                # Process the task
                self.process_image(self.args)

                # Mark the task as done
                self.work_queue.task_done()
        except Exception as e:
            ic(e, os.path.basename(__file__))

    def process_image(self, args):
        isUploadOnline = args["isUploadOnline"]
        self.printer_instance = args["printer_instance"]
        img_path = args["path_to_img"]

        # Initiation of Uploading and/or printing tasks
        if isUploadOnline:
            ic()
            self.progress.emit("Uploading")
            self.upload_worker.upload_and_overlay(img_path)
        else:
            ic()
            self.progress.emit("Printing")
            self.print_img(img_path)

    def print_img(self, img_path:str):
        ic()
        self.progress.emit("Printing")
        self.print_service.call(img_path, self.printer_instance)
        self.progress.emit("Done")

    def notify_error(self, err:str):
        # ic(self.args == self.current_args, os.path.basename(__file__))
        self.current_args_of_operation.emit(self.args)
        self.progress.emit(err)

    def stop(self):
        self._is_running = False
        self.quit()
        self.wait()
