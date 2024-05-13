import os, json, datetime
import lib.libfango as libfango

class task():
    # Each task has Name, Details, a Deadline and can be Done or not (by default they're not done: False)
    def __init__(self, name: str, details: str | None = None, deadline: None = None, done: bool = False) -> None:
        self.name = name
        self.details = details
        self.deadline = deadline
        self.done = done
    
    # Returns a dictionary with each attribute (Name, Details, Deadline and Done)
    def get_task(self) -> dict:
        task = {
            'name': self.name,
            'details': self.details,
            'deadline': self.deadline,
            'done': self.done
        }

        return task
    
    # Renames the selected task (Modify Name)
    def rename(self, name: str):
        self.name = name
    
    # Edits the selected task (Modify Details)
    def edit(self, details: str):
        self.details = details
    
    # Checks or not the selected task (Modify Done)
    def check(self, check: bool):
        self.done = check

# How many times work is done in a day in seconds (Total of working time spent)
# How many free time is achieved in a day in seconds (Total of free time achieved)
# In a week, average of work and rest (Line graph), store in year-month file
# Compare with a standard work/rest value (or with averages)
# THIS STRUCTURE IS NOT ITERABLE, PANDAS MUST BE USED
# file = {
#   "MONTH": {
#       "TODAY": (WORK_TIME, FREE_TIME, LOOPS)
#   }
# }
class stats():
    LOCATION = f"{libfango.USER_DIR}/stats"
    TODAY = datetime.date.today()
    MONTH = str(TODAY)[0:7]
    FILE = f"{LOCATION}/{str(TODAY)[0:7]}.json"
    
    def __init__(self, work_time: int = 0, free_time: int = 0, loops: int = 0):
        if not os.path.exists(self.LOCATION):
            os.mkdir(self.LOCATION)
        if not os.path.exists(self.FILE):
            # Create base file fot current month
            self.work_time = work_time
            self.free_time = free_time
            self.loops = loops
            with open(self.FILE, 'w') as stats:
                pass
        else:
            # Load current month file
            with open(self.FILE, 'r') as stats:
                pass
    
    # Adds a second to the work_time variable
    def add_work_time(self):
        self.work_time += 1
    
    # Adds a second to the free_time variable
    def add_free_time(self):
        self.free_time += 1