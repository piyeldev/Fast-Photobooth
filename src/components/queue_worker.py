from PySide6.QtCore import QObject, Signal
from queue import Queue
from components.worker import WorkerThread
from components.custom_queue import CustomQueue
from icecream import ic
import os

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

        self.work_queue = CustomQueue()
        self.worker_thread = WorkerThread(self.work_queue)
        self.worker_thread.progress.connect(self.setStatus)
        self.worker_thread.queue_number_notifier.connect(self.sendNum)
        self.worker_thread.current_args_of_operation.connect(self.sendCurrentArgs)
        self.worker_thread.start()

        self.queue_history = QueueHistory()

        self.current_work_number = 0

    def sendNum(self, num):
        self.notify_current_work_number.emit(num)

    def sendCurrentArgs(self, args:dict):
        self.current_args.emit(args)

    def setStatus(self, status:str):
        self.progress.emit(status)

    def addWork(self, args:dict):
        args["queue_num"] = self.current_work_number

        data = [f'{args["name"]} - {args["frame_name"]} - {args["size_str"]}', args["queue_num"]]
        self.work_added.emit(data)
        self.work_queue.put(args)
        
        self.queue_history.add_to_history(args)
        self.current_work_number += 1        

    def stop_worker(self):
        self.worker_thread.stop()
    

class QueueHistory(QObject):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, "initialized") and self.initialized:
            return
        super().__init__()
        self.initialized = True

        self.queue_list = []

    def add_to_history(self, args:dict):
        self.queue_list.append(args)

    def find_item_from_specific_queue_num(self, num: int):
        for i in range(len(self.queue_list)):
            item = self.queue_list[i]
            item_num = item["queue_num"]
            if item_num == num:
                return item
        return None
        