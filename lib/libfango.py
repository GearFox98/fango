import os, json, time, threading
import flet as ft
from enum import Enum
from pathlib import Path
from plyer import notification
from pydub.playback import play
from pydub import AudioSegment


CONFIG = str(os.path.expanduser('~/.fango/config.json'))
APP_NAME = "Fang'o timer"
#ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = Path(os.path.realpath(__file__)).parent.parent
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

class MODES(Enum):
    WORKING = 0,
    FREE = 1,

# Notifier
def notifier(title:str, message: str):
    icon = os.path.join(ASSETS_DIR, "icon.png")
    sound = os.path.join(ASSETS_DIR, "notification.mp3")
    notification.notify(
        app_name=APP_NAME,
        title=title,
        message=message,
        timeout=5,
        app_icon=icon
    ) # type: ignore

    if os.path.exists(sound):
        notifier_sound = AudioSegment.from_mp3(sound)
        play(notifier_sound)
    else:
        print(f"Fang says: {sound} can't be found!")

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

# Animate progress
def anim_progress(start: int, end: int, step: int, progress: ft.ProgressRing, page: ft.Page):
        for i in range(start, end, step):
            progress.value = (i / 100)/2
            time.sleep(0.005)
            page.update()

# Timer
# Use with fang-o.py ui component
def timer(page: ft.Page, clock: ft.Text, progress_bow: ft.ProgressRing, mode_label: ft.Text, loop_label: ft.Text, breaker: threading.Event):
        try:
            pomodoro = pomodoro_timer()
            pomodoro.reset_loop()
            session = 0 # Session number
            n = None # Notification thread variable
            while True:
                loop = pomodoro.get_loop()

                data = get_data(pomodoro, loop)

                # Gettinf if current loop is a work loop or a free time loop
                if loop % 2 == 0:
                    progress_bow.color = ft.colors.GREEN
                    mode_label.value = f"Descanso: {data['current_timer']} min."
                else:
                    progress_bow.color = ft.colors.BLUE
                    mode_label.value = f"Trabajo"
                    session += 1
                
                loop_label.value = f"Sesión: {session}"

                seconds = data['current_timer'] * 60
                t_seconds = seconds
                # Timer
                while seconds:
                    if breaker.is_set():
                        raise Exception("Requested halt") # Thread breaker
                    pc = (t_seconds - seconds) * 100 / t_seconds
                    mins, sec = divmod(seconds, 60)
                    timer = '{:02d}:{:02d}'.format(mins, sec)
                    clock.value = timer
                    progress_bow.value = (pc/2) * 0.01
                    print(timer, end='\r')
                    page.update()
                    time.sleep(1)
                    seconds -= 1
            
                pomodoro.add_loop() # Update loop in pomodoro object

                # Notification sub threads
                if data['mode'] == MODES.FREE:
                    n = threading.Thread(target=notifier, args=["A trabajar", f"Terminó el tiempo de descanso {data['current_timer']} minutos"], daemon=True)
                    n.start()
                else:
                    n = threading.Thread(target=notifier, args=["Tiempo de descansar", f"Terminó el tiempo de trabajo"], daemon=True)
                    n.start()
        except Exception as e:
            print(f"\nTimer stopped by user: {e.args}")
        finally:
            # Reset GUI
            if not n == None:
                n.join()
            clock.value = "00:00"
            anim_progress(int((pc/2)/100), 101, 1, progress_bow, page)