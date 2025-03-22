from PySide6.QtCore import QObject, Signal
from queue import Queue
from components.worker import WorkerThread
from icecream import ic

class QueueWorker(QObject):
    _instance = None
    work_added = Signal(str)
    progress = Signal(str)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, "initialized") and self.initialized:
            return
        super().__init__()
        self.initialized = True

        self.work_queue = Queue()
        self.worker_thread = WorkerThread(self.work_queue)
        self.worker_thread.progress.connect(self.setStatus)
        # status code GOES HERE
        self.worker_thread.start()        


    def setStatus(self, status:str):
        self.progress.emit(status)

    def addWork(self, args:dict):
        self.work_queue.put(args)
        list_title = f'{args["name"]} - {args["frame_name"]} - {args["size_str"]}'
        self.work_added.emit(list_title)
        pass

    def stop_worker(self):
        self.worker_thread.stop()

