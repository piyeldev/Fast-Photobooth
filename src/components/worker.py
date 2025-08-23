from PySide6.QtCore import QThread, Signal
import os, traceback, queue
from icecream import ic
from components.upload_worker import UploadWorker
from components.print_service import PrintService


class WorkerThread(QThread):
    _instance = None
    progress = Signal(str)  # Signal to communicate progress updates to the GUI
    queue_number_notifier = Signal(int)
    current_args_of_operation = Signal(dict)

    @classmethod
    def getInstance(cls, work_queue=None):
        if cls._instance is None:
            if work_queue is None:
                raise ValueError("work_queue must be provided for the first initialization")
            cls._instance = cls(work_queue)
        return cls._instance
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, work_queue):
        if hasattr(self, "initialized") and self.initialized:
            return
        super().__init__()
        self.initialized = True
        self.work_queue = work_queue
        self._is_running = True
        self.upload_worker = UploadWorker()
        self.upload_worker.output.connect(self.print_img)
        self.upload_worker.errorSig.connect(self.notify_error)
        self.print_service = PrintService()
        self.current_args = None
        
    def cancelWork(self, queue_num: int):
        self.work_queue.cancel_task(queue_num)

    def isWorkCanceled(self, queue_num: int):
        return self.work_queue.isCanceled(queue_num)

    
    
    def run(self):
        try:
            while self._is_running:
                try:
                     
                    # Attempt to get a task from the queue with a timeout
                    self.args = self.work_queue.get(timeout=1)
                except queue.Empty:
                    continue  # No task available, continue the loop

                # Notify the GUI of the queue number
                queue_num = self.args["queue_num"]
                self.queue_number_notifier.emit(queue_num)
                self.current_args = self.args

                if self.isWorkCanceled(queue_num):
                    self.progress.emit(f'Task was canceled: {queue_num}')
                    self.work_queue.task_done()
                    continue

                result = self.process_image(self.args)

                is_print_to_pdf = self.args["print_to_pdf"]
                if result is not None:
                    if result == "Printed":
                        continue
                    elif os.path.isfile(result):
                        self.print_img(result, is_print_to_pdf)
                    else:
                        print("Unexpected outcome occured: {result}")
                else:
                    print(f"failed: {queue_num}")
                    self.progress.emit("Failed")

                # Mark the current task as done
                self.work_queue.task_done()


        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            # ic(e, os.path.basename(__file__))

    def process_image(self, args):
        isUploadOnline = args["isUploadOnline"]
        self.printer_instance = args["printer_instance"]
        img_path = args["path_to_img"]
        name = args["name"]
        is_print_to_pdf = args["print_to_pdf"]
        drive_link = args["drive_link"]

        # Initiation of Uploading and/or printing tasks
        if isUploadOnline:
            self.progress.emit("Uploading")
            if not img_path:
                print('img_path is None')
                return
            processed_img_path = self.upload_worker.upload_and_overlay(img_path, name, drive_link)
            
            return processed_img_path
        else:
            self.progress.emit("Printing")
            self.print_img(img_path, is_print_to_pdf)
            return "Printed"

    def print_img(self, img_path:str, is_print_to_pdf: bool):
        self.progress.emit("Printing")
        self.print_service.call(img_path, self.printer_instance, is_print_to_pdf)
        self.progress.emit("Done")


    def notify_error(self, err:str):
        self.current_args_of_operation.emit(self.args)
        self.progress.emit(f'failed: {err}')

    def stop(self):
        self._is_running = False
        self.quit()
        self.wait()
