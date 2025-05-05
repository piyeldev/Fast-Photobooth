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
        """Override get to skip canceled tasks."""
        while not self.empty():
            task = super().get(*args, **kwargs)
            if task["queue_num"] not in self.canceled_tasks:
                return task
            else:
                # print(f"CUSTOM_QUEUE: Task {task["queue_num"]} is canceled")
                self.task_done()
        raise queue.Empty

