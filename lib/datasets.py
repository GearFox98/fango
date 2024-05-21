import os, json, datetime
import lib.libfango as libfango

from lib.path import (TIMER, CONFIG, USER_DIR)

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
class Stats():
    LOCATION = f"{USER_DIR}/stats"
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

class Config_File():
    def __init__(self):
        if os.path.exists(CONFIG):
            with open(CONFIG, 'r') as conf:
                config = json.load(conf)
                self.theme = config['theme']
                self.lang = config['lang']
                self.stats = config['stats']
        else:
            with open(CONFIG, 'w') as conf:
                config = {
                    'theme': libfango.THEME['LIGHT'],
                    'lang': 'ES',
                    'stats': False
                }

                json.dump(
                    config,
                    fp=conf,
                    indent= 4
                )

    # Getters
    def get_conf(self) -> dict:
        config = dict()
        with open(CONFIG, 'r') as conf:
            config = json.load(conf)
        return config

    # Setters
    def set_theme(self, theme: str):
        self.theme = theme

    def set_lang(self, lang: str):
        self.lang = lang

    def set_stats(self, stats: bool):
        self.stats = stats

    # Misc
    def write_conf(self):
        with open(CONFIG, 'w') as conf:
            config = {
                'theme': self.theme,
                'lang': self.lang,
                'stats': self.stats
            }

            json.dump(
                config,
                fp=conf,
                indent= 4
            )


class Pomodoro_Timer():
    def __init__(self, work_time: int = 25, free_time: int = 5, long_free_time: int = 15, loop: int = 1):
        if not os.path.exists(TIMER): # Generate config file
            self.work_time = work_time
            self.free_time = free_time
            self.long_free_time = long_free_time
            self.loop = loop

            self.dump_config()
        else: # Load file
            with open(TIMER, mode='r') as conf:
                temp = json.load(conf)
                self.work_time = temp['work']
                self.free_time = temp['free']
                self.long_free_time = temp['long_free']
                self.loop = temp['loop']

    # Get work time
    def get_wtime(self) -> int:
        return self.work_time

    # Get free time
    def get_ftime(self) -> int:
        return self.free_time

    # Get long free time
    def get_lftime(self) -> int:
        return self.long_free_time

    # Get current loop
    def get_loop(self) -> int:
        return self.loop

    # Return a dictionary with the timer attributes
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
        with open(TIMER, mode='w') as conf:
            json.dump(pomodoro, fp=conf, indent=4)

    def reset_loop(self):
        self.loop = 1
        self.dump_config()

    def add_loop(self):
        self.loop += 1
        if self.loop == 9:
            self.loop = 1