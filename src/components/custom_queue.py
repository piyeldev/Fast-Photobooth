import queue

class CustomQueue(queue.Queue):
    def __init__(self):
        super().__init__()
        self.canceled_tasks = set()

    def cancel_task(self, task_id):
        """Mark a task as canceled."""
        self.canceled_tasks.add(task_id)

    def isCanceled(self, task_id):
        if task_id in self.canceled_tasks:
            return True
        return False
    
    def get(self, *args, **kwargs):
        while True:
            try:
                task = super().get(*args, **kwargs)  # blocking
            except queue.Empty:
                raise
            if task.get("queue_num") in self.canceled_tasks:
                self.task_done()
                continue
            return task

