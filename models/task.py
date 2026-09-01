from models.enums import TaskStatus
from datetime import datetime, date

class Task:
    def __init__(self, title, weight, progress_percent=0, status=TaskStatus.TODO, completed_at=None, deadline=None):
        if weight <= 0:
            raise ValueError("Task Weight Must Be Greater That")
        self.title = title
        self.weight = weight
        self.progress_percent = progress_percent
        self.status = status
        self.completed_at = completed_at
        self.deadline = deadline

    def start(self):
        if self.status == TaskStatus.COMPLETED:
           return
        self.status = TaskStatus.IN_PROGRESS


    def complete(self):
        if self.status == TaskStatus.COMPLETED:
            return 
        self.status = TaskStatus.COMPLETED
        self.progress_percent = 100
        self.completed_at = datetime.now()


    def reopen(self):
        if self.status != TaskStatus.COMPLETED:
            return
        self.status = TaskStatus.REOPENED
        self.progress_percent = 0
        self.completed_at = None

    
    def update_progress(self, percent):
        percent = max(0, min(100, percent))
        if percent == 0:
            self.status = TaskStatus.TODO
            self.progress_percent = 0
            self.completed_at = None
        elif 1 <= percent <= 99:
             self.status = TaskStatus.IN_PROGRESS
             self.progress_percent = percent
             self.completed_at = None
        elif percent == 100:
            self.complete()

    def is_completed(self):
        return self.status == TaskStatus.COMPLETED

    def is_overdue(self, today):
        if self.deadline is None:
           return False
        elif self.is_completed():
            return False
        elif self.deadline < today:
            return True
        else:
            return False

    def to_dict(self):
        return {
            "title": self.title,
            "weight": self.weight,
            "progress_percent": self.progress_percent,
            "status": self.status,
            "completed_at": self.completed_at.isoformat() if self.completed_at is not None else None,
            "deadline": self.deadline.isoformat() if self.deadline is not None else None,
    }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            weight=data["weight"],
            progress_percent=data["progress_percent"],
            status=TaskStatus(data["status"]),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data["completed_at"] is not None else None,
            deadline=date.fromisoformat(data["deadline"]) if data["deadline"] is not None else None,
    )
