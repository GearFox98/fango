import json
import lib.libfango as libfango

class task():
    def __init__(self, name: str, details: str | None = None, deadline: None = None, done: bool = False) -> None:
        self.name = name
        self.details = details
        self.deadline = deadline
        self.done = done
    
    def get_task(self) -> dict:
        task = {
            'name': self.name,
            'details': self.details,
            'deadline': self.deadline,
            'done': self.done
        }

        return task
    
    def rename(self, name: str):
        self.name = name
    
    def edit(self, details: str):
        self.details = details
    
    def check(self, check: bool):
        self.done = check