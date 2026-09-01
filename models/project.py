from models.task import Task
from datetime import date



class Project:
    def __init__(self, name, start_date, deadline, tasks = None):
        if start_date >= deadline:
            raise ValueError(f"Start date must be before deadline.")
        if tasks is None:
           tasks=[]
        self.tasks = tasks
        self.name = name
        self.start_date = start_date
        self.deadline = deadline


    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                return
        raise ValueError(f"Task '{title}' not found.")

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
               return task
        return None

    def update_task(self, title, new_title=None, new_weight=None, new_deadline=None):
        task = self.get_task(title)
        if task is None:
           raise ValueError(f"Task '{title}' not found.")
        if new_title is not None:
           task.title = new_title
        if new_weight is not None:
            if new_weight <= 0:
               raise ValueError("Task weight must be greater than zero.")
            task.weight = new_weight
        if new_deadline is not None:
           task.deadline = new_deadline

    def get_completed_tasks(self):
        result = []
        for task in self.tasks:
            if task.is_completed():
                result.append(task)
        return result


    def get_pending_tasks(self):
        result = []
        for task in self.tasks:
            if not task.is_completed():
                result.append(task)
        return result
    
    def to_dict(self):
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "deadline": self.deadline.isoformat(),
            "tasks": [task.to_dict() for task in self.tasks],
    }

    @classmethod
    def from_dict(cls, data):
        tasks = [Task.from_dict(task_data) for task_data in data["tasks"]]
        return cls(
           name=data["name"],
           start_date=date.fromisoformat(data["start_date"]),
           deadline=date.fromisoformat(data["deadline"]),
           tasks=tasks,
    )
