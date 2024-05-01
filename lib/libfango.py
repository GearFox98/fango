import os, json
from enum import Enum

CONFIG = str(os.path.expanduser('~/.fango/config.json'))

class MODES(Enum):
    WORKING = 0,
    FREE = 1,

# Values for timer
class pomodoro_timer:
    work_time: int = 25
    free_time: int = 5
    long_free_time: int = 15
    loop: int = 1

    def __init__(self, work_time: int = 25, free_time: int = 5, long_free_time: int = 15, loop: int = 1):
        if not os.path.exists(CONFIG): # Generate config file
            self.work_time = work_time
            self.free_time = free_time
            self.long_free_time = long_free_time
            self.loop = loop

            self.dump_config()
        else: # Load file
            with open(CONFIG, mode='r') as conf:
                temp = json.load(conf)
                self.work_time = temp['work']
                self.free_time = temp['free']
                self.long_free_time = temp['long_free']
                self.loop = temp['loop']

    def get_wtime(self) -> int:
        return self.work_time
    
    def get_ftime(self) -> int:
        return self.free_time
    
    def get_lftime(self) -> int:
        return self.long_free_time
    
    def get_loop(self) -> int:
        return self.loop
    
    def get_pomodoro(self) -> dict:
        pomodoro = {
            'work' : self.work_time,
            'free' : self.free_time,
            'long_free' : self.long_free_time,
            'loop' : self.loop
        }

        return pomodoro
    
    def dump_config(self):
        pomodoro = self.get_pomodoro()
        # Dump file
        with open(CONFIG, mode='w') as conf:
            json.dump(pomodoro, fp=conf, indent=4)
    
    def reset_loop(self):
        self.loop = 1
        self.dump_config()
    
    def add_loop(self):
        self.loop += 1
        if self.loop == 9:
            self.loop = 1
        self.dump_config()

# Get Data
def get_data(pomodoro: pomodoro_timer, loop: int = 1) -> dict:
    # Reset counter
    if loop == 9:
        loop = 1
    
    if loop % 8 == 0:
        mode = MODES.FREE
        current_timer = pomodoro.get_lftime()
    elif loop % 2 == 0:
        mode = MODES.FREE
        current_timer = pomodoro.get_ftime()
    else:
        mode = MODES.WORKING
        current_timer = pomodoro.get_wtime()
    
    data = {
        'current_timer' : current_timer,
        'mode' : mode,
        'loop' : loop
    }

    return data