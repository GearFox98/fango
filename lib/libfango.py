import os, time, threading
import flet as ft

from enum import Enum
from pathlib import Path

# Notification component
from plyer import notification
from pydub.playback import play
from pydub import AudioSegment

from lib.translations import TRANSLATIONS
from lib.datasets import Config_File
from lib.datasets import Pomodoro_Timer
from lib.path import (TIMER, CONFIG, ROOT_DIR, ASSETS_DIR, USER_DIR)

APP_NAME = "Fang'o timer"
WINDOW_DIM = {
    "NORMAL_H": 450,
    "STATS_H": 500
}

THEME = {
    'LIGHT': "LIGHT",
    'DARK': "DARK"
}

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

# Timer stuff
# Get Data
def get_data(pomodoro: Pomodoro_Timer, loop: int = 1) -> dict:
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

# Animate progress bow on start and on finish
def anim_progress(start: int, end: int, step: int, progress: ft.ProgressRing, page: ft.Page):
        for i in range(start, end, step):
            progress.value = (i / 100)/2
            time.sleep(0.005)
            page.update()

# Timer
# Use with fang-o.py ui component
def timer(page: ft.Page, clock: ft.Text, progress_bow: ft.ProgressRing, mode_label: ft.Text, loop_label: ft.Text, breaker: threading.Event):
        try:
            pomodoro = Pomodoro_Timer()
            pomodoro.reset_loop()
            session = 0 # Session number
            n = None # Notification thread variable
            lang = Config_File().lang
            ui_lang = TRANSLATIONS[lang]
            while True:
                loop = pomodoro.get_loop()

                data = get_data(pomodoro, loop)
                config = Config_File()

                # Gettinf if current loop is a work loop or a free time loop
                if loop % 2 == 0:
                    progress_bow.color = ft.colors.GREEN
                    mode_label.value = f"{ui_lang['STAGES_SECTION'][2]}: {data['current_timer']} min."
                else:
                    progress_bow.color = ft.colors.BLUE
                    #mode_label.value = f"Trabajo"
                    mode_label.value = f"{ui_lang['STAGES_SECTION'][1]}"
                    session += 1
                
                loop_label.value = f"{ui_lang['STAGES_SECTION'][0]}: {session}"

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
                    n = threading.Thread(target=notifier, args=[ui_lang['NOTIFICATIONS'][0], ui_lang['NOTIFICATIONS'][1].format(data['current_timer'])], daemon=True)
                    n.start()
                else:
                    n = threading.Thread(target=notifier, args=[ui_lang['NOTIFICATIONS'][2], ui_lang['NOTIFICATIONS'][3]], daemon=True)
                    n.start()
        except Exception as e:
            print(f"\nTimer stopped by user: {e.args}")
        finally:
            # Reset GUI
            if not n == None:
                n.join()
            clock.value = "00:00"
            anim_progress(int((pc/2)/100), 101, 1, progress_bow, page)

# Config stuff
# Configuration panel functions
def set_option(pomodoro: Pomodoro_Timer, page: ft.Page, text_field: ft.TextField, field_type: str | None):
    try:
        value = int(text_field.value) # type: ignore
        if field_type == "work":
            pomodoro.work_time = value
        elif field_type == "free":
            pomodoro.free_time = value
        elif field_type == "lfree":
            pomodoro.long_free_time = value
        page.update()
        pomodoro.dump_config()
    except Exception as _e:
        config = Config_File()
        lang = config.lang
        warn = TRANSLATIONS[lang]

        def undo(_e):
            pomodoro = Pomodoro_Timer()
            text_field.value = pomodoro.get_wtime() # type: ignore
            page.update()

        page.snack_bar = ft.SnackBar(
                content=ft.Text(warn['WARNINGS'][1], weight=ft.FontWeight.BOLD),
                bgcolor=ft.colors.ORANGE,
                action=warn['BUTTONS'][4],
                on_action=undo
            )
        page.snack_bar.open = True
        page.update()

def set_stats_interface(page: ft.Page, stats: ft.Checkbox | bool, stats_btn: None | ft.TextButton = None):
    value = stats.value if not type(stats) == bool else stats
    if value:
        if not stats_btn == None:
            stats_btn.visible = True
    else:
        if not stats_btn == None:
            stats_btn.visible = False
    page.update()
    print(value)

def change_theme(mode: str):
    config = Config_File()
    config.set_theme(mode)
    config.write_conf()

def save_all(pomodoro: Pomodoro_Timer, page: ft.Page, work: ft.TextField, free: ft.TextField, lfree: ft.TextField, stats: ft.Checkbox, lang: ft.Dropdown, stats_btn: ft.TextButton | None = None):
    set_option(pomodoro, page, work, "work")
    set_option(pomodoro, page, free, "free")
    set_option(pomodoro, page, lfree, "lfree")

    config = Config_File()

    current_lang = config.lang

    if not lang.value == current_lang:
        warn = TRANSLATIONS[lang.value] # type: ignore
        snack = ft.SnackBar(
            content=ft.Row(
                [
                    ft.Icon(
                        ft.icons.INFO,
                        color=ft.colors.WHITE
                    ),
                    ft.Text(
                        value=warn['WARNINGS'][0]
                    ),
                ]
            ),
            bgcolor=ft.colors.BLUE
        )
        page.snack_bar = snack
        page.snack_bar.open = True
        page.update()

    config.set_stats(stats.value) # type: ignore
    config.set_lang(lang.value) # type: ignore

    config.write_conf()
    set_stats_interface(page, stats, stats_btn)
    
    page.update()