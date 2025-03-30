from PySide6.QtCore import QObject, Signal
from queue import Queue
from components.worker import WorkerThread
from icecream import ic

class QueueWorker(QObject):
    _instance = None
    work_added = Signal(list)
    progress = Signal(str)
    notify_current_work_number = Signal(int)
    current_args = Signal(dict)

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
        self.worker_thread.queue_number_notifier.connect(lambda num: self.notify_current_work_number.emit(num))
        self.worker_thread.current_args_of_operation.connect(self.sendCurrentArgs)
        self.worker_thread.start()        

        self.current_work_number = 0

    def sendCurrentArgs(self, args:dict):
        self.current_args.emit(args)

    def setStatus(self, status:str):
        ic()
        self.progress.emit(status)

    def addWork(self, args:dict):
        args["queue_num"] = self.current_work_number
        ic(args)

        data = [f'{args["name"]} - {args["frame_name"]} - {args["size_str"]}', args]
        self.work_added.emit(data)


        self.work_queue.put(args)

        self.current_work_number += 1        

    def stop_worker(self):
        self.worker_thread.stop()

