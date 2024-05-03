import threading
import flet as ft
import os, time
import lib.libfango as libfango

from plyer import notification
from math import pi

APP_NAME = "Fang'o timer"

data = {
    'clock' : '00:00',
    'mode' : 0,
    'run' : False
}

# Notifier
def notifier(title:str, message: str):
    icon = os.path.realpath("assets/icon.png")
    notification.notify(
        app_name=APP_NAME,
        title=title,
        message=message,
        timeout=5,
        app_icon=icon
    )

# Main UI
async def main(page: ft.Page):
    page.title = APP_NAME
    page.window_max_height = 400
    page.window_max_width = 415
    page.window_min_height = 400
    page.window_min_width = 415
    page.window_maximizable = False
    page.padding = 0

    clock = ft.Text(value='00:00', text_align=ft.TextAlign.CENTER, size=54)
    progress = ft.ProgressRing(value=0.5, rotate=-pi/2, width=300, height=300, stroke_width=30, color=ft.colors.BLUE)
    progress_shadow = ft.ProgressRing(value=0.5, rotate=-pi/2, width=300, height=300, stroke_width=30, color=ft.colors.GREY)
    
    # Stages attributes
    loop_label = ft.Text("Sesión: 0", size=24)
    mode_label = ft.Text("Trabajo", size=24)
    
    # Stages (Below the clock)
    stages = ft.Row(
        [
            loop_label, # Loop Number
            mode_label # Mode
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Timer component
    timer = ft.Container(
        ft.Stack(
            [
                ft.Container(
                    content=progress_shadow,
                    width=410,
                    height=330,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=progress,
                    width=410,
                    height=330,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=30),
                            ft.Row([clock], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Divider(),
                            stages,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        
                    ),
                    width=410,
                    height=330,
                    alignment=ft.alignment.center,
                    padding=35
                )
            ]
        )
    )

    # Animate progress
    def anim_progress(start: int, end: int, step: int):
        for i in range(start, end, step):
            progress.value = (i / 100)/2
            time.sleep(0.005)
            page.update()

    # Threaded Functions
    # To cancel the process
    breaker = threading.Event()

    # Main function
    def pomodoro_timer():
        try:
            pomodoro = libfango.pomodoro_timer()
            pomodoro.reset_loop()
            session = 0 # Session number
            n = None # Notification thread variable
            while True:
                loop = pomodoro.get_loop()

                data = libfango.get_data(pomodoro, loop)

                # Gettinf if current loop is a work loop or a free time loop
                if loop % 2 == 0:
                    progress.color = ft.colors.GREEN
                    mode_label.value = f"Descanso: {data['current_timer']} min."
                else:
                    progress.color = ft.colors.BLUE
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
                    progress.value = (pc/2) * 0.01
                    print(timer, end='\r')
                    page.update()
                    time.sleep(1)
                    seconds -= 1
            
                pomodoro.add_loop() # Update loop in pomodoro object

                # Notification sub threads
                if data['mode'] == libfango.MODES.FREE:
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
            anim_progress(int((pc/2)/100), 101, 1)

    # Activate daemon break
    def set_breaker(_e):
        if data['run'] == False:
            anim_progress(100, -1, -1)
            breaker.clear()
            data['run'] = True
            main_button.icon = ft.icons.STOP
            main_button.text = "Detener"
            t = threading.Thread(target=pomodoro_timer, daemon=True, name="Timer")
            t.start()
            print(f"Started thread: {t.name}")
        else:
            data["run"] = False
            main_button.icon = ft.icons.PLAY_ARROW
            main_button.text = "Iniciar"
            breaker.set()
            page.update()

    # UI
    main_button = ft.TextButton(
        text="Iniciar",
        icon=ft.icons.PLAY_ARROW,
        icon_color=ft.colors.BLACK,
        on_click=set_breaker
    )

    # TODO - Options view
    option_button = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(
                    name=ft.icons.SETTINGS,
                    color=ft.colors.BLACK
                )
            ]
        ),
        width=50,
        disabled=True
    )

    # App menu
    page.appbar = ft.AppBar(
        title=ft.Text(APP_NAME, weight=ft.FontWeight.BOLD),
        actions=[
            main_button,
            option_button
        ]
    )

    await page.add_async(timer)

# Create config folder
if not os.path.exists(os.path.expanduser("~/.fango")):
    os.mkdir(os.path.expanduser("~/.fango"))

ft.app(target=main)
