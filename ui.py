import threading
import flet as ft
import os, time, asyncio
import lib.libfango as libfango

from desktop_notifier import DesktopNotifier
from math import pi

data = {
    'clock' : '00:00',
    'mode' : 0,
    'run' : False
}

NOTIFIER = DesktopNotifier(app_name="Fango", app_icon="assets/fango.png")

# Notifier
def notify(message):
    async def notif(text):
        notification = await NOTIFIER.send(
            title="Fango",
            message=text,
            sound=True
        )

        time.sleep(5)

        await NOTIFIER.clear(notification)
        await NOTIFIER.clear_all()
    
    asyncio.run(notif(message))

    print("Notification closed successfully")

# Main UI
async def main(page: ft.Page):
    page.title = "Fango"
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
            print(breaker.is_set())
            pomodoro = libfango.pomodoro_timer()
            pomodoro.reset_loop()
            session = 0
            n = None
            while True:
                loop = pomodoro.get_loop()

                data = libfango.get_data(pomodoro, loop)

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
                while seconds:
                    if breaker.is_set():
                        raise Exception("Requested halt")
                    pc = (t_seconds - seconds) * 100 / t_seconds
                    mins, sec = divmod(seconds, 60)
                    timer = '{:02d}:{:02d}'.format(mins, sec)
                    clock.value = timer
                    progress.value = (pc/2) * 0.01
                    print(timer, end='\r')
                    page.update()
                    time.sleep(1)
                    seconds -= 1
            
                pomodoro.add_loop()

                if data['mode'] == libfango.MODES.FREE:
                    #asyncio.run(notify(f"Terminó el tiempo de {data['current_timer']} minutos"))
                    n = threading.Thread(target=notify, args=[f"Terminó el tiempo de {data['current_timer']} minutos"], daemon=True)
                    n.start()
                else:
                    #asyncio.run(notify("Terminó el tiempo de trabajo"))
                    n = threading.Thread(target=notify, args=[f"Terminó el tiempo de trabajo"], daemon=True)
                    n.start()
        except Exception as e:
            print("\nTimer stopped")
            print(e.args)
        finally:
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
            t = threading.Thread(target=pomodoro_timer, daemon=True)
            t.start()
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
        title=ft.Text("Fango", weight=ft.FontWeight.BOLD),
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
